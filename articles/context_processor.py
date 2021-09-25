from .models import ArticleCategory


def get_data(request):
    print(ArticleCategory.my_query.parent_categories())
    return {
        'categories': ArticleCategory.my_query.parent_categories()
    }