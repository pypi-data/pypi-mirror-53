```python
    import abc, jsonschema, rdflib, collections, itertools, operator, copy, functools, pyld.jsonld as jsonld, ast, pathlib, typing
    import strict_rfc3339, rfc3986, rfc3987, IPython, toolz, builtins
```


```python
    class Schema:
        @classmethod
        def schema(cls): return {**collections.ChainMap(*(getattr(object, '__annotations__', {}) or {} for object in cls.__mro__)), 'title': cls.__name__, }
        @classmethod
        def validate(cls, object, schema=None): jsonschema.validate(object, schema or cls.schema(), format_checker=jsonschema.FormatChecker())
```


```python
    class JsonSchemaMeta(Schema, abc.ABCMeta):
        def __init_subclass__(cls, **kwargs):  cls.__annotations__ = cls.validate(kwargs) or kwargs

    class JsonSchema(JsonSchemaMeta, **jsonschema.Draft7Validator.META_SCHEMA): ...
```


```python
    def map_container(callable):
        @functools.wraps(callable)
        def logic(object, *args, **kwargs):
            if isinstance(object, (list, dict)): return object.map(callable, *args, **kwargs)
            return object.pipe(callable, *args, **kwargs)
        return logic
```


```python
class Parser:
    def text(self): return self
    def read(self): return String(pathlib.Path(self).read_text())
    def yaml(self):
        try: from ruamel import yaml
        except: import yaml
        return self.pipe(operator.methodcaller('text'), yaml.safe_load, Type.object)
    def json(self):
        try: import ujson as json
        except: import json
        return self.pipe(operator.methodcaller('text'), json.loads, Type.object)
    def __import__(self): return __import__('importlib').import_module(self)
    def git(self): return __import__('git').Repo(self)
    def download_json(self, *args, **object): return Type.object(__import__('requests').get(self, *args, **object).json())
    def download(self, *args, **object): return String.object(__import__('requests').get(self, *args, **object).text)
    def graphviz(self): return __import__('graphviz').Source(object)

for self in vars(Parser):
    if self not in dir(object) and (
        self in '__import__'.split() or not self.startswith('_')
    ): setattr(Parser, self, map_container(getattr(Parser, self)))
```


```python
    class Type(Schema, metaclass=JsonSchema): 
        __annotations__ = {}
        def __new__(cls, object=None, *args, **kwargs):
            if object is None: object = copy.copy(cls.schema().get('default'))
            return cls.validate(object) or super().__new__(cls, object, *args, **kwargs)

        def __init_subclass__(cls, **kwargs):  cls.__annotations__ = type(cls).validate(kwargs) or kwargs

        @classmethod
        def object(type, object=None):
            for cls in (type.__subclasses__()):
                try: return cls.object(object)
                except BaseException as e: ...
            else: return type(object)
            
        def pipe(self, *funcs, **kwargs): return toolz.compose(*reversed(funcs))(self, **kwargs)
        def do(self, *funcs, **kwargs): self.pipe(*funcs, **kwargs); return self
        def list(self): return List(self)
        def tuple(self): return tuple(self)
        def set(self): return set(self)
        def str(self): return String.object(self)
        def zip(self, *args): return list(zip(self, *args))
        def starmap(self, callable): return List(itertools.starmap(callable, self))
        
    class Container(Parser):
        def series(self, *args, **kwargs) -> 'pandas.Series': return __import__('pandas').Series(self, *args, **kwargs)
        def frame(self, *args, **kwargs) -> 'pandas.DataFrame': return __import__('pandas').DataFrame(self, *args, **kwargs)
        def __getitem__(self, object): return Type.object(super().__getitem__(object))
        
    class Sequence(Container):
        def map(self, callable, **kwargs): return self.pipe(toolz.partial(toolz.map, toolz.partial(callable, **kwargs)), list, List)
        def filter(self, callable, **kwargs): return self.pipe(toolz.partial(toolz.filter, toolz.partial(callable, **kwargs)), list, List)
        def reduce(self, callable, **kwargs): return self.pipe(toolz.partial(toolz.reduce, toolz.partial(callable, **kwargs)), Type.object)
        def groupby(self, callable, **kwargs): return self.pipe(toolz.partial(toolz.groupby, toolz.partial(callable, **kwargs)), Dict)
        def reduceby(self, callable, **kwargs): return self.pipe(toolz.partial(toolz.reduceby, toolz.partial(callable, **kwargs)), Dict)
```


