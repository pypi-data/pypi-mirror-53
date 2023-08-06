```python
    __all__ = 'get',
```

`get` is an `async` function to make requests to the github api.  if you have an access token in os.environ then you can make many requests.


```python
    import aiohttp, gidgethub.aiohttp, asyncio, pandas
```


```python
    async def get(*object):
        async with aiohttp.ClientSession() as session:
            gh = gidgethub.aiohttp.GitHubAPI(session, "deathbeds")
            return await asyncio.gather(*map(gh.getitem, object))
```


```python
    Ø = __name__ == '__main__'; 
    if Ø: import nest_asyncio; nest_asyncio.apply(); shell = get_ipython(); 
```


```python
    Ø and shell.run_cell("""(tony,) = await get('/users/tonyfast')""");
```


```python
    Ø and shell.run_cell("""df = pandas.concat([
        pandas.DataFrame(x)
        for x in await get(*[F"/users/tonyfast/gists?page={x}" for x in range(1, min(3, tony['public_gists']//30 + 1))])
    ])""");
```
