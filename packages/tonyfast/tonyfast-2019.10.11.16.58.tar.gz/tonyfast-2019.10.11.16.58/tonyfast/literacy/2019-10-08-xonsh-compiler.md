```python
    import xonsh.main, xonsh.execer, IPython, ast
    execer = xonsh.execer.Execer()
    class CachingCompiler(IPython.core.compilerop.CachingCompiler):
        def ast_parse(self, source, filename='<unknown>', symbol='exec'): 
            return globals()['execer']._parse_ctx_free(source + "\n", symbol, filename)[0] or ast.Module([])
```


```python
    def load_ipython_extension(shell): 
        if not hasattr(__import__('builtins'), '__xonsh__'):
            with xonsh.main.main_context('-i'.split()): ...
        shell.compile = CachingCompiler()

    def unload_ipython_extension(shell): shell.compile = IPython.core.compilerop.CachingCompiler
    __name__ == '__main__' and load_ipython_extension(get_ipython())
```
