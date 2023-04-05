```python
from dash import Dash, html

app = Dash()

app.layout = html.Div('My Dashboard 2')

if __name__ == '__main__':
    app.run_server(debug=True)
```

Dash example:
![img_1.png](img_1.png)

```python
app.layout = html.Div('My Dashboard')
```
![img_2.png](img_2.png)