```python
    class Dict(Type, Container, dict, type='object', default={}): 
        def map(self, value=None, key=None): return Dict({(key or toolz.identity)(k): (value or toolz.identity)(v) for k, v in self.items()})
        def filter(self, value=None, key=None): return Dict({k: v for k, v in self.items() if (
            (key(k) if key else True) and (value(v) if value else True)
        )})
        
```


```python
    class List(Type, Sequence, list, type='array', default=[]): 
        def __new__(cls, object=None, *args, **kwargs): 
            if isinstance(object, tuple): object = list(object)
            return super().__new__(cls, object, *args, **kwargs)        
```


```python
    class Null(Type, type='null'): 
        def __new__(cls, object=None, *args, **kwargs): return cls.validate(cls, object)
    class Integer(Type, int, type='integer', default=''): ...
    class Number(Type, float, type='number', default=''): ...
    
    class String(Type, Parser, str, type='string', default=''):
        def path(self) -> pathlib.Path: return pathlib.Path(self)
    
    class Date(String, format='date'): ...
    class Datetime(String, format='date-time'): ...
    class Time(String, format='time'): ...
    class Color(String, format='color'): ...
    
    class Email(String, format='email'): ...
    class Uri(String, format='uri'):         
        def text(self, *args, **object): return __import__('requests').get(self,*args, **object).text
        
    class File(String): 
        def text(self): return self.path().read_text()
        @classmethod
        def validate(cls, object, schema=None):
            if object.path().exists(): return 
            raise ValueError(F"{object} is not a file.")
    class Dir(File): 
        @classmethod
        def validate(cls, object, schema=None):
            if object.path().is_dir(): return 
            raise ValueError(F"{object} is not a file.")
```


```python
    class StringTypes(ast.NodeTransformer):
        def visit_type(self, node, type=None):
            next = ast.parse(F"""__import__('importlib').import_module('{__name__}').{type}.object('')""").body[0].value
            next.args = [node]
            return ast.copy_location(next, node)
        
        visit_JoinedStr = visit_Str = functools.partialmethod(visit_type, type='String')
        visit_DictComp = visit_Dict = functools.partialmethod(visit_type, type='Dict')
        visit_ListComp = visit_List = functools.partialmethod(visit_type, type='List')
```


```python
    def unload_ipython_extension(shell): shell.ast_transformers = [x for x in shell.ast_transformers if not isinstance(x, StringTypes)]
    def load_ipython_extension(shell): unload_ipython_extension(shell) or shell.ast_transformers.append(StringTypes())
    __name__ == '__main__' and load_ipython_extension(get_ipython())
```

    __name__ == '__main__' and "jschema.ipynb".yaml()['cells'].series().apply("pandas".imp().Series).T


