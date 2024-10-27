from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Promo
from django.utils import timezone

User  = get_user_model()

class PromoTests(TestCase):

    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='password', role=1)
        self.outlet_user = User.objects.create_user(username='outlet', password='password', role=2)
        self.client.login(username='admin', password='password')

        self.promo = Promo.objects.create(
            title='Test Promo',
            description='This is a test promo.',
            discount_percentage=20.00,
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(days=10),
            promo_code='TEST20',
            created_by=self.outlet_user
        )

    def test_show_promo_list_admin(self):
        response = self.client.get(reverse('promo:show_promo'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Promo Spesial untuk Kamu!')

    def test_show_promo_list_outlet_user(self):
        self.client.logout()
        self.client.login(username='outlet', password='password')
        response = self.client.get(reverse('promo:show_promo'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Update Promo Outlet Kamu!')

    def test_create_promo(self):
        self.client.login(username='outlet', password='password')
        response = self.client.post(reverse('promo:create_promo'), {
            'title': 'New Promo',
            'description': 'New promo description.',
            'discount_percentage': 15.00,
            'start_date': timezone.now() + timezone.timedelta(days=1),
            'end_date': timezone.now() + timezone.timedelta(days=5),
            'promo_code': 'NEW15',
            'created_by': self.outlet_user.id 
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Promo.objects.count(), 2)

    def test_update_promo(self):
        self.client.login(username='outlet', password='password')
        response = self.client.post(reverse('promo:update_promo', args=[self.promo.id]), {
            'title': 'Updated Promo',
            'description': 'Updated description.',
            'discount_percentage': 25.00,
            'start_date': timezone.now() + timezone.timedelta(days=2),
            'end_date': timezone.now() + timezone.timedelta(days=7),
            'promo_code': 'UPD25',
            'created_by': self.outlet_user.id 
        })
        self.promo.refresh_from_db()
        self.assertEqual(self.promo.title, 'Updated Promo')
        self.assertEqual(response.status_code, 200)

    def test_delete_promo(self):
        self.client.login(username='outlet', password='password')
        response = self.client.post(reverse('promo:delete_promo', args=[self.promo.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Promo.objects.count(), 0)

    def test_filter_promos(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('promo:filter_promos'), {'filter': 'highest-discount'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('promos', response.json())

    def test_get_promo_details(self):
        response = self.client.get(reverse('promo:get_promo', args=[self.promo.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], self.promo.title)

    def tearDown(self):
        self.promo.delete()
        self.admin_user.delete()
        self.outlet_user.delete()

