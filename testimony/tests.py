from django.test import TestCase
from django.urls import reverse
from stores.models import Store, Category
from account.models import User
from testimony.models import Testimony

class TestimonyViewTests(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.user.role = 1  # Set role to normal user
        self.user.save()

        # Create a category
        self.category = Category.objects.create(name='Test')

        # Create a store
        self.store = Store.objects.create(
            user=self.user,
            brand='brand',
            description='Description',
            address='Address',
            contact_number='123456789',
            website='http://a.com',
            social_media='http://facebook.com/a'
        )
        self.store.categories.add(self.category)

        self.testimony = Testimony.objects.create(
            testimony='Bagus!',
            rating=4,
            userId=self.user,
            storeId=self.store
        )

    def test_show_testimony_by_merchant(self):
        response = self.client.get(reverse('testimony:show_testimony_by_merchant', args=[self.store.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_testimony.html')

    def test_show_testimony_by_merchant_json(self):
        response = self.client.get(reverse('testimony:show_testimony', args=[self.store.pk]))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['testimony'], 'Bagus!')

    def test_get_merchant_rating(self):
        response = self.client.get(reverse('testimony:get_rating', args=[self.store.pk]))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['rating'], 4)

    def test_create_new_testimony_authenticated(self):
        self.client.login(username='testuser', password='pass')
        response = self.client.post(reverse('testimony:create_new_testimony'), {
            'testimony': 'Awesome!',
            'rating': 5,
            'store_id': self.store.pk
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Testimony.objects.filter(testimony='Awesome!').exists())

    def test_create_new_testimony_invalid_rating(self):
        self.client.login(username='testuser', password='pass')
        response = self.client.post(reverse('testimony:create_new_testimony'), {
            'testimony': 'Awesome!',
            'rating': 10,  
            'store_id': self.store.pk
        })
        self.assertEqual(response.status_code, 400)

    def test_delete_testimony_authenticated(self):
        self.client.login(username='testuser', password='pass')
        response = self.client.delete(reverse('testimony:delete_testimony', args=[self.testimony.pk]))
        # Log in the user
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Testimony.objects.filter(pk=self.testimony.pk).exists())

    def test_delete_testimony_not_found(self):
        self.client.login(username='testuser', password='pass')
        response = self.client.delete(reverse('testimony:delete_testimony', args=[9999]))  # Non-existing ID
        self.assertEqual(response.status_code, 404)

