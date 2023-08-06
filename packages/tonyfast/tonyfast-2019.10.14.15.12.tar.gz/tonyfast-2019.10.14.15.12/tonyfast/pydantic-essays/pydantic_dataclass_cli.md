`pydantic.dataclasses` make it possible to create CLI's from `dataclasses` syntax.  The `pydantic_cli` package already does this for us, but it is strictly for `pydantic.BaseModel` objects.  When we call `pydantic_cli.to_runner`, we must explicity use the `dataclasses`'s `__pydantic_model__`.


```python
    import pydantic, pathlib
    @pydantic.dataclasses.dataclass
    class Y: a: int; b: int = None
    __import__('inspect').signature(Y)
```




    <Signature (a: int, b: int = None) -> None>




```python
    from IPython import get_ipython, display; Ø = __name__ == '__main__'
```


```python
    main = display.Code("""
    import pydantic, sys, pydantic_cli
    with __import__('importnb').Notebook(): import pydantic_dataclass_cli

    def main(object: pydantic_dataclass_cli.Y) -> int:
        print(object.dict())
        return 0

    __name__ == '__main__' and sys.exit(
        pydantic_cli.to_runner(
            pydantic_dataclass_cli.Y.__pydantic_model__, 
            main)(sys.argv[1:]))""", language="python"); main
```




