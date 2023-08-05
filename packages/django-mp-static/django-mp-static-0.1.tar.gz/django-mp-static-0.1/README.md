# MP-static

Django static app.

### Installation

Install with pip:

```
pip install django-mp-static
```

Add your custom static settings:

```
from static import BaseStaticFilesSettings


class StaticFilesSettings(BaseStaticFilesSettings):

    IS_LESS_ENABLED = True  # this option enables less files compiler

    BOWER_INSTALLED_APPS = (
        'jquery#1.11.0',
        'bootstrap#3.3.7',
        ...
    )

    STYLESHEETS = (
        'bootstrap/less/bootstrap.less',
        'bootstrap/less/theme.less',
        ...
    )

    JAVASCRIPT = (
        'jquery/dist/jquery.js',
        'bootstrap/dist/js/bootstrap.js',
        ...
    )
```


Add static to template:

```
{% load pipeline %}

{% stylesheet 'generic' %}
{% javascript 'generic' %}
```
