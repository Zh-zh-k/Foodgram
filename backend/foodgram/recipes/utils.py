from django.core.paginator import Paginator

RECIPES_IN_PAGE = 6


def pages(request, recipes):
    paginator = Paginator(recipes, RECIPES_IN_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
