from django.forms import ModelForm

from .models import Category


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ["category_name", "cat_image"]

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields["category_name"].widget.attrs["placeholder"] = "Enter Category Name"

        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control mt-1 mb-2"
