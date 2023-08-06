```python
    with __import__('importnb').Notebook():
        try:
            from . import rdflib_patch
        except:
            import rdflib_patch
    import rdflib, pandas, pydantic, jsonschema, json, abc, networkx, itertools, dataclasses, requests, typing, collections, requests_cache, inspect, IPython, pyld.jsonld as jsonld, abc
    from toolz.curried import *; from rdflib.namespace import OWL, RDF, RDFS, SKOS, DC, DCTERMS
    requests_cache.install_cache('rdf')
    __all__ = tuple("Graph CC RDFS HYDRA OWL XHTML RDF XS XSD SW".split())

    SCHEMA = rdflib.Namespace('http://schema.org/')
```


```python
if 'field_class_to_schema_enum_enabled' not in globals(): field_class_to_schema_enum_enabled = pydantic.schema.field_class_to_schema_enum_enabled
```

Meta classes hold linked data types in their annotations.

The class of the meta class stores the python type annotations.


```python
def split(object): ns, sep, pointer = object.rpartition('/#'['#' in object]); return ns+sep, pointer
```

Load in a bunch of namespaces.


```python
class Namespace(rdflib.namespace.ClosedNamespace):
    def __getattr__(_, name):
        object = super().__getattr__(name)
        return self.new(object)

class Graph(rdflib.ConjunctiveGraph):
    types = {}
    CC: rdflib.term.URIRef('http://creativecommons.org/ns#')
    RDFS: rdflib.term.URIRef('http://www.w3.org/2000/01/rdf-schema#')
    HYDRA: rdflib.term.URIRef('http://www.w3.org/ns/hydra/core#')
    OWL: rdflib.term.URIRef('http://www.w3.org/2002/07/owl#')
    XHTML: rdflib.term.URIRef('http://www.w3.org/1999/xhtml/vocab#')
    RDF: rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
    XSD: rdflib.term.URIRef('http://www.w3.org/2001/XMLSchema#')
    XS: rdflib.term.URIRef('http://www.w3.org/2001/XMLSchema-datatypes#')
    SW: rdflib.term.URIRef('http://www.w3.org/2003/06/sw-vocab-status/ns#')
    SCHEMA: rdflib.term.URIRef('http://schema.org/')
    PROV: rdflib.term.URIRef('http://www.w3.org/ns/prov#')
    DCAT: rdflib.term.URIRef('http://www.w3.org/ns/dcat#')
    QUDT: rdflib.term.URIRef('http://qudt.org/schema/qudt#')
    
    def get(self, object, format=None):
        if format in {'json-ld'}: object = pipe(object, requests.get, requests.Response.json, jsonld.expand, json.dumps)
        else: object = requests.get(str(object)).text
        self.parse(data=object, format=format); self.update()
        return self
    
    def update(self): pipe(
        self, concat, filter(flip(isinstance)(rdflib.URIRef)), filter(flip(str.startswith)('http')),                      
        set, groupby(compose(first, split)), valmap(
            compose(list, map(compose(second, split)))
        ), itemmap(lambda x: (rdflib.URIRef(x[0]), Namespace(*x))), 
        keymap(pipe(self.__annotations__, itemmap(reversed), dict).get), keyfilter(flip(isinstance)(str)),
        itemmap(do(lambda x: setattr(self, *x)))
    ); return self
    
    def enrich(self, type):
        if type not in self.types: 
            subject = self[type]
            object = self[:, :, type]
            __annotations__ = {}
            bases = pipe(subject, filter(compose({RDFS.subPropertyOf, RDFS.subClassOf, RDF.type}.__contains__, first)), map(last), map(self.enrich), set, tuple) or (self.enrich(RDFS.Resource),)
            __context__ = pipe(self[:, RDFS.domain, type] + self[:, SCHEMA.domainIncludes, type], map(juxt(compose(second, split), identity)), dict)
            self.types[type] = __import__('builtins').type(second(split(type)), tuple(sorted(bases, key=lambda x: list(self.types).index(x.type), reverse=True)), {
            '__doc__': ''.join(self[type, RDFS.comment]), **locals()})
            self.types[type].__context__ = pipe(self.types[type], inspect.getmro, map(lambda x: getattr(x, '__context__', {})), lambda x: collections.ChainMap(*x), dict)        
        return self.types[type]
    
    def new(self, type):  
        if type not in self.types: self.enrich(type); self.annotate(); 
        return self.types[type]
    
    def annotate(self):
        """Add type annotations from the context."""
        for cls in list(self.types.values()):
            if not hasattr(cls, '__annotations__'): cls.__annotations__ = {}
            pipe(cls.__context__, 
                 valmap(lambda x: self[x, RDFS.range] + self[x, SCHEMA.rangeIncludes]), valmap(map(self.enrich)), valmap(tuple), valmap((str,).__add__), 
                 valmap(typing.Union.__getitem__), valmap(lambda x: typing.Union[x, typing.List[x]]),
                 cls.__annotations__.update)
            cls.__annotations__ = {'value': cls.__annotations__.pop('value'), **cls.__annotations__, }
            for x in cls.__annotations__: setattr(cls, x, getattr(cls, x, None))
            excepts(BaseException, pydantic.dataclasses.dataclass)(cls)

```


