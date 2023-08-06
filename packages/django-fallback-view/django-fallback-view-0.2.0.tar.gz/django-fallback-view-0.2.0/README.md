# Django Fallback View

## Description

Middleware that returns a fallback view when the URL matches anything that isnt specified>

## Installation

```
pip install django-fallback-view
```

## Usage

```python
# settings.py

FALLBACK_VIEW = "path.to.view.class.ViewClass"

MIDDLEWARE = [
    ...
    "fallback_view.middleware.FallbackViewMiddleware",
]
```


