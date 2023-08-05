```python
import pathlib, collections, ipywidgets, contextlib
__all__ = 'articles',
```


```python
class Docs(collections.UserDict):
    mode = 'markdown'
    repr = __import__('IPython').display.Markdown
    def __getitem__(self, object): return self.repr(
        __import__('nbconvert').get_exporter(self.mode)().from_filename(super().__getitem__(object))[0]
    )
```


```python
root = pathlib.Path(globals().get('__file__', '__init__.py')).parent
articles = Docs((str(file.relative_to(root)), file) for file in root.rglob('*.ipynb'))
```


```python
with contextlib.redirect_stderr(__import__('io').StringIO()):
    @ipywidgets.interactive
    def browse(article: articles): display(article)

    _ipython_display_ = lambda:display(browse)
```