```python
self = (
    Graph().get(rdflib.namespace.RDF, 'ttl')
    .get(rdflib.namespace.RDFS, 'ttl')
    .get(rdflib.namespace.OWL, 'ttl')
    .get('https://www.w3.org/ns/prov.ttl', 'ttl')
    .get('https://raw.githubusercontent.com/AKSW/RDB2RDF-Seminar/master/sparqlmap/eclipse/workspace/xturtle.core/xsd.ttl', 'ttl')
    .get('https://www.w3.org/ns/hydra/core', 'json-ld')
    .get('http://www.w3.org/2003/06/sw-vocab-status/ns#', 'xml')
    .get('http://schema.org/version/latest/schema.ttl', 'ttl')
    .get('https://w3c.github.io/dxwg/dcat/rdf/dcat.ttl', 'ttl')
    .get('https://creativecommons.org/schema.rdf', 'xml')
    .get('http://qudt.org/2.0/schema/qudt', 'ttl')
    .get('http://www.linkedmodel.org/schema/vaem', 'xml')   
    .get('http://qudt.org/1.1/schema/dimension', 'xml')
    .get('http://qudt.org/1.1/schema/quantity', 'xml')
    .get('http://www.linkedmodel.org/1.0/schema/dtype', 'xml')
)
```


```python
class WebType:
    @classmethod
    def schema(cls): return cls.__pydantic_model__.schema(cls)

    def __get_validators__():
        """[custom types]: https://pydantic-docs.helpmanual.io/#custom-data-types"""
        return []
    
    def dict(self, **ctx):
        object = {'@context': ctx, **{
            k: v.dict(**(ctx and v.__context__ or {})) if isinstance(v, WebType) else v
            for k, v in [(x, getattr(self, x)) for x in self.__context__ if getattr(self, x, None) is not None]}}
        for k, v in object.items():
            try: object['@context'][k] = jsonschema.validate(v, {'anyOf': [{'type': 'string', 'format': 'uri'}, {'type': 'string', 'format': 'json-pointer'}]}, format_checker=jsonschema.draft7_format_checker) or {'@type': '@id', '@id': object['@context'][k]}
            except jsonschema.ValidationError: ...
        return object
    
    def metadata(self): return jsonld.expand(self.dict(**self.__context__))
```


```python
self.types[RDFS.Resource] = type(second(split(RDFS.Resource)), (WebType,), {
    '__doc__': ''.join(self[RDFS.Resource, RDFS.comment]), '__context__': pipe(
        self[:, RDFS.domain, RDFS.Resource],
        map(juxt(compose(second, split), identity)), dict
    ), 'type': RDFS.Resource, 'subject': self[RDFS.Resource], 'object': self[:, :, RDFS.Resource]
})
self.types[RDFS.Class] = type(second(split(RDFS.Class)), (self.types[RDFS.Resource],), {
    '__doc__': ''.join(self[RDFS.Class, RDFS.comment]), '__context__': pipe(
        self[:, RDFS.domain, RDFS.Class],
        map(juxt(compose(second, split), identity)), dict
    ), 'type': RDFS.Class, 'subject': self[RDFS.Class], 'object': self[:, :, RDFS.Class]
})
self.annotate()
```


```python
if 'field_class_to_schema_enum_enabled' not in globals(): field_class_to_schema_enum_enabled = pydantic.schema.field_class_to_schema_enum_enabled
pydantic.schema.field_class_to_schema_enum_enabled = ((self.RDFS.Resource, {}),) + field_class_to_schema_enum_enabled
```
