```python
    %reload_ext pidgin
    import graphviz
```


<pre class="ipython"><code>%reload_ext pidgin
import graphviz</code></pre>




```python
# Notebooks & computational documents


### Computational documents
## multi hypermedia collage

## An example: Business reports

* Word, Excel, Powerpoint, `...`


> ### Name some other computational documents.
```


<h1 id="notebooks-computational-documents">Notebooks &amp; computational documents</h1>
<h3 id="computational-documents">Computational documents</h3>
<h2 id="multi-hypermedia-collage">multi hypermedia collage</h2>
<h2 id="an-example-business-reports">An example: Business reports</h2>
<ul>
<li>Word, Excel, Powerpoint, <code>...</code></li>
</ul>
<blockquote>
<h3 id="name-some-other-computational-documents.">Name some other computational documents.</h3>
</blockquote>




```python
## Some other computational documents

* HTML
* Markdown
* PDF
* Latex
* Jupyter notebooks
* Software packages
```


<h2 id="some-other-computational-documents">Some other computational documents</h2>
<ul>
<li>HTML</li>
<li>Markdown</li>
<li>PDF</li>
<li>Latex</li>
<li>Jupyter notebooks</li>
<li>Software packages</li>
</ul>




```python
## Words & not words

Data-driven documents go beyond words to include data, code, & visuals fill voids in language.

### Computational Documents are multi-lingual
```


<h2 id="words-not-words">Words &amp; not words</h2>
<p>Data-driven documents go beyond words to include data, code, &amp; visuals fill voids in language.</p>
<h3 id="computational-documents-are-multi-lingual">Computational Documents are multi-lingual</h3>




```python
## Literate programs

Our savior [Donald Knuth](https://en.wikipedia.org/wiki/Donald_Knuth).

* [The Patron Saint of Yak Shaves](https://yakshav.es/the-patron-saint-of-yakshaves/)
```


<h2 id="literate-programs">Literate programs</h2>
<p>Our savior <a href="https://en.wikipedia.org/wiki/Donald_Knuth">Donald Knuth</a>.</p>
<ul>
<li><a href="https://yakshav.es/the-patron-saint-of-yakshaves/">The Patron Saint of Yak Shaves</a></li>
</ul>




```python
## Precedence in journalism

Data driven journalism is athe forefront of comminicating information.|

* [`"django"`](https://en.wikipedia.org/wiki/Django_(web_framework))
    
    ![](https://user-images.githubusercontent.com/4236275/65614341-fc2ec700-dfa6-11e9-9b00-741b974d3142.png)
    
* [The future of news is not an article](http://nytlabs.com/blog/2015/10/20/particles/)
* [LA times uses altair](https://github.com/datadesk/altair-latimes/pull/1)
```


<h2 id="precedence-in-journalism">Precedence in journalism</h2>
<p>Data driven journalism is athe forefront of comminicating information.|</p>
<ul>
<li><p><a href="https://en.wikipedia.org/wiki/Django_(web_framework)"><code>"django"</code></a></p>
<p><img src="https://user-images.githubusercontent.com/4236275/65614341-fc2ec700-dfa6-11e9-9b00-741b974d3142.png" /></p></li>
<li><p><a href="http://nytlabs.com/blog/2015/10/20/particles/">The future of news is not an article</a></p></li>
<li><p><a href="https://github.com/datadesk/altair-latimes/pull/1">LA times uses altair</a></p></li>
</ul>




```python
* ## Code > Narrative
* ## Narrative > Code

> ### Which is role the of `"data scientist"`, and `"software engineer"`?
```


<ul>
<li><h2 id="code-narrative">Code &gt; Narrative</h2></li>
<li><h2 id="narrative-code">Narrative &gt; Code</h2></li>
</ul>
<blockquote>
<h3 id="which-is-role-the-of-data-scientist-and-software-engineer">Which is role the of <code>"data scientist"</code>, and <code>"software engineer"</code>?</h3>
</blockquote>



`my_function_that_changes_the_world_cause_I_said_so` then I'll key programming

## Code > Narrative

Informal names are adopted for literacy and narrative in `"docstrings"` are secondary to the code.


```python
    def my_function_that_changes_the_world_cause_I_said_so(): 
        """>>> assert 42, 'This function does not change the world'"""
```


<pre class="ipython"><code>def my_function_that_changes_the_world_cause_I_said_so(): 
    &quot;&quot;&quot;&gt;&gt;&gt; assert 42, &#39;This function does not change the world&#39;&quot;&quot;&quot;</code></pre>



## Narrative Over Code

my `function` that `changes_the_world` cause I said so` then I'll key programming

    def function(): """>>> assert 42"""
    def changes_the_world(): """>>> assert True"""

Literate documents include code & multimedia in formal language to connect features of the human and machine language.


```python
### Doctesting and docstrings

    import doctest

Tests provide trust to an `object`.  Place `doctest`s in your function to run tests interactively.

    doctest.testmod()
```




    TestResults(failed=0, attempted=3)



## Notebooks simulate a document.

# They are a flexible form to project different forms of multi hypermedia documents.


```python
    graphviz.Source("digraph {Notebooks->{ %s }}"%' '.join(x for x in __import__('nbconvert').get_export_names() if not '_' in x))
```




![svg](output_14_0.svg)




<pre class="ipython"><code>graphviz.Source(&quot;digraph {Notebooks-&gt;{ %s }}&quot;%&#39; &#39;.join(x for x in __import__(&#39;nbconvert&#39;).get_export_names() if not &#39;_&#39; in x))</code></pre>




```python

```
