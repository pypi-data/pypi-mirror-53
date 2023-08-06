This notebook enhances the `pydantic.BaseModel` to provide interactive type checking of `object`s.

One of the features of `traitlets` is that it provides interactive type validation when values are set.  `pydantic` only checks the validates when the `type` is instantiated.


```python
    import pydantic
```


```python
    class X(pydantic.BaseModel): a: int
    X.schema()
```




    {'title': 'X',
     'type': 'object',
     'properties': {'a': {'title': 'A', 'type': 'integer'}},
     'required': ['a']}



Although the `type` should be an `int`, we can set a `str` `property` value.


```python
    X(a=12).a = 'asdf'
```

`pydantic` provides custom `setattr` heuristics.  The `BaseModel` below extends the `pydantic` version to require strict `type` values on the properties.


```python
    class BaseModel(pydantic.BaseModel):
        def __setattr__(self, str, value):
            data = self.dict()
            data.update({str: value})
            self.validate(data)
            return object.__setattr__(self, str, value)
```


```python
    class Y(BaseModel): a: int
    with __import__('pytest').raises(pydantic.ValidationError): 
        
        Y(a=12).a = 'asdf'
```

Numeric `str`ings are edge cases because `pydantic` serializes the `object`s.


```python
    Y(a=12).a = '10'
```