<style>.output_html .hll { background-color: #ffffcc }
.output_html  { background: #f8f8f8; }
.output_html .c { color: #408080; font-style: italic } /* Comment */
.output_html .err { border: 1px solid #FF0000 } /* Error */
.output_html .k { color: #008000; font-weight: bold } /* Keyword */
.output_html .o { color: #666666 } /* Operator */
.output_html .ch { color: #408080; font-style: italic } /* Comment.Hashbang */
.output_html .cm { color: #408080; font-style: italic } /* Comment.Multiline */
.output_html .cp { color: #BC7A00 } /* Comment.Preproc */
.output_html .cpf { color: #408080; font-style: italic } /* Comment.PreprocFile */
.output_html .c1 { color: #408080; font-style: italic } /* Comment.Single */
.output_html .cs { color: #408080; font-style: italic } /* Comment.Special */
.output_html .gd { color: #A00000 } /* Generic.Deleted */
.output_html .ge { font-style: italic } /* Generic.Emph */
.output_html .gr { color: #FF0000 } /* Generic.Error */
.output_html .gh { color: #000080; font-weight: bold } /* Generic.Heading */
.output_html .gi { color: #00A000 } /* Generic.Inserted */
.output_html .go { color: #888888 } /* Generic.Output */
.output_html .gp { color: #000080; font-weight: bold } /* Generic.Prompt */
.output_html .gs { font-weight: bold } /* Generic.Strong */
.output_html .gu { color: #800080; font-weight: bold } /* Generic.Subheading */
.output_html .gt { color: #0044DD } /* Generic.Traceback */
.output_html .kc { color: #008000; font-weight: bold } /* Keyword.Constant */
.output_html .kd { color: #008000; font-weight: bold } /* Keyword.Declaration */
.output_html .kn { color: #008000; font-weight: bold } /* Keyword.Namespace */
.output_html .kp { color: #008000 } /* Keyword.Pseudo */
.output_html .kr { color: #008000; font-weight: bold } /* Keyword.Reserved */
.output_html .kt { color: #B00040 } /* Keyword.Type */
.output_html .m { color: #666666 } /* Literal.Number */
.output_html .s { color: #BA2121 } /* Literal.String */
.output_html .na { color: #7D9029 } /* Name.Attribute */
.output_html .nb { color: #008000 } /* Name.Builtin */
.output_html .nc { color: #0000FF; font-weight: bold } /* Name.Class */
.output_html .no { color: #880000 } /* Name.Constant */
.output_html .nd { color: #AA22FF } /* Name.Decorator */
.output_html .ni { color: #999999; font-weight: bold } /* Name.Entity */
.output_html .ne { color: #D2413A; font-weight: bold } /* Name.Exception */
.output_html .nf { color: #0000FF } /* Name.Function */
.output_html .nl { color: #A0A000 } /* Name.Label */
.output_html .nn { color: #0000FF; font-weight: bold } /* Name.Namespace */
.output_html .nt { color: #008000; font-weight: bold } /* Name.Tag */
.output_html .nv { color: #19177C } /* Name.Variable */
.output_html .ow { color: #AA22FF; font-weight: bold } /* Operator.Word */
.output_html .w { color: #bbbbbb } /* Text.Whitespace */
.output_html .mb { color: #666666 } /* Literal.Number.Bin */
.output_html .mf { color: #666666 } /* Literal.Number.Float */
.output_html .mh { color: #666666 } /* Literal.Number.Hex */
.output_html .mi { color: #666666 } /* Literal.Number.Integer */
.output_html .mo { color: #666666 } /* Literal.Number.Oct */
.output_html .sa { color: #BA2121 } /* Literal.String.Affix */
.output_html .sb { color: #BA2121 } /* Literal.String.Backtick */
.output_html .sc { color: #BA2121 } /* Literal.String.Char */
.output_html .dl { color: #BA2121 } /* Literal.String.Delimiter */
.output_html .sd { color: #BA2121; font-style: italic } /* Literal.String.Doc */
.output_html .s2 { color: #BA2121 } /* Literal.String.Double */
.output_html .se { color: #BB6622; font-weight: bold } /* Literal.String.Escape */
.output_html .sh { color: #BA2121 } /* Literal.String.Heredoc */
.output_html .si { color: #BB6688; font-weight: bold } /* Literal.String.Interpol */
.output_html .sx { color: #008000 } /* Literal.String.Other */
.output_html .sr { color: #BB6688 } /* Literal.String.Regex */
.output_html .s1 { color: #BA2121 } /* Literal.String.Single */
.output_html .ss { color: #19177C } /* Literal.String.Symbol */
.output_html .bp { color: #008000 } /* Name.Builtin.Pseudo */
.output_html .fm { color: #0000FF } /* Name.Function.Magic */
.output_html .vc { color: #19177C } /* Name.Variable.Class */
.output_html .vg { color: #19177C } /* Name.Variable.Global */
.output_html .vi { color: #19177C } /* Name.Variable.Instance */
.output_html .vm { color: #19177C } /* Name.Variable.Magic */
.output_html .il { color: #666666 } /* Literal.Number.Integer.Long */</style><div class="highlight"><pre><span></span><span class="kn">import</span> <span class="nn">pydantic</span><span class="o">,</span> <span class="nn">sys</span><span class="o">,</span> <span class="nn">pydantic_cli</span>
<span class="k">with</span> <span class="nb">__import__</span><span class="p">(</span><span class="s1">&#39;importnb&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">Notebook</span><span class="p">():</span> <span class="kn">import</span> <span class="nn">pydantic_dataclass_cli</span>

<span class="k">def</span> <span class="nf">main</span><span class="p">(</span><span class="nb">object</span><span class="p">:</span> <span class="n">pydantic_dataclass_cli</span><span class="o">.</span><span class="n">Y</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="nb">int</span><span class="p">:</span>
    <span class="k">print</span><span class="p">(</span><span class="nb">object</span><span class="o">.</span><span class="n">dict</span><span class="p">())</span>
    <span class="k">return</span> <span class="mi">0</span>

<span class="vm">__name__</span> <span class="o">==</span> <span class="s1">&#39;__main__&#39;</span> <span class="ow">and</span> <span class="n">sys</span><span class="o">.</span><span class="n">exit</span><span class="p">(</span>
    <span class="n">pydantic_cli</span><span class="o">.</span><span class="n">to_runner</span><span class="p">(</span>
        <span class="n">pydantic_dataclass_cli</span><span class="o">.</span><span class="n">Y</span><span class="o">.</span><span class="n">__pydantic_model__</span><span class="p">,</span> 
        <span class="n">main</span><span class="p">)(</span><span class="n">sys</span><span class="o">.</span><span class="n">argv</span><span class="p">[</span><span class="mi">1</span><span class="p">:]))</span>
</pre></div>





```python
    Ø and pathlib.Path('__main__.py').write_text(main.data)
```




    344



The sample `__main__.py` file above demons


```python
    if Ø: 
        !ipython __main__.py -- --help
```

    ]0;IPython: tonyfast/gists2usage: __main__.py [-h] [--b B] a
    
    positional arguments:
      a           (type:<class 'int'> )
    
    optional arguments:
      -h, --help  show this help message and exit
      --b B       (type:<class 'int'> default:None)



```python
    if Ø:
        !python __main__.py 10
```

    {'a': 10, 'b': None}