```python
if __name__ == '__main__':
    __import__('requests_cache').install_cache('jschema')
    "https://api.github.com/users/tonyfast/gists".download_json().frame().T.pipe(display)
```


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
      <th>4</th>
      <th>5</th>
      <th>6</th>
      <th>7</th>
      <th>8</th>
      <th>9</th>
      <th>...</th>
      <th>20</th>
      <th>21</th>
      <th>22</th>
      <th>23</th>
      <th>24</th>
      <th>25</th>
      <th>26</th>
      <th>27</th>
      <th>28</th>
      <th>29</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>url</td>
      <td>https://api.github.com/gists/ab4f3cf987a87d574...</td>
      <td>https://api.github.com/gists/79779f89e749c72e7...</td>
      <td>https://api.github.com/gists/7b66a5d9b09c4754c...</td>
      <td>https://api.github.com/gists/306be744a71ef148d...</td>
      <td>https://api.github.com/gists/15c6ac8f005a55222...</td>
      <td>https://api.github.com/gists/4f56c72c99fdd3464...</td>
      <td>https://api.github.com/gists/e387e567cebf4ec72...</td>
      <td>https://api.github.com/gists/d845d7a63ba24aab8...</td>
      <td>https://api.github.com/gists/87562b3e76e20855a...</td>
      <td>https://api.github.com/gists/6382152537773be2f...</td>
      <td>...</td>
      <td>https://api.github.com/gists/5a0507d00a1081fad...</td>
      <td>https://api.github.com/gists/605e63deb188f6901...</td>
      <td>https://api.github.com/gists/61a17214486f1e194...</td>
      <td>https://api.github.com/gists/030c51e35e2f5e469...</td>
      <td>https://api.github.com/gists/8c278dc253179e0eb...</td>
      <td>https://api.github.com/gists/0bf98418128c7823f...</td>
      <td>https://api.github.com/gists/1447eb0077eb44e34...</td>
      <td>https://api.github.com/gists/98530c6644485022f...</td>
      <td>https://api.github.com/gists/0a06a249c8de5d236...</td>
      <td>https://api.github.com/gists/8ee0038edad9d8ab4...</td>
    </tr>
    <tr>
      <td>forks_url</td>
      <td>https://api.github.com/gists/ab4f3cf987a87d574...</td>
      <td>https://api.github.com/gists/79779f89e749c72e7...</td>
      <td>https://api.github.com/gists/7b66a5d9b09c4754c...</td>
      <td>https://api.github.com/gists/306be744a71ef148d...</td>
      <td>https://api.github.com/gists/15c6ac8f005a55222...</td>
      <td>https://api.github.com/gists/4f56c72c99fdd3464...</td>
      <td>https://api.github.com/gists/e387e567cebf4ec72...</td>
      <td>https://api.github.com/gists/d845d7a63ba24aab8...</td>
      <td>https://api.github.com/gists/87562b3e76e20855a...</td>
      <td>https://api.github.com/gists/6382152537773be2f...</td>
      <td>...</td>
      <td>https://api.github.com/gists/5a0507d00a1081fad...</td>
      <td>https://api.github.com/gists/605e63deb188f6901...</td>
      <td>https://api.github.com/gists/61a17214486f1e194...</td>
      <td>https://api.github.com/gists/030c51e35e2f5e469...</td>
      <td>https://api.github.com/gists/8c278dc253179e0eb...</td>
      <td>https://api.github.com/gists/0bf98418128c7823f...</td>
      <td>https://api.github.com/gists/1447eb0077eb44e34...</td>
      <td>https://api.github.com/gists/98530c6644485022f...</td>
      <td>https://api.github.com/gists/0a06a249c8de5d236...</td>
      <td>https://api.github.com/gists/8ee0038edad9d8ab4...</td>
    </tr>
    <tr>
      <td>commits_url</td>
      <td>https://api.github.com/gists/ab4f3cf987a87d574...</td>
      <td>https://api.github.com/gists/79779f89e749c72e7...</td>
      <td>https://api.github.com/gists/7b66a5d9b09c4754c...</td>
      <td>https://api.github.com/gists/306be744a71ef148d...</td>
      <td>https://api.github.com/gists/15c6ac8f005a55222...</td>
      <td>https://api.github.com/gists/4f56c72c99fdd3464...</td>
      <td>https://api.github.com/gists/e387e567cebf4ec72...</td>
      <td>https://api.github.com/gists/d845d7a63ba24aab8...</td>
      <td>https://api.github.com/gists/87562b3e76e20855a...</td>
      <td>https://api.github.com/gists/6382152537773be2f...</td>
      <td>...</td>
      <td>https://api.github.com/gists/5a0507d00a1081fad...</td>
      <td>https://api.github.com/gists/605e63deb188f6901...</td>
      <td>https://api.github.com/gists/61a17214486f1e194...</td>
      <td>https://api.github.com/gists/030c51e35e2f5e469...</td>
      <td>https://api.github.com/gists/8c278dc253179e0eb...</td>
      <td>https://api.github.com/gists/0bf98418128c7823f...</td>
      <td>https://api.github.com/gists/1447eb0077eb44e34...</td>
      <td>https://api.github.com/gists/98530c6644485022f...</td>
      <td>https://api.github.com/gists/0a06a249c8de5d236...</td>
      <td>https://api.github.com/gists/8ee0038edad9d8ab4...</td>
    </tr>
    <tr>
      <td>id</td>
      <td>ab4f3cf987a87d574144051e652f879a</td>
      <td>79779f89e749c72e72b6b4470b512496</td>
      <td>7b66a5d9b09c4754c4a7577242975cb1</td>
      <td>306be744a71ef148d3590118495ff644</td>
      <td>15c6ac8f005a5522291f08d95619e085</td>
      <td>4f56c72c99fdd346481a01ad27a9aaf4</td>
      <td>e387e567cebf4ec726be9f1bde6503f5</td>
      <td>d845d7a63ba24aab895a1580b8702aff</td>
      <td>87562b3e76e20855aa076bf793c8208f</td>
      <td>6382152537773be2ffc208c3d4e526c2</td>
      <td>...</td>
      <td>5a0507d00a1081fadccb158d31137d2c</td>
      <td>605e63deb188f6901a465420e9e6ce85</td>
      <td>61a17214486f1e1947707e1c65ace378</td>
      <td>030c51e35e2f5e4698d476443e98765c</td>
      <td>8c278dc253179e0ebd1b9ef96b63f51c</td>
      <td>0bf98418128c7823f8cf2ecf30bea8fa</td>
      <td>1447eb0077eb44e3452a4e3e7d311f70</td>
      <td>98530c6644485022f49545f333760916</td>
      <td>0a06a249c8de5d236d861237eda846bd</td>
      <td>8ee0038edad9d8ab438202d477f26925</td>
    </tr>
    <tr>
      <td>node_id</td>
      <td>MDQ6R2lzdGFiNGYzY2Y5ODdhODdkNTc0MTQ0MDUxZTY1Mm...</td>
      <td>MDQ6R2lzdDc5Nzc5Zjg5ZTc0OWM3MmU3MmI2YjQ0NzBiNT...</td>
      <td>MDQ6R2lzdDdiNjZhNWQ5YjA5YzQ3NTRjNGE3NTc3MjQyOT...</td>
      <td>MDQ6R2lzdDMwNmJlNzQ0YTcxZWYxNDhkMzU5MDExODQ5NW...</td>
      <td>MDQ6R2lzdDE1YzZhYzhmMDA1YTU1MjIyOTFmMDhkOTU2MT...</td>
      <td>MDQ6R2lzdDRmNTZjNzJjOTlmZGQzNDY0ODFhMDFhZDI3YT...</td>
      <td>MDQ6R2lzdGUzODdlNTY3Y2ViZjRlYzcyNmJlOWYxYmRlNj...</td>
      <td>MDQ6R2lzdGQ4NDVkN2E2M2JhMjRhYWI4OTVhMTU4MGI4Nz...</td>
      <td>MDQ6R2lzdDg3NTYyYjNlNzZlMjA4NTVhYTA3NmJmNzkzYz...</td>
      <td>MDQ6R2lzdDYzODIxNTI1Mzc3NzNiZTJmZmMyMDhjM2Q0ZT...</td>
      <td>...</td>
      <td>MDQ6R2lzdDVhMDUwN2QwMGExMDgxZmFkY2NiMTU4ZDMxMT...</td>
      <td>MDQ6R2lzdDYwNWU2M2RlYjE4OGY2OTAxYTQ2NTQyMGU5ZT...</td>
      <td>MDQ6R2lzdDYxYTE3MjE0NDg2ZjFlMTk0NzcwN2UxYzY1YW...</td>
      <td>MDQ6R2lzdDAzMGM1MWUzNWUyZjVlNDY5OGQ0NzY0NDNlOT...</td>
      <td>MDQ6R2lzdDhjMjc4ZGMyNTMxNzllMGViZDFiOWVmOTZiNj...</td>
      <td>MDQ6R2lzdDBiZjk4NDE4MTI4Yzc4MjNmOGNmMmVjZjMwYm...</td>
      <td>MDQ6R2lzdDE0NDdlYjAwNzdlYjQ0ZTM0NTJhNGUzZTdkMz...</td>
      <td>MDQ6R2lzdDk4NTMwYzY2NDQ0ODUwMjJmNDk1NDVmMzMzNz...</td>
      <td>MDQ6R2lzdDBhMDZhMjQ5YzhkZTVkMjM2ZDg2MTIzN2VkYT...</td>
      <td>MDQ6R2lzdDhlZTAwMzhlZGFkOWQ4YWI0MzgyMDJkNDc3Zj...</td>
    </tr>
    <tr>
      <td>git_pull_url</td>
      <td>https://gist.github.com/ab4f3cf987a87d57414405...</td>
      <td>https://gist.github.com/79779f89e749c72e72b6b4...</td>
      <td>https://gist.github.com/7b66a5d9b09c4754c4a757...</td>
      <td>https://gist.github.com/306be744a71ef148d35901...</td>
      <td>https://gist.github.com/15c6ac8f005a5522291f08...</td>
      <td>https://gist.github.com/4f56c72c99fdd346481a01...</td>
      <td>https://gist.github.com/e387e567cebf4ec726be9f...</td>
      <td>https://gist.github.com/d845d7a63ba24aab895a15...</td>
      <td>https://gist.github.com/87562b3e76e20855aa076b...</td>
      <td>https://gist.github.com/6382152537773be2ffc208...</td>
      <td>...</td>
      <td>https://gist.github.com/5a0507d00a1081fadccb15...</td>
      <td>https://gist.github.com/605e63deb188f6901a4654...</td>
      <td>https://gist.github.com/61a17214486f1e1947707e...</td>
      <td>https://gist.github.com/030c51e35e2f5e4698d476...</td>
      <td>https://gist.github.com/8c278dc253179e0ebd1b9e...</td>
      <td>https://gist.github.com/0bf98418128c7823f8cf2e...</td>
      <td>https://gist.github.com/1447eb0077eb44e3452a4e...</td>
      <td>https://gist.github.com/98530c6644485022f49545...</td>
      <td>https://gist.github.com/0a06a249c8de5d236d8612...</td>
      <td>https://gist.github.com/8ee0038edad9d8ab438202...</td>
    </tr>
    <tr>
      <td>git_push_url</td>
      <td>https://gist.github.com/ab4f3cf987a87d57414405...</td>
      <td>https://gist.github.com/79779f89e749c72e72b6b4...</td>
      <td>https://gist.github.com/7b66a5d9b09c4754c4a757...</td>
      <td>https://gist.github.com/306be744a71ef148d35901...</td>
      <td>https://gist.github.com/15c6ac8f005a5522291f08...</td>
      <td>https://gist.github.com/4f56c72c99fdd346481a01...</td>
      <td>https://gist.github.com/e387e567cebf4ec726be9f...</td>
      <td>https://gist.github.com/d845d7a63ba24aab895a15...</td>
      <td>https://gist.github.com/87562b3e76e20855aa076b...</td>
      <td>https://gist.github.com/6382152537773be2ffc208...</td>
      <td>...</td>
      <td>https://gist.github.com/5a0507d00a1081fadccb15...</td>
      <td>https://gist.github.com/605e63deb188f6901a4654...</td>
      <td>https://gist.github.com/61a17214486f1e1947707e...</td>
      <td>https://gist.github.com/030c51e35e2f5e4698d476...</td>
      <td>https://gist.github.com/8c278dc253179e0ebd1b9e...</td>
      <td>https://gist.github.com/0bf98418128c7823f8cf2e...</td>
      <td>https://gist.github.com/1447eb0077eb44e3452a4e...</td>
      <td>https://gist.github.com/98530c6644485022f49545...</td>
      <td>https://gist.github.com/0a06a249c8de5d236d8612...</td>
      <td>https://gist.github.com/8ee0038edad9d8ab438202...</td>
    </tr>
    <tr>
      <td>html_url</td>
      <td>https://gist.github.com/ab4f3cf987a87d57414405...</td>
      <td>https://gist.github.com/79779f89e749c72e72b6b4...</td>
      <td>https://gist.github.com/7b66a5d9b09c4754c4a757...</td>
      <td>https://gist.github.com/306be744a71ef148d35901...</td>
      <td>https://gist.github.com/15c6ac8f005a5522291f08...</td>
      <td>https://gist.github.com/4f56c72c99fdd346481a01...</td>
      <td>https://gist.github.com/e387e567cebf4ec726be9f...</td>
      <td>https://gist.github.com/d845d7a63ba24aab895a15...</td>
      <td>https://gist.github.com/87562b3e76e20855aa076b...</td>
      <td>https://gist.github.com/6382152537773be2ffc208...</td>
      <td>...</td>
      <td>https://gist.github.com/5a0507d00a1081fadccb15...</td>
      <td>https://gist.github.com/605e63deb188f6901a4654...</td>
      <td>https://gist.github.com/61a17214486f1e1947707e...</td>
      <td>https://gist.github.com/030c51e35e2f5e4698d476...</td>
      <td>https://gist.github.com/8c278dc253179e0ebd1b9e...</td>
      <td>https://gist.github.com/0bf98418128c7823f8cf2e...</td>
      <td>https://gist.github.com/1447eb0077eb44e3452a4e...</td>
      <td>https://gist.github.com/98530c6644485022f49545...</td>
      <td>https://gist.github.com/0a06a249c8de5d236d8612...</td>
      <td>https://gist.github.com/8ee0038edad9d8ab438202...</td>
    </tr>
    <tr>
      <td>files</td>
      <td>{'2019-09-26-pandas-apply-series.ipynb': {'fil...</td>
      <td>{'2019-09-25-nasa-weather-events.ipynb': {'fil...</td>
      <td>{'2019-09-25-notebook-documents.ipynb': {'file...</td>
      <td>{'2019-09-24-.ipynb': {'filename': '2019-09-24...</td>
      <td>{'2019-09-24-importnb.ipynb': {'filename': '20...</td>
      <td>{'requirements.txt': {'filename': 'requirement...</td>
      <td>{'__init__.py': {'filename': '__init__.py', 't...</td>
      <td>{'pydantic_dataclass_cli.ipynb': {'filename': ...</td>
      <td>{'pandas-jam-session.ipynb': {'filename': 'pan...</td>
      <td>{'__init__.py': {'filename': '__init__.py', 't...</td>
      <td>...</td>
      <td>{'requirements.txt': {'filename': 'requirement...</td>
      <td>{'chris-ml-study-hall.ipynb': {'filename': 'ch...</td>
      <td>{'requirements.txt': {'filename': 'requirement...</td>
      <td>{'functors.ipynb': {'filename': 'functors.ipyn...</td>
      <td>{'x.py': {'filename': 'x.py', 'type': 'applica...</td>
      <td>{'requirements.txt': {'filename': 'requirement...</td>
      <td>{'rdf_type_system.ipynb': {'filename': 'rdf_ty...</td>
      <td>{'requirements.txt': {'filename': 'requirement...</td>
      <td>{'requirements.txt': {'filename': 'requirement...</td>
      <td>{'shema_org_python_types.ipynb': {'filename': ...</td>
    </tr>
    <tr>
      <td>public</td>
      <td>True</td>
      <td>True</td>
      <td>True</td>
      <td>True</td>
      <td>True</td>
      <td>True</td>
      <td>True</td>
      <td>True</td>
      <td>True</td>
      <td>True</td>
      <td>...</td>
      <td>True</td>
      <td>True</td>
      <td>True</td>
      <td>True</td>
      <td>True</td>
      <td>True</td>
      <td>True</td>
      <td>True</td>
      <td>True</td>
      <td>True</td>
    </tr>
    <tr>
      <td>created_at</td>
      <td>2019-09-26T15:00:43Z</td>
      <td>2019-09-26T03:14:57Z</td>
      <td>2019-09-25T15:13:00Z</td>
      <td>2019-09-25T03:01:51Z</td>
      <td>2019-09-24T14:24:46Z</td>
      <td>2019-09-23T15:24:21Z</td>
      <td>2019-09-23T13:24:26Z</td>
      <td>2019-09-22T16:46:13Z</td>
      <td>2019-09-18T15:44:38Z</td>
      <td>2019-09-15T17:29:37Z</td>
      <td>...</td>
      <td>2019-08-29T16:07:21Z</td>
      <td>2019-08-28T22:37:25Z</td>
      <td>2019-08-27T16:24:18Z</td>
      <td>2019-08-27T14:10:20Z</td>
      <td>2019-08-26T02:25:43Z</td>
      <td>2019-08-23T19:12:58Z</td>
      <td>2019-08-22T03:45:11Z</td>
      <td>2019-08-20T04:42:33Z</td>
      <td>2019-08-17T02:44:08Z</td>
      <td>2019-08-15T22:16:11Z</td>
    </tr>
    <tr>
      <td>updated_at</td>
      <td>2019-09-26T15:00:43Z</td>
      <td>2019-09-26T15:52:45Z</td>
      <td>2019-09-26T16:55:02Z</td>
      <td>2019-09-25T03:07:15Z</td>
      <td>2019-09-24T15:59:18Z</td>
      <td>2019-09-23T15:44:58Z</td>
      <td>2019-09-23T15:21:52Z</td>
      <td>2019-09-22T17:06:46Z</td>
      <td>2019-09-18T15:44:40Z</td>
      <td>2019-09-20T13:23:42Z</td>
      <td>...</td>
      <td>2019-08-30T16:23:15Z</td>
      <td>2019-08-29T05:58:20Z</td>
      <td>2019-08-27T16:26:21Z</td>
      <td>2019-09-03T04:51:45Z</td>
      <td>2019-08-26T02:25:43Z</td>
      <td>2019-08-23T19:13:30Z</td>
      <td>2019-08-22T13:19:09Z</td>
      <td>2019-08-20T04:46:24Z</td>
      <td>2019-09-04T15:46:02Z</td>
      <td>2019-08-15T23:06:13Z</td>
    </tr>
    <tr>
      <td>description</td>
      <td></td>
      <td>Run this code on my binder https://mybinder.or...</td>
      <td>A discourse on the form of computational noteb...</td>
      <td></td>
      <td>Why importnb⁇ https://mybinder.org/v2/gist/ton...</td>
      <td>Tests for tonyfast's blog: https://mybinder.or...</td>
      <td>Create interactive widgets for functions when ...</td>
      <td>Essays on high level pydantic usage.</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>https://mybinder.org/v2/gist/tonyfast/5a0507d0...</td>
      <td>https://mybinder.org/v2/gist/tonyfast/605e63de...</td>
      <td>Define and validate schema.org structured data...</td>
      <td>https://mybinder.org/v2/gist/tonyfast/030c51e3...</td>
      <td>A closed namespace for schema.org https://sche...</td>
      <td>Unembed widget json into python</td>
      <td>https://mybinder.org/v2/gist/tonyfast/1447eb00...</td>
      <td>Turn rdf graphs into pandas dataframes https:/...</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>comments</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <td>user</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <td>comments_url</td>
      <td>https://api.github.com/gists/ab4f3cf987a87d574...</td>
      <td>https://api.github.com/gists/79779f89e749c72e7...</td>
      <td>https://api.github.com/gists/7b66a5d9b09c4754c...</td>
      <td>https://api.github.com/gists/306be744a71ef148d...</td>
      <td>https://api.github.com/gists/15c6ac8f005a55222...</td>
      <td>https://api.github.com/gists/4f56c72c99fdd3464...</td>
      <td>https://api.github.com/gists/e387e567cebf4ec72...</td>
      <td>https://api.github.com/gists/d845d7a63ba24aab8...</td>
      <td>https://api.github.com/gists/87562b3e76e20855a...</td>
      <td>https://api.github.com/gists/6382152537773be2f...</td>
      <td>...</td>
      <td>https://api.github.com/gists/5a0507d00a1081fad...</td>
      <td>https://api.github.com/gists/605e63deb188f6901...</td>
      <td>https://api.github.com/gists/61a17214486f1e194...</td>
      <td>https://api.github.com/gists/030c51e35e2f5e469...</td>
      <td>https://api.github.com/gists/8c278dc253179e0eb...</td>
      <td>https://api.github.com/gists/0bf98418128c7823f...</td>
      <td>https://api.github.com/gists/1447eb0077eb44e34...</td>
      <td>https://api.github.com/gists/98530c6644485022f...</td>
      <td>https://api.github.com/gists/0a06a249c8de5d236...</td>
      <td>https://api.github.com/gists/8ee0038edad9d8ab4...</td>
    </tr>
    <tr>
      <td>owner</td>
      <td>{'login': 'tonyfast', 'id': 4236275, 'node_id'...</td>
      <td>{'login': 'tonyfast', 'id': 4236275, 'node_id'...</td>
      <td>{'login': 'tonyfast', 'id': 4236275, 'node_id'...</td>
      <td>{'login': 'tonyfast', 'id': 4236275, 'node_id'...</td>
      <td>{'login': 'tonyfast', 'id': 4236275, 'node_id'...</td>
      <td>{'login': 'tonyfast', 'id': 4236275, 'node_id'...</td>
      <td>{'login': 'tonyfast', 'id': 4236275, 'node_id'...</td>
      <td>{'login': 'tonyfast', 'id': 4236275, 'node_id'...</td>
      <td>{'login': 'tonyfast', 'id': 4236275, 'node_id'...</td>
      <td>{'login': 'tonyfast', 'id': 4236275, 'node_id'...</td>
      <td>...</td>
      <td>{'login': 'tonyfast', 'id': 4236275, 'node_id'...</td>
      <td>{'login': 'tonyfast', 'id': 4236275, 'node_id'...</td>
      <td>{'login': 'tonyfast', 'id': 4236275, 'node_id'...</td>
      <td>{'login': 'tonyfast', 'id': 4236275, 'node_id'...</td>
      <td>{'login': 'tonyfast', 'id': 4236275, 'node_id'...</td>
      <td>{'login': 'tonyfast', 'id': 4236275, 'node_id'...</td>
      <td>{'login': 'tonyfast', 'id': 4236275, 'node_id'...</td>
      <td>{'login': 'tonyfast', 'id': 4236275, 'node_id'...</td>
      <td>{'login': 'tonyfast', 'id': 4236275, 'node_id'...</td>
      <td>{'login': 'tonyfast', 'id': 4236275, 'node_id'...</td>
    </tr>
    <tr>
      <td>truncated</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>...</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
    </tr>
  </tbody>
</table>
<p>18 rows × 30 columns</p>
</div>



```python
[*range(10)].filter(lambda x: x%2).map(chr)
```


    ---------------------------------------------------------------------------

    ValidationError                           Traceback (most recent call last)

    <ipython-input-14-166614df768d> in <module>
    ----> 1 [*range(10)].filter(lambda x: x%2).map(chr)
    

    <ipython-input-6-0d5a3c10f685> in filter(self, callable, **kwargs)
         30 class Sequence(Container):
         31     def map(self, callable, **kwargs): return self.pipe(toolz.partial(toolz.map, toolz.partial(callable, **kwargs)), List)
    ---> 32     def filter(self, callable, **kwargs): return self.pipe(toolz.partial(toolz.filter, toolz.partial(callable, **kwargs)), List)
         33     def reduce(self, callable, **kwargs): return self.pipe(toolz.partial(toolz.reduce, toolz.partial(callable, **kwargs)), Type.object)
         34     def groupby(self, callable, **kwargs): return self.pipe(toolz.partial(toolz.groupby, toolz.partial(callable, **kwargs)), Dict)


    <ipython-input-6-0d5a3c10f685> in pipe(self, *funcs, **kwargs)
         14         else: return type(object)
         15 
    ---> 16     def pipe(self, *funcs, **kwargs): return toolz.compose(*reversed(funcs))(self, **kwargs)
         17     def do(self, *funcs, **kwargs): self.pipe(*funcs, **kwargs); return self
         18     def list(self): return List(self)


    ~/anaconda3/lib/python3.7/site-packages/toolz/functoolz.py in __call__(self, *args, **kwargs)
        486         ret = self.first(*args, **kwargs)
        487         for f in self.funcs:
    --> 488             ret = f(ret)
        489         return ret
        490 


    <ipython-input-8-c06806cb1a17> in __new__(cls, object, *args, **kwargs)
          2     def __new__(cls, object=None, *args, **kwargs):
          3         if isinstance(object, tuple): object = list(object)
    ----> 4         return super().__new__(cls, object, *args, **kwargs)
    

    <ipython-input-6-0d5a3c10f685> in __new__(cls, object, *args, **kwargs)
          3     def __new__(cls, object=None, *args, **kwargs):
          4         if object is None: object = copy.copy(cls.schema().get('default'))
    ----> 5         return cls.validate(object) or super().__new__(cls, object, *args, **kwargs)
          6 
          7     def __init_subclass__(cls, **kwargs):  cls.__annotations__ = type(cls).validate(kwargs) or kwargs


    <ipython-input-2-2bf8b0375eea> in validate(cls, object, schema)
          3     def schema(cls): return {**collections.ChainMap(*(getattr(object, '__annotations__', {}) or {} for object in cls.__mro__)), 'title': cls.__name__, }
          4     @classmethod
    ----> 5     def validate(cls, object, schema=None): jsonschema.validate(object, schema or cls.schema(), format_checker=jsonschema.FormatChecker())
    

    ~/anaconda3/lib/python3.7/site-packages/jsonschema/validators.py in validate(instance, schema, cls, *args, **kwargs)
        897     error = exceptions.best_match(validator.iter_errors(instance))
        898     if error is not None:
    --> 899         raise error
        900 
        901 


    ValidationError: <filter object at 0x108538c50> is not of type 'array'
    
    Failed validating 'type' in schema:
        {'default': [], 'title': 'List', 'type': 'array'}
    
    On instance:
        <filter object at 0x108538c50>



```python

```
