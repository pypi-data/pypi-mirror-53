# django-slappy
[![PyPI version](https://badge.fury.io/py/vabbat.svg)](https://badge.fury.io/py/django-slappy)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/vabbat.svg)](https://pypi.python.org/pypi/django-slappy/)

This is a django app that allows you to run python interactively in slack. It requires an
existing server running django.

## Features

### Variable Persistence

![persist](https://raw.githubusercontent.com/Madoshakalaka/django-slappy/master/readme_assets/variable-persistence.png)

### Shared Scope
allows interactivity between users

![shared-scope](https://raw.githubusercontent.com/Madoshakalaka/django-slappy/master/readme_assets/shared_scope.png)

### Multi-liners

![multi-liner](https://raw.githubusercontent.com/Madoshakalaka/django-slappy/master/readme_assets/multi-liner.png)

### Fool Proof
Long running code will be terminated
![code-timeout](https://raw.githubusercontent.com/Madoshakalaka/django-slappy/master/readme_assets/timeout.png)

Exit prevention
![prevents-exit](https://raw.githubusercontent.com/Madoshakalaka/django-slappy/master/readme_assets/fool-proof.png)

## Installation

Need an already running django site

`pip install django-slappy`

1. Add "django_slappy" to your INSTALLED_APPS setting like this

    ```python
        INSTALLED_APPS = [
            ...
            'django_slappy',
        ]
    ```

2. Include the URLconf in your project urls.py like this

```
    path('slappy/', include('django_slappy.urls'))
```

3. [Create a slack app](https://api.slack.com/) and add command with url 'http://your-server/slappy/'

4. Install to workspace. Slack will give you an OAUTH secret. Paste to your `settings.py` like
following

    ```
    SLACK_OAUTH_SECRET = "abab-1231231231232-sfasfasdf-12312312"
    ```
   A better practice is to use environment variable.
   
## Note

Of course you'll expose your server to remote-exploitation.

Make sure your have nice people in your workspace, otherwise prepare to get your entire server deleted