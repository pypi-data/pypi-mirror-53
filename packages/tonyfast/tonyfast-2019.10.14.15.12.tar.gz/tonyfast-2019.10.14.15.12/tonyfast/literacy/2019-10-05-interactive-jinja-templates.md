Allowing code cells to accept Markdown requires different display behavior.  An important feature of computational documents is the real data can be included within a narrative.  In this document,  we add the ability to template Markdown with `jinja2`.  We'll observe value changes and update the display with `traitlets`.


```python
    import nbconvert, htmlmin, collections, jinja2.meta, IPython, sys, traitlets
    with __import__('importnb').Notebook():
        try: from . import __interactive_markdown_cells
        except: import __interactive_markdown_cells

```

Observable is singleton that manages the changes to the `jinja2` templates.


```python
    class Observable(traitlets.config.SingletonConfigurable):
        parent = IPython.get_ipython()
        def _post_execute(self): 
            with self.hold_trait_notifications():
                for trait in self.traits():
                    if trait not in self._config_traits and trait in self.parent.user_ns:
                        if getattr(self, trait, None) is not self.parent.user_ns.get(trait, None): setattr(self, trait, self.parent.user_ns.get(trait, None))

        _config_traits = set(traitlets.config.SingletonConfigurable().traits())
    
```

Donald Knuth referred to the presentation of literate code as `"Weaving"` which we derive our main `Weave` `type` from.


```python
    class Weave(traitlets.config.SingletonConfigurable):
        environment = nbconvert.TemplateExporter().environment
        parent = IPython.get_ipython()
        observable = Observable.instance()
        
        def post_run_cell(self, result): 
            if result.info.raw_cell.splitlines()[0].strip() not in {'', ';'}: 
                self.log.error(result.info.raw_cell)
                self.format(result.info.raw_cell)  
                
        def finalize(self, object):
            if isinstance(object, str):  
                object = self.parent.user_ns.get(object, object)
                if isinstance(object, str): return object
                
            known = dispatch_extras(object)
            if known: return known
                
            bundle, metadata = self.parent.display_formatter.format(object)
            for type in reversed(self.parent.display_formatter.active_types):
                if type in bundle: 
                    object = bundle[type]
                    if type.startswith('image') and ('svg' not in type):  object = _format_images(type, bundle)
                    if type == 'text/latex': 
                        if object.startswith('$$') and object.endswith('$$'): object = object[1:-1]
                    if type =='text/html': object = htmlmin.minify(object, remove_empty_space=True)
                    break
            return object
                
        def format(self, source, **k):
            if source in self.parent.user_ns and isinstance(self.parent.user_ns.get(source), str):
                source = self.parent.user_ns.get(source)
            self.environment.filters.update({k: v for k, v in self.parent.user_ns.items() if callable(v)})            
            source, metadata = front_matter(source)
            
            def update(change=None, init=False):
                nonlocal source, self, display_id, template, k, metadata
                object = template.render(**collections.ChainMap(k, metadata, self.parent.user_ns, self.parent.user_ns.get('__annotations__', {}), vars(__import__('builtins'))))
                if len(object.splitlines()) == 1 and object.startswith('http'): 
                    data = {'text/html': IPython.display.IFrame(object, '100%', 600)._repr_html_(), 'text/plain': object}
                elif object in self.parent.user_ns: 
                    data = self.display_formatter.format(self.parent.user_ns[object])[0]
                else: data = {'text/markdown': object, 'text/plain': source,}
                getattr(display_id, init and 'display' or 'update')(data, metadata=metadata, raw=True)
                
            template, display_id = self.environment.overlay(finalize=self.finalize).from_string(source), IPython.display.DisplayHandle()
            update(init=True)
            
            undeclared = jinja2.meta.find_undeclared_variables(template.environment.parse(source))
            for key in list(undeclared): 
                if isinstance(self.parent.user_ns.get(key, None), __import__('types').ModuleType):
                    undeclared.remove(key)
            if undeclared:
                for var in undeclared: self.observable.has_trait(var) or self.observable.add_traits(**{var: traitlets.Any()})
                self.observable.observe(update, undeclared)
```

`IPython` extension


```python
    def unload_ipython_extension(shell):
        try: Observable.instance().parent.events.unregister('post_execute', Observable.instance()._post_execute)
        except: ...
        try: shell.events.unregister('post_run_cell', Weave.instance().post_run_cell)
        except ValueError: ...
    def load_ipython_extension(shell):
        unload_ipython_extension(shell)
        shell.events.register('post_execute', Observable.instance()._post_execute)
        shell.events.register('post_run_cell', Weave.instance().post_run_cell)
```


```python
    def dispatch_extras(object):
        if 'matplotlib' in sys.modules:
            import matplotlib
            try:
                if isinstance(object, (matplotlib.figure.Axes, matplotlib.figure.Figure, getattr(matplotlib.axes._subplots, 'AxesSubplot', type))): return _show_axes(object)
            except: ...

        if 'sympy.plotting' in sys.modules:
            from sympy.plotting.plot import Plot
            if isinstance(object, Plot): return _show_sympy_axes(object)
```


```python
    def import_yaml():
        try: from ruamel import yaml
        except: 
            try: import yaml
            except:...
        return yaml

    def front_matter(source):
        try:
            if source.startswith('---\n') and (source.rindex('\n---\n')):
                data, sep, rest = source.lstrip('-').partition('\n---\n')
                data = import_yaml().safe_load(__import__('io').StringIO(data))
                if isinstance(data, dict): return rest, data
        except ValueError: ...
        return source, {}
```


```python
    def _show_axes(object):
        import matplotlib.backends.backend_svg; bytes = __import__('io').BytesIO()
        matplotlib.backends.backend_agg.FigureCanvasAgg(getattr(object, 'figure', object)).print_png(bytes)
        try: return _format_bytes(bytes.getvalue(), object)
        finally: matplotlib.pyplot.clf()

    def _show_sympy_axes(object): 
        bytes = __import__('io').BytesIO()
        object.save(bytes)
        try: return _format_bytes(bytes.getvalue(), object)
        finally: __import__('matplotlib').pyplot.clf()

    def _format_bytes(bytes, object): return _format_images('image/png', {'image/png': bytes})

    def _format_images(type, bundle):
        str = bundle[type]        
        if isinstance(str, bytes): str = __import__('base64').b64encode(str).decode('utf-8')
        if type in ('image/svg+xml', 'text/html'):  ...
        elif str.startswith('http'): str = F"""<img src="{str}"/>"""
        else: str = F"""<img src="data:{type};base64,{str}"/>"""
        return str
```


```python
    __name__ == '__main__' and load_ipython_extension(get_ipython())
```


    __name__ == '__main__' and load_ipython_extension(get_ipython())

