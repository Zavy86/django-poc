from django.urls import reverse
from django.utils.html import format_html
from django.views.debug import default_urlconf


def welcome(request):
    response = default_urlconf(request)
    links = format_html(
        '<nav aria-label="Project links" style="display: flex; '
        'justify-content: center; gap: 1.5rem; margin-top: 2rem;">'
        '<a href="{}">Django Admin</a>'
        '<a href="{}">POC API</a>'
        '</nav>',
        reverse("admin:index"),
        reverse("index"),
    )
    # Keep Django's bundled welcome page and add navigation inside its main content.
    response.content = response.content.replace(
        b"</main>", links.encode(response.charset) + b"</main>", 1
    )
    return response
