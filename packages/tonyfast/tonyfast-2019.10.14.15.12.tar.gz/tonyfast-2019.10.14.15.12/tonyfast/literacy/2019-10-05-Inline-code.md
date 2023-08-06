All code should compute, <code>code</code> for typographic decoration should require extra effort to suppress.  As a rule, code in a document should work.


In this document, we'll execute code from within ticks as one would with inline code.


```python
import ast, mistune, re
```

Use `mistune`'s pattern to discover inine code.


```python
inline = re.compile(mistune.InlineGrammar.code.pattern[1:])
```

Create an `ast.NodeTransformer` that runs code in ticks.  In this case, `ast.parse` is applied to any inline code.


```python
class Inline(ast.NodeTransformer):
    def __init__(self, shell): self.shell = shell
    def visit_Expr(self, node):
        if isinstance(node.value, ast.Str):
            nodes = [node]
            for m in inline.finditer(node.value.s): nodes += ast.copy_location(self.shell.compile.ast_parse(m.group().strip('`')), node).body
            return nodes
        return node
```

Append to the `ast_transformers` with an `IPython` magic.


```python
    def unload_ipython_extension(shell): shell.ast_transformers += [x for x in shell.ast_transformers if not isinstance(x, Inline)]
    def load_ipython_extension(shell): unload_ipython_extension(shell); shell.ast_transformers += [Inline(shell)]
    __name__ == '__main__' and load_ipython_extension(get_ipython())
```
