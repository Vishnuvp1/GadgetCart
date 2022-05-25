from django.forms import ModelForm

from .models import Brand


class BrandForm(ModelForm):
    class Meta:
        model = Brand
        fields = ["brand_name", "brand_image"]

    def __init__(self, *args, **kwargs):
        super(BrandForm, self).__init__(*args, **kwargs)
        self.fields["brand_name"].widget.attrs["placeholder"] = "Enter Brand Name"

        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control mt-1 mb-2"
