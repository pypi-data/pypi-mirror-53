class RecentUseCache:
    def __init__(self, max_records=200, auto_flush_down_to=50):
        if auto_flush_down_to > max_records:
            raise RuntimeError('"auto_flush_down_to" should be less than "max_records"')

        # must ensure that when the cache is auto_flushed the last added record remains,
        # this is import if we are "ensure_overwrite" is True when calling "addDoc"
        if auto_flush_down_to <= 0:
            raise RuntimeError('"auto_flush_down_to" should be greater than zero')

        # hash table of data, data is accessed using unique key
        self.docs = {}
        # array of document keys. Document keys that were added or accessed most recently will be at the bottom
        self.doc_ordering = [] 
        # hash table of where in doc_ordering a particular key can be found; search arrays is slow, this optimises it
        self.doc_ordering_lookup = {}
        self.num_empty_doc_order_recs = 0
        self.max_records = max_records
        self.auto_flush_down_to = auto_flush_down_to # specifies number of remaining records after and auto_flush
        self.onFlush = lambda docs: False

    def __len__(self): 
        return self._getNumDocs()

    def __contains__(self, key):
        return key in self.docs

    def _getNumDocs(self): 
        num_docs = len(self.doc_ordering) - self.num_empty_doc_order_recs
        return num_docs

    def addVal(self, key, val):

        # if document already exists in the cache, allow it to be over written
        # but also update the order in which documents were added
        if key in self.docs:
            self._removeOldOrdering(key)

        self.docs[key] = val
        self._addNewOrdering(key)

        if len(self) > self.max_records:
            self._autoFlush() 

    def getVal(self, key):
        if key in self.docs:
            self._removeOldOrdering(key)
            self._addNewOrdering(key)
            return self.docs[key]
        else:
            return None

    def flushAll(self):
        return self._flush()

    def _autoFlush(self):
        num_docs_to_flush = len(self) - self.auto_flush_down_to
        flushed_docs = self._flush(num_docs_to_flush)

    def _flush(self, num_docs_to_flush=None):
        # if numDocsToFlush is None (not a number), then all docs will be flushed
        def rebuildDocOrder_closure(num_docs_to_flush):
            # curry the question of whether `num_doc_to_flush is None`
            if num_docs_to_flush is None:
                return lambda num_flushed_docs: False
            else:
                return lambda num_flushed_docs: (num_flushed_docs >= num_docs_to_flush)

        rebuildDocOrder = rebuildDocOrder_closure(num_docs_to_flush)
        
        flushed_docs = {}
        num_flushed_docs = 0
        new_doc_ordering = []
        doc_order_ind = -1
        rebuild_doc_order = False       # initial state
        for key in self.doc_ordering:
            # if num_docs_to_flush AND (num_flushed_docs >= num_docs_to_flush)
            if rebuild_doc_order: 
                # rebuild state for remaining documents
                doc_order_ind += 1
                new_doc_ordering.append(key)
                self.doc_ordering_lookup[key] = doc_order_ind
            else: # (while rebuild_doc_order = False)
                # many docs are None, because they were moved to the end of the ordering list
                if key is None:
                    self.num_empty_doc_order_recs -= 1
                    continue

                num_flushed_docs += 1
                flushed_docs[key] = self.docs[key]
                del self.docs[key]
                del self.doc_ordering_lookup[key]

                rebuild_doc_order = rebuildDocOrder(num_flushed_docs)

        self.doc_ordering = new_doc_ordering
        self.onFlush(flushed_docs)
        return flushed_docs

    def _addNewOrdering(self,key):
        self.doc_ordering.append(key)
        self.doc_ordering_lookup[key] = len(self.doc_ordering) - 1

    def _removeOldOrdering(self, key):
        # we set the element of doc_ordering to None instead of removing it.
        # option 1: (not used)
        #   # remove is a slow operation because it need to first find the element to remove
        #   `self.doc_ordering.remove(key)`  
        # option 2: implemented
        #   we speed up finding the element to remove by keeping a hash (doc_ordering_lookup) of 
        #   where each key is in doc_ordering. This means we cannot delete elements from doc_ordering
        #   because this would change the size of doc_ordering and invalidate the information stored
        #   within doc_ordering_lookup
        # option 3: TODO
        #   use an ordered set to abstract away the details of option 2
        ind = self.doc_ordering_lookup[key]
        self.doc_ordering[ind] = None
        self.num_empty_doc_order_recs += 1

