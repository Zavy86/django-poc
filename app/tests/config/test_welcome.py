from django.test import SimpleTestCase
from django.urls import reverse


class WelcomeTests(SimpleTestCase):
    def test_root_displays_django_welcome_page(self):
        response = self.client.get("/")

        self.assertContains(response, "The install worked successfully! Congratulations!")
        self.assertTrue(response["Content-Type"].startswith("text/html"))

    def test_welcome_links_to_admin_and_api(self):
        response = self.client.get("/")

        self.assertContains(response, f'href="{reverse("admin:index")}"')
        self.assertContains(response, f'href="{reverse("index")}"')
