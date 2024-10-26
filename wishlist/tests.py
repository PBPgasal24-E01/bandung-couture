# tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from stores.models import Store, Category
from wishlist.models import Wishlist

User  = get_user_model()

class WishlistTests(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user.role = 1  # Set role to normal user
        self.user.save()

        # Create a category
        self.category = Category.objects.create(name='Test Category')

        # Create a store
        self.store = Store.objects.create(
            user=self.user,
            brand='Test Store',
            description='Test Description',
            address='Test Address',
            contact_number='123456789',
            website='http://teststore.com',
            social_media='http://facebook.com/teststore'
        )
        self.store.categories.add(self.category)

    def test_add_to_wishlist(self):
        # Log in the user
        self.client.login(username='testuser', password='testpass')

        # Add store to wishlist
        response = self.client.post(reverse('wishlist:add', kwargs={'store_id': self.store.id}))
        self.assertEqual(response.status_code, 200)

        # Check if the store is in the wishlist
        wishlist_item = Wishlist.objects.get(user=self.user, store=self.store)
        self.assertIsNotNone(wishlist_item)

    def test_remove_from_wishlist(self):
        # Log in the user
        self.client.login(username='testuser', password='testpass')

        # Add store to wishlist first
        Wishlist.objects.create(user=self.user, store=self.store)

        # Remove store from wishlist
        response = self.client.post(reverse('wishlist:remove', kwargs={'store_id': self.store.id}))
        self.assertEqual(response.status_code, 200)

        # Check if the store is removed from the wishlist
        with self.assertRaises(Wishlist.DoesNotExist):
            Wishlist.objects.get(user=self.user, store=self.store)

    def test_show_button_redirect(self):
        # Log in the user
        self.client.login(username='testuser', password='testpass')

        # Add store to wishlist
        Wishlist.objects.create(user=self.user, store=self.store)

        # Check if the button redirects to the store's show page
        response = self.client.get(reverse('wishlist:view'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse('stores:show'))

    def test_ajax_add_to_wishlist(self):
        # Log in the user
        self.client.login(username='testuser', password='testpass')

        # Simulate AJAX request to add to wishlist
        response = self.client.post(reverse('wishlist:add', kwargs={'store_id': self.store.id}), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

        # Ensure the store is in the wishlist
        self.assertTrue(Wishlist.objects.filter(user=self.user, store=self.store).exists())

    def test_ajax_remove_from_wishlist(self):
        # Log in the user
        self.client.login(username='testuser', password='testpass')

        # Add store to wishlist first
        Wishlist.objects.create(user=self.user, store=self.store)

        # Simulate AJAX request to remove from wishlist
        response = self.client.post(reverse('wishlist:remove', kwargs={'store_id': self.store.id}), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

        # Ensure the store is removed from the wishlist
        self.assertFalse(Wishlist.objects.filter(user=self.user, store=self.store).exists())

    def test_filter_by_category(self):
        # Log in the user
        self.client.login(username='testuser', password='testpass')

        # Add store to wishlist
        Wishlist.objects.create(user=self.user, store=self.store)

        # Filter by category
        response = self.client.get(reverse('wishlist:filter', kwargs={'category_id': self.category.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Store')
