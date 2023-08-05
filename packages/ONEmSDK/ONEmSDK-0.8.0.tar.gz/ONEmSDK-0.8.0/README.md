# ONEm Python SDK

*ONEm Python SDK* is a library that helps in communication between your web app and the
ONEm platform. It guides the developer to build JSON responses which are compliant with
the [JSON schema](https://app.swaggerhub.com/apis/romeo1m/schemajson) ONEm platform works 
by.

## Installation
```bash
$ pip install onemsdk
```

## Version history
See [HISTORY.md](HISTORY.md) file.

## Usage example

In order to serve a selectable menu like the one below, the application has to respond to
ONEm platform with a JSON having a certain structure.

The menu:
```
#MY-FIRST-APP MENU
A First item
B Second item
C Third item
--Reply A-C
```

The menu, as any other screen the user receives, has a simple structure, very similar with
with a web page:
- the first line is called **header** ("#MY-FIRST-APP MENU")
- it continues with a **body** (containing the selectable options)
- the last line is called **footer** ("--Reply A-C").


The JSON that generates this menu:
```json
{
  "content_type": "menu",
  "content": {
    "type": "menu",
    "body": [
      {
        "type": "option",
        "description": "First item",
        "method": "GET",
        "path": "/callback-url/item1"
      },
      {
        "type": "option",
        "description": "Second item",
        "method": "GET",
        "path": "/callback-url/item2"
      },
      {
        "type": "option",
        "description": "Third item",
        "method": "POST",
        "path": "/callback-url/item3"
      }
    ],
    "header": "my menu",
    "footer": "Reply A-C"
  }
}
``` 

Working with JSONs is not as fast and clear as using simple Python objects or HTML. Here
is where the ONEm SDK comes into play.

Before starting to write code please make sure you have an account on the ONEm developer
portal and registered an app. We will assume your app is called **my-first-app**.

### Create a menu with Python objects
```python
from onemsdk.schema.v1 import Response, Menu, MenuItem


def handle_request_with_objects(request):

    menu_items = [
        MenuItem(description='First item',
                 method='GET',
                 path='/callback-url/item1'),
        MenuItem(description='Second item',
                 method='GET',
                 path='/callback-url/item2'),
        MenuItem(description='Third item',
                 method='POST',
                 path='/callback-url/item3')
    ]

    menu = Menu(header='menu', footer='Reply A-C', body=menu_items)

    # Wrap the Menu object into a Response object compatible with the JSON schema
    response = Response(content=menu)

    # Jsonify the response and send it the over the wire
    return response.json()
```

### Create a menu with HTML

#### 1. Create `<appdir>/static/menu.html` file:
```html
<section>
  <header>menu</header>
  <ul>
    <li>
      <a href="/callback-url/item1" method="GET">First item</a>
    </li>
    <li>
      <a href="/callback-url/item2" method="GET">Second item</a>
    </li>
    <li>
      <a href="/callback-url/item3" method="POST">Third item</a>
    </li>
  </ul>
  <footer>Reply A-C</footer>
</section>
```

#### 2. In your request handler:
```python
from onemsdk.parser import load_html
from onemsdk.schema.v1 import Response


def handle_request_with_html(request):
    ...
    # Turn the HTML into a Python tag object
    root_tag = load_html(html_file="<appdir>/static/menu.html")

    # Turn the tag object into a Response object compatible with the JSON schema
    response = Response.from_tag(root_tag)

    # Jsonify the response and send it the over the wire
    return response.json()
```

ONEm SDK supports Jinja2 and Django template engines, as HTML is not a good fit for dynamic content.

Setting a directory with static files is recommended when using HTML or Jinja2 files.
After doing that, all the files can be referred relative to the static directory. The
place to do that is the entry file of your web application:

```python
import onemsdk

...
onemsdk.config.set_static_dir('./static')
...
```

### Create a menu with Jinja2 template
#### 1. Create `<appdir>/static/menu.jinja2` file:
```jinja2
<section>
  <header>{{ header }}</header>
  <ul>
    {% for item in items %}
    <li>
      <a href="{{ item['href'] }}" 
         method="{{ item['method'] }}">
          {{ item['description'] }}
      </a>
    </li>
    {% endfor %}
  </ul>
  <footer>{{ footer }}</footer>
</section>
```

#### 2. In your request handler:
```python
from onemsdk.schema.v1 import Response
from onemsdk.parser import load_template


def handle_request_with_template(request):
    ...
    data = {
        'header': 'menu',
        'footer': 'Reply A-C',
        'items': [
            {
                'method': 'GET', 
                'href': '/callback-url/item1', 
                'description': 'First item'
            },
            {
                'method': 'GET', 
                'href': '/callback-url/item2', 
                'description': 'Second item'
            },
            {
                'method': 'POST', 
                'href': '/callback-url/item3', 
                'description': 'Third item'
            },
        ]
    }
    
    # Turn the HTML template into Python object
    # Static directory is set, so write only the name of the Jinja2 file 
    root_tag = load_template(template_file="menu.jinja2", **data)

    # Turn the tag object into a Response object compatible with the JSON schema
    response = Response.from_tag(root_tag)

    # Jsonify the response and send it the over the wire
    return response.json()
```


### Using Django templates
#### 1. Add the middleware, ideally last in your `settings.MIDDLEWARE` chain

```python

MIDDLEWARE = [
    ...,
    'onemsdk.contrib.django.HtmlToOnemResponseMiddleware',
]
```


#### 2. Use Django templates with the ONEm supported tags.

```python
from django.views.generic import TemplateView

class MyMenuView(TemplateView):
    template_name = 'my_menu.html'

    def get_context_data(self):
        items = Item.objects.all()  # some items
        return {'items': items}
```

```html
<section>
    <header>My Menu</header>
    <ul>
        {% for item in items %}
            <li>
                <a href="{{ item.get_absolute_url }}">
                    {{ item.description }}
                </a>
            </li>
        {% endfor %}
    </ul>
    <footer>My Footer</footer>
</section>
```
