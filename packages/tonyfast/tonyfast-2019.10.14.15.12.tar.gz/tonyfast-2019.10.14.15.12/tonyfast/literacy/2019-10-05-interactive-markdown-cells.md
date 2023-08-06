My white 🐳 is literate markdown programming in the notebook.

I have made so many attempts at a literate interface to the notebook.  Each of these experiments revealed important features of modern [literate ~~programming~~ computing](http://blog.fperez.org/2013/04/literate-computing-and-computational.html).

I've drawn the concept in packages & single notebooks.  In retrospect, they contain too many opinions to be extensible.  

Here is another go at it.


```python
    import re, textwrap, tokenize, io, itertools, IPython; from toolz.curried import *
    __all__ = 'parse',
```

Use the `mistune` to `parse` block level markdown objects.


```python
    class Lexer(__import__('mistune').BlockLexer):
        def parse(self, text, rules=None):
            text = ''.join(x if x.strip() else "\n" for x in text.splitlines(True))
            rules = rules or self.default_rules
            def manipulate(text):
                for key in rules:
                    m = getattr(self.rules, key).match(text)
                    if m: getattr(self, 'parse_%s' % key)(m); return m
                return False  
            while text:
                m = manipulate(text)
                if m: text = text[len(m.group(0)):]
                if not m and text: raise RuntimeError('Infinite loop at: %s' % text)
                if self.tokens: self.tokens[-1]['match'] = m
            return self.tokens
```


```python
    def quote(str, prior="", tick='"""'):
        """wrap a block of text in quotes. """
        if not str.strip(): return str
        indent, outdent = len(str)-len(str.lstrip()), len(str.rstrip())
        if tick in str or str.endswith(tick[0]): tick = '"""'
        return str[:indent] + prior + tick + str[indent:outdent] + tick + ";" + str[outdent:]
```

`parse`  markdown code into valid python code.


```python
    def parse(object, *, formatted="" , indent=4, _indent=-1):
        object += '\n'
        """`parse` code formatted in markdown"""
        tokens = Lexer()(object)
        while tokens:
            token = tokens.pop(0)
            if token['type'] == 'code':
                if token['lang']: continue
                code = token['match'].group().rstrip()
                text, object = re.split(r'\s*'.join(re.escape(code).splitlines(True)), object)
                stripped = code.strip()
                if stripped.startswith(('>>>',)) or not stripped: continue # don't do anything for blank code.
                if _indent < 0: _indent = len(code) - len(code.lstrip())
                if code.startswith(('```',)): code = textwrap.indent(code.strip('`'), ' '*_indent)
                try: last_token = pipe(list(tokenize.tokenize(io.BytesIO(textwrap.dedent(formatted).encode('utf-8')).readline)),reversed, curry(itertools.dropwhile)(compose(complement(str.strip), operator.attrgetter('string'))), first)
                except tokenize.TokenError as exception:
                    if exception.args[0] == 'EOF in multi-line string': text = textwrap.indent(text, ' '*_indent)
                    else: text = (text.strip() and quote or identity)(text, ' '*_indent)
                else: 
                    text = quote(textwrap.indent(text, ' '*_indent), ' '*indent if last_token.string in {':'} else '' + ' '*(len(last_token.line) - len(last_token.line.lstrip())))
                formatted += text + code
        if object.strip(): formatted += textwrap.indent(quote(object), ' '*_indent)
        IPython.get_ipython().log.debug(textwrap.dedent(formatted))
        return formatted
```

Another notebook defines how the output should be displayed.

Create `IPython` extensions that can be reused.


```python
    def cleanup_transform(x): return textwrap.dedent(parse(''.join(x))).splitlines(True)

    def unload_ipython_extension(shell):
        globals()['_transforms'] = globals().get('_transforms', shell.input_transformer_manager.cleanup_transforms)
        global _transforms
        shell.input_transformer_manager.cleanup_transforms = _transforms
    def load_ipython_extension(shell):
        unload_ipython_extension(shell)
        shell.input_transformer_manager.cleanup_transforms = [cleanup_transform]

    __name__ == '__main__' and load_ipython_extension(get_ipython())
```

> This currently doesn't work inside list items.
