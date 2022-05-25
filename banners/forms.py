from django import forms
from banners.models import Banner


class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = "__all__"
