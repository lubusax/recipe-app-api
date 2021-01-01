from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@thingsintouch.com',
            password='password123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@thingsintouch.com',
            password='password123',
            name='Jon Doe'
        )

    def test_users_listed(self):
        """Are users listed on user page?"""
        url = reverse('admin:core_user_changelist')
        response = self.client.get(url)

        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)

    def test_user_change_page(self):
        """Does the user edit page work?"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        # /admin/core/user/<:id>
        response = self.client.get(url)  # http GET

        self.assertEqual(response.status_code, 200)

    def test_create_user_page(self):
        """Does the create user page work?"""
        url = reverse('admin:core_user_add')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
