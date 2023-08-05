# Project description
Django View As user is a middleware thats provides login in as any user functionality. It is modification of [django-view-as](https://pypi.org/project/django-view-as/) package. The django-view-as is not supported on django 2 and newer version, so I have modified the package.

  - User a shortcurt key to switch user
  - Login to Django application as any user
  - Switchback to orginal user

### Installation

Install the package:

```
pip install viewasuser
```
Add installed app:

```
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.sessions',
    'viewasuser',
]
```
Add the middleware:

```
MIDDLEWARE = [
    'viewasuser.middleware.ViewAsMiddleware',

]
```

### Usage
Load any page with an html response type, hit the tilda key (~), and you’ll see a new toolbar at the bottom of the page. Enter a username to change who you’re viewing the site as.

### Configure the menu toggle key
The following configuration option could be set in your settings.py to change the default keystroke to toggle the “View as” menu. Its value is the javascript key number that will be matched in the keydown event handler.

```
VIEWAS_TOGGLE_KEY = 192 
```

### License
----
MIT

