Automatically generate interactive widgets for functions.


```python
    import ipywidgets, types, inspect, IPython, abc, hypothesis
```


```python
    @staticmethod
    def patch_single_value(o):
        object = widget_from_single_value(o) 
        strategy = __import__('hypothesis').strategies.from_type(o).wrapped_strategy
        object = ipywidgets.interactive.widget_from_iterable([strategy.example() for x in range(20)])
        return object
```


```python
    if 'widget_from_single_value' not in globals(): widget_from_single_value = ipywidgets.interactive.widget_from_single_value
    ipywidgets.interactive.widget_from_single_value = patch_single_value
```


```python
    @type
    def Function(): ...
    manager = {}
```


```python
    def wrap(function):
        def wrapped(*args, **kwargs):
            object = function(*args, **kwargs)
            object and print(object)
        wrapped.__signature__ = inspect.signature(function)
        return wrapped
```


```python
    def display_function_interactive(function):
        global manager
        print(function)
        if function.__annotations__:
            key = getattr(function, '__name__', str(function))
            if key in manager: manager.pop(key).close()
            try:
                manager[key] = ipywidgets.interactive(wrap(function))
                IPython.display.display(manager[key])
            except ValueError: ...
        return None
```


```python
    def unload_ipython_extension(shell):
        shell.display_formatter.ipython_display_formatter.type_printers.pop(Function, None)
    def load_ipython_extension(shell):
        unload_ipython_extension(shell)
        shell.display_formatter.ipython_display_formatter.for_type(Function, display_function_interactive)
    __name__ == '__main__' and load_ipython_extension(get_ipython())
```
