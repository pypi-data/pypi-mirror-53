A common use for notebooks is to "test an idea".  Designing pathways to mature informal notebook to formal testing tools like `doctest`.  This notebook implements the ability to `doctest` when a cell is run.


```python
import doctest, traitlets, IPython, contextlib, ast, textwrap
```

A full featured interactive `doctest` tool will be able to access any modifications to the interactive shell.  For example magics must work.


```python
    @contextlib.contextmanager
    def wrapped_compiler(shell):
        """`wrapped_compiler` replaces the `doctest` compiler with the interactive shell."""
        def compiler(input, filename, symbol, *args, **kwargs):
            nonlocal shell
            return shell.compile(ast.Interactive(body=shell.transform_ast(shell.compile.ast_parse(shell.transform_cell(textwrap.indent(input, " " * 4)))).body), filename, "single",)
        yield setattr(doctest, "compile", compiler)
        try: doctest.compile = compile
        except: ...
```

`run_docstring_examples` implements `doctest` machinery to test code with the interactive python shell.


```python
    def run_docstring_examples(str, shell=IPython.get_ipython(), verbose=False, compileflags=None):
        runner = doctest.DocTestRunner(verbose=verbose, optionflags=doctest.ELLIPSIS)
        with wrapped_compiler(shell):
            for test in doctest.DocTestFinder(verbose).find(str, name=shell.user_module.__name__):
                test.globs = shell.user_ns
                runner.run(test, compileflags=compileflags, clear_globs=False)
        return runner

    def run(result): return run_docstring_examples(result.info.raw_cell, IPython.get_ipython())
```


```python
    def unload_ipython_extension(shell):
        try: shell.events.unregister('post_run_cell', run)
        except ValueError: ...
    def load_ipython_extension(shell): unload_ipython_extension(shell), shell.events.register('post_run_cell', run)
    __name__ == '__main__' and load_ipython_extension(get_ipython())
```
