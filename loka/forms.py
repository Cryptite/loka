from django import forms
from django.contrib.flatpages.models import FlatPage
from tinymce.widgets import TinyMCE
from loka.models import TownMedia


class TownBannerForm(forms.ModelForm):
    class Meta:
        model = TownMedia
        exclude = ['town']


class FlatPageForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = FlatPage