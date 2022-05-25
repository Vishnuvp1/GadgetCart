from .models import Brand


def menulinks(request):
    links = Brand.objects.all()
    return dict(link=links)
