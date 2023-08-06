Most canonical examples for [`fastapi`](https://github.com/tiangolo/fastapi) use `fastapi.FastAPI` to instantiate an application.  This notebook envisions a situation where an author has written several useful notebooks and they want to reuse as API's.  This is acheived with `fastapi` and `importnb`.


```python
import requests, pandas, IPython
```

`fastapi` provides the `fastapi.APIRouter` to build [bigger applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/#apirouter)


```python
app = __import__('fastapi').APIRouter()  # Typically __import__('fastapi').FastAPI()
```

`user` is an example endpoint that recieves __Github__ information for a username.


```python
@app.get('/user')
def user(name: str = 'tonyfast'):
    global id
    id = pandas.Series(requests.get(F'https://api.github.com/users/{name}').json())
    return id.to_dict()

__import__('requests_cache').install_cache('fastapi_routes') # Add a caching mechanism.
```

`gists` accesses the user's gist.


```python
@app.get('/gists')
def gists(pages: int = 2):
    global id, df
    globals().get('id', user())
    df = pandas.concat([pandas.DataFrame(requests.get(
        F'https://api.github.com/users/{id.login}/gists?page={i}').json()
                                        ) for i in range(1, pages)])
    return [x.to_dict() for n, x in df.iterrows()]
```

Use the base `starlette` library to customize to [customize repsonses](https://fastapi.tiangolo.com/tutorial/custom-response/).  For example, we return a `pandas` table.


```python
@app.get('/table', response_class=__import__('starlette').responses.HTMLResponse)
def table(): return globals()['df'].to_html()
```

## Running the application

1. Running this notebook

    Under the right conditions this notebook can be executed as a standalone application using the code below.


```python
if __name__ == '__main__' and '__file__' in globals():
    APP = __import__('fastapi').FastAPI()
    APP.include_router(app)
    __name__ == '__main__' and __import__('uvicorn').run(APP, host="0.0.0.0", port=8000)
```

2. Running many notebooks with `fastapi` and `uvicorn`.
    
    Create an application level python file to aggregrate the `fastapi.APIRouter`s into a unified application.  Each endpoint is prefix by the module name.


```python
__name__ == '__main__' and '__file__' not in globals() and IPython.display.Code(filename='main.py')
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
.output_html .il { color: #666666 } /* Literal.Number.Integer.Long */</style><div class="highlight"><pre><span></span><span class="n">app</span> <span class="o">=</span> <span class="nb">__import__</span><span class="p">(</span><span class="s1">&#39;fastapi&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">FastAPI</span><span class="p">()</span>
<span class="k">with</span> <span class="nb">__import__</span><span class="p">(</span><span class="s1">&#39;importnb&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">Notebook</span><span class="p">():</span>
    <span class="k">try</span><span class="p">:</span> <span class="kn">from</span> <span class="nn">.</span> <span class="kn">import</span> <span class="n">__fastapi_routes</span>
    <span class="k">except</span><span class="p">:</span> <span class="kn">import</span> <span class="nn">__fastapi_routes</span>
<span class="n">app</span><span class="o">.</span><span class="n">include_router</span><span class="p">(</span><span class="n">__fastapi_routes</span><span class="o">.</span><span class="n">app</span><span class="p">,</span> <span class="n">prefix</span><span class="o">=</span><span class="n">F</span><span class="s2">&quot;/{__fastapi_routes.__name__}&quot;</span><span class="p">)</span>
<span class="vm">__name__</span> <span class="o">==</span> <span class="s1">&#39;__main__&#39;</span> <span class="ow">and</span> <span class="nb">__import__</span><span class="p">(</span><span class="s1">&#39;uvicorn&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="n">app</span><span class="p">,</span> <span class="n">host</span><span class="o">=</span><span class="s2">&quot;0.0.0.0&quot;</span><span class="p">,</span> <span class="n">port</span><span class="o">=</span><span class="mi">8000</span><span class="p">)</span>
</pre></div>



