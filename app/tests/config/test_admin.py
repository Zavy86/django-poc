from django.test import SimpleTestCase


class AdminTests(SimpleTestCase):
    def test_admin_requires_login(self):
        response = self.client.get("/admin/")

        self.assertRedirects(
            response, "/admin/login/?next=/admin/", fetch_redirect_response=False
        )

    def test_admin_login_page_is_available(self):
        response = self.client.get("/admin/login/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin/login.html")
        self.assertContains(response, 'name="username"')
