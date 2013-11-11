from django import forms
from loka.models import TownMedia


class TownBannerForm(forms.ModelForm):
    class Meta:
        model = TownMedia
        exclude = ['town']