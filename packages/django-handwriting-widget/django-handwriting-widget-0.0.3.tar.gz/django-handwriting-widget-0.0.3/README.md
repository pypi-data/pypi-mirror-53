# Django Handwriting Widget

> A handwriting widget for django  
> Using [signature_pad](https://github.com/szimek/signature_pad) for js library

## Installation

Install with `pip`

```
pip install django-handwriting-widget
```

Add this app to `INSTALLED_APPS` in `settings.py`

```python
INSTALLED_APPS = [
    ...
    'handwriting',
]
```

## Usage

[Example model](e_signatures/models.py)

### Form

```python
from django import forms

from handwriting.forms import HandwritingPad

from .models import Signature


class SignatureForm(forms.ModelForm):
    class Meta:
        model = Signature
        fields = '__all__'
        widgets = {
            'image': HandwritingPad(),
        }
```

### Admin

```python
from django.contrib import admin

from handwriting.admin import HandwritingPadModelAdmin

from .models import Signature


@admin.register(Signature)
class SignatureAdmin(HandwritingPadModelAdmin):
    list_display = ('name', 'create_at')
```

or 

```python
from django.contrib import admin

from handwriting.admin import HandwritingPadAdminMixin

from .models import Signature


@admin.register(Signature)
class SignatureAdmin(HandwritingPadAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'create_at')
```

or

```python
from django.contrib import admin

from .forms import SignatureForm
from .models import Signature


@admin.register(Signature)
class SignatureAdmin(admin.ModelAdmin):
    form = SignatureForm
    list_display = ('name', 'create_at')
```
