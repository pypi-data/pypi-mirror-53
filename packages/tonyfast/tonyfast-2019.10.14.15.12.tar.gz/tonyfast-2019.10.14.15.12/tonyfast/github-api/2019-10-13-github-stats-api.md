https://developer.github.com/v3/repos/statistics/


```python
    %%capture
    import uritemplate, requests, pandas, hvplot.pandas; __import__('requests_cache').install_cache('stats')
```


```python
    stats = "https://api.github.com/repos/{owner}/{repo}/stats/"
```


```python
    for x in "contributors commit_activity code_frequency".split():
        globals()[x] = uritemplate.URITemplate(stats+x)
```


```python
    owner, repo = "omnisci/jupyterlab-omnisci".split('/')
```


```python
    def get(url):
        if requests.get(url).status_code == 202: return __import__('time').sleep(1) or get(url)
        return pandas.DataFrame(requests.get(url).json())
```


```python
    df = get(contributors.expand(globals()))
    df = df.weeks.apply(pandas.Series).stack().apply(pandas.Series).reset_index(-1, drop=True).join(df.author.apply(pandas.Series))
    df.w = df.w.pipe(pandas.to_datetime, unit='s')
    df = df.set_index(['w', 'login'])

    contributions = df[list('acd')].rename(columns=dict(zip('ad', '+-'), c='commits')).unstack('login')
    contributions.T
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>w</th>
      <th>2018-03-25</th>
      <th>2018-04-01</th>
      <th>2018-04-08</th>
      <th>2018-04-15</th>
      <th>2018-04-22</th>
      <th>2018-04-29</th>
      <th>2018-05-06</th>
      <th>2018-05-13</th>
      <th>2018-05-20</th>
      <th>2018-05-27</th>
      <th>...</th>
      <th>2019-08-11</th>
      <th>2019-08-18</th>
      <th>2019-08-25</th>
      <th>2019-09-01</th>
      <th>2019-09-08</th>
      <th>2019-09-15</th>
      <th>2019-09-22</th>
      <th>2019-09-29</th>
      <th>2019-10-06</th>
      <th>2019-10-13</th>
    </tr>
    <tr>
      <th></th>
      <th>login</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan="5" valign="top">+</td>
      <td>domoritz</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>gnestor</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>ian-r-rose</td>
      <td>42848</td>
      <td>507</td>
      <td>771</td>
      <td>319</td>
      <td>551</td>
      <td>311</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>656</td>
      <td>149</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>saulshanabrook</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>410</td>
      <td>0</td>
      <td>70</td>
      <td>456</td>
      <td>28</td>
      <td>225</td>
      <td>...</td>
      <td>1671</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>tonyfast</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>15</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td rowspan="5" valign="top">commits</td>
      <td>domoritz</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>gnestor</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>ian-r-rose</td>
      <td>14</td>
      <td>3</td>
      <td>10</td>
      <td>5</td>
      <td>8</td>
      <td>9</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>5</td>
      <td>4</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>saulshanabrook</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>8</td>
      <td>0</td>
      <td>1</td>
      <td>3</td>
      <td>2</td>
      <td>7</td>
      <td>...</td>
      <td>10</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>tonyfast</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td rowspan="5" valign="top">-</td>
      <td>domoritz</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>gnestor</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>ian-r-rose</td>
      <td>42164</td>
      <td>17</td>
      <td>353</td>
      <td>78</td>
      <td>111</td>
      <td>103</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>1814</td>
      <td>73</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>saulshanabrook</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>56</td>
      <td>0</td>
      <td>33</td>
      <td>127</td>
      <td>28</td>
      <td>12</td>
      <td>...</td>
      <td>4720</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>tonyfast</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
<p>15 rows × 82 columns</p>
</div>




```python
    df = get(commit_activity.expand(globals()))
    df.week = df.week.pipe(pandas.to_datetime, unit='s')
    df = df.set_index('week').days.apply(pandas.Series)
    df.columns = (
        df.index[0]+pandas.to_timedelta(df.columns.map('{} days'.format))
    ).strftime('%A')

    weekly_commits = df
    weekly_commits.T
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>week</th>
      <th>2018-10-21</th>
      <th>2018-10-28</th>
      <th>2018-11-04</th>
      <th>2018-11-11</th>
      <th>2018-11-18</th>
      <th>2018-11-25</th>
      <th>2018-12-02</th>
      <th>2018-12-09</th>
      <th>2018-12-16</th>
      <th>2018-12-23</th>
      <th>...</th>
      <th>2019-08-11</th>
      <th>2019-08-18</th>
      <th>2019-08-25</th>
      <th>2019-09-01</th>
      <th>2019-09-08</th>
      <th>2019-09-15</th>
      <th>2019-09-22</th>
      <th>2019-09-29</th>
      <th>2019-10-06</th>
      <th>2019-10-13</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Sunday</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>8</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Monday</td>
      <td>0</td>
      <td>8</td>
      <td>9</td>
      <td>3</td>
      <td>3</td>
      <td>3</td>
      <td>1</td>
      <td>0</td>
      <td>13</td>
      <td>0</td>
      <td>...</td>
      <td>9</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Tuesday</td>
      <td>0</td>
      <td>11</td>
      <td>0</td>
      <td>4</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Wednesday</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>2</td>
      <td>0</td>
      <td>1</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Thursday</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>7</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>2</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Friday</td>
      <td>4</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>3</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>3</td>
      <td>4</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Saturday</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
<p>7 rows × 52 columns</p>
</div>




```python
    df = get(code_frequency.expand(globals()))
    df = df[[1, 2]].rename(columns=dict(zip([1,2], "+-"))).set_index(df[0].pipe(pandas.to_datetime, unit='s').rename('week'))
    code_changes = df; code_changes.T
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>week</th>
      <th>2018-03-25</th>
      <th>2018-04-01</th>
      <th>2018-04-08</th>
      <th>2018-04-15</th>
      <th>2018-04-22</th>
      <th>2018-04-29</th>
      <th>2018-05-06</th>
      <th>2018-05-13</th>
      <th>2018-05-20</th>
      <th>2018-05-27</th>
      <th>...</th>
      <th>2019-08-11</th>
      <th>2019-08-18</th>
      <th>2019-08-25</th>
      <th>2019-09-01</th>
      <th>2019-09-08</th>
      <th>2019-09-15</th>
      <th>2019-09-22</th>
      <th>2019-09-29</th>
      <th>2019-10-06</th>
      <th>2019-10-13</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>+</td>
      <td>42848</td>
      <td>507</td>
      <td>771</td>
      <td>319</td>
      <td>976</td>
      <td>311</td>
      <td>70</td>
      <td>456</td>
      <td>28</td>
      <td>225</td>
      <td>...</td>
      <td>1671</td>
      <td>0</td>
      <td>656</td>
      <td>149</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>-</td>
      <td>-42164</td>
      <td>-17</td>
      <td>-353</td>
      <td>-78</td>
      <td>-168</td>
      <td>-103</td>
      <td>-33</td>
      <td>-127</td>
      <td>-28</td>
      <td>-12</td>
      <td>...</td>
      <td>-4720</td>
      <td>0</td>
      <td>-1814</td>
      <td>-73</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
<p>2 rows × 82 columns</p>
</div>


