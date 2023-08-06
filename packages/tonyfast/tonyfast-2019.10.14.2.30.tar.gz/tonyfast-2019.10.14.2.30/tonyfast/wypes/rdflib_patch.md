```python
    import rdflib, functools
```


```python
    @functools.partial(setattr, rdflib.Graph, '__getitem__')
    def _(self, object):
        if not isinstance(object, tuple): object = object,
        while len(object) < 3: object += slice(None),
        object = slice(*object)
        if object.start != slice(None):
            if object.stop != slice(None): return list(self.objects(object.start, object.stop))
            if object.step != slice(None): return list(self.predicates(object.start, object.stop))
            return list(self.predicate_objects(object.start))
        if object.stop != slice(None):
            if object.step != slice(None): return list(self.subjects(object.stop, object.step))
            return list(self.subject_objects(object.stop))
        return list(self.subject_predicates(object.step))           
```


```python
    @functools.partial(setattr, rdflib.namespace.ClosedNamespace, '__dir__')
    def _(self): return super(rdflib.namespace.ClosedNamespace, self).__dir__() + list(getattr(self, '_ClosedNamespace__uris'))
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-1-eb2086d40d17> in <module>
    ----> 1 @functools.partial(setattr, rdflib.namespace.ClosedNamespace, '__dir__')
          2 def _(self): return super(rdflib.namespace.ClosedNamespace, self).__dir__() + list(getattr(SCHEMA, '_ClosedNamespace__uris'))


    NameError: name 'functools' is not defined



```python

```
