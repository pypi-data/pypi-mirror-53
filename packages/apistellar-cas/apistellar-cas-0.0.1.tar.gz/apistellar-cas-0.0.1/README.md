# CAS for apistellar

## USEAGE
```angular2
pip install apistellar-cas
```

```python
from apistellar_cas import nit

# before app init
init()
...
```

```python
from apistar import App
from apistellar import Controller, route, get
from apistellar_cas import login_required


@route("/", name="welcome")
class WelcomeController(Controller):

    @get("/")
    @login_required() # add this
    def index(self, app: App) -> str:
        return app.render_template('index.html')

```
