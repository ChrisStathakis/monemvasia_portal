from .forms import NewsLetterFrontEndForm


def newsletter_data(request):
    return {
        'newsletter_form': NewsLetterFrontEndForm
    }