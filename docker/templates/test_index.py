from django.test import SimpleTestCase


class IndexTests(SimpleTestCase):
    def test_api_returns_hello_world(self):
        response = self.client.get("/__APP_NAME__")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "hello-world"})
