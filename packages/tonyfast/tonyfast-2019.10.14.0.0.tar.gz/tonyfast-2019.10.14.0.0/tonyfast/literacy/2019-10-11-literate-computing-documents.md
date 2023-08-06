```python
    %reload_ext tonyfast.literacy
    import graphviz
```


    %reload_ext tonyfast.literacy
    import graphviz



```python
[Literate programs][literate] employ multiple language forms to communicate computational thought.
They target human readable documents and computational source code.
Donald Knuth's original literate programming implementation WEB combines $\LaTeX$ for document formatting and Pascal computation.
This approach to composition allows a program to express a narrative in human & computer logic.

![](https://user-images.githubusercontent.com/4236275/66661243-313d4980-ec36-11e9-93bc-159498cde227.png)

[meta]: https://en.wikipedia.org/wiki/Metalanguage
[literate]: https://en.wikipedia.org/wiki/Literate_programming
[ousterhout]: https://en.wikipedia.org/wiki/Ousterhout%27s_dichotomy
[pdf]: http://www.literateprogramming.com/knuthweb.pdf
```

    <>:11: DeprecationWarning: invalid escape sequence \L



[Literate programs][literate] employ multiple language forms to communicate computational thought.
They target human readable documents and computational source code.
Donald Knuth's original literate programming implementation WEB combines $\LaTeX$ for document formatting and Pascal computation.
This approach to composition allows a program to express a narrative in human & computer logic.

![](https://user-images.githubusercontent.com/4236275/66661243-313d4980-ec36-11e9-93bc-159498cde227.png)

[meta]: https://en.wikipedia.org/wiki/Metalanguage
[literate]: https://en.wikipedia.org/wiki/Literate_programming
[ousterhout]: https://en.wikipedia.org/wiki/Ousterhout%27s_dichotomy
[pdf]: http://www.literateprogramming.com/knuthweb.pdf



```python
    
    document = graphviz.Source("""digraph {
    layout=dot
    node[penwidth=0 fontsize=20]
    edge[style=tapered penwidth=5]
    narrative->program -> {application scripting}
    subgraph cluster_ousterhout {scripting application label="ousterhout's\ndichotomy"}
    subgraph cluster_narrative {narrative program label=document}
    subgraph cluster_types {static dynamic label=types}
    scripting->dynamic
    application->static
    narrative-> human -> dynamic
    program -> computer -> static
    subgraph cluster_literate {human computer label="language"}
    }""")
```


```python
The literate program has two components: the document langauge and programming language.  
Programming languages have another dichotomy of an statically typed application and a dynamically typed scripting language.

    document
```




![svg](output_3_0.svg)




The literate program has two components: the document langauge and programming language.  
Programming languages have another dichotomy of an statically typed application and a dynamically typed scripting language.

    document



```python
    
    implementation = graphviz.Source("""digraph {
        layout=dot
        node[penwidth=0 fontsize=20]
        edge[style=tapered penwidth=5]
        markdown->narrative->program -> {application scripting}
        markdown->python -> scripting
        markdown->bash-> application
        subgraph cluster_xonsh {python bash label=xonsh}
        subgraph cluster_ousterhout {scripting application label="ousterhout's\ndichotomy"}
        subgraph cluster_narrative {narrative program label=document}
        subgraph cluster_types {static dynamic label=types}
        scripting->dynamic
        application->static
        narrative-> human -> dynamic
        program -> computer -> static
        subgraph cluster_literate {human computer label="language"}
    }""")
```


```python
    import xonsh
A modern implementation of literate programming could use Markdown as a document language.  
Markdown is a flexible markup language that permits any programming language as a subset.
A holistic literate programming language should have access to scripting and application languages.
In this tool, we choose `xonsh` which allows scripting in python and application programming in bash.

    implementation
```




![svg](output_5_0.svg)




    import xonsh
A modern implementation of literate programming could use Markdown as a document language.  
Markdown is a flexible markup language that permits any programming language as a subset.
A holistic literate programming language should have access to scripting and application languages.
In this tool, we choose `xonsh` which allows scripting in python and application programming in bash.

    implementation



```python
Now using markdown we can run bash code inline `git status` and python `print(F"{__name__} woo")`.
And of course indented code is run as expected.

    x = $(ls)
    print('----')
    print(len(x))
```

    ----
    298



Now using markdown we can run bash code inline `git status` and python `print(F"{__name__} woo")`.
And of course indented code is run as expected.

    x = $(ls)
    print('----')
    print(len(x))



```python
    import doctest
We can `doctest` stuff too!

    >>> echo hello
    hello
    <BLANKLINE>
    >>> 11
    1...
```


    import doctest
We can `doctest` stuff too!

    >>> echo hello
    hello
    <BLANKLINE>
    >>> 11
    1...

