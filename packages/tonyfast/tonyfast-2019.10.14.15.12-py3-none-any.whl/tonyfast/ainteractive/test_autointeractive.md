```python
with __import__('importnb').Notebook():
    %reload_ext autointeractive
```


```python
def f(x: (0, 100, 2)): return x
```


```python
f
```

    <function f at 0x7f6380d43488>



    interactive(children=(IntSlider(value=50, description='x', step=2), Output()), _dom_classes=('widget-interact'…



```python
def g(x: int, y: str, z: (0, 100)): return x, y, z
```


```python
g
```

    <function g at 0x7f6380650158>



    interactive(children=(Dropdown(description='x', options=(6409049200610498984, -46, 10992, 44, -20658, -8, 0, 0…

