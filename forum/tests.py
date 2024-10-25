from django.test import TestCase, Client
from account.models import User
from forum.models import Forum
from django.urls import reverse
import uuid


class ForumModelTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='12345')
        self.user2 = User.objects.create_user(username='testuser2', password='12345')

        self.parent_forum = Forum.objects.create(
            user=self.user1,
            title='Parent Forum',
            details='This is a parent forum.'
        )

        self.child_forum = Forum.objects.create(
            user=self.user1,
            title='Child Forum',
            details='This is a child forum.',
            parent=self.parent_forum
        )

    def test_forum_creation(self):
        self.assertEqual(self.parent_forum.title, 'Parent Forum')
        self.assertEqual(self.parent_forum.details, 'This is a parent forum.')
        self.assertEqual(self.parent_forum.user, self.user1)

        self.assertEqual(self.child_forum.title, 'Child Forum')
        self.assertEqual(self.child_forum.details, 'This is a child forum.')
        self.assertEqual(self.child_forum.parent, self.parent_forum)

    def test_forum_parent_child_relationship(self):
        self.assertIn(self.child_forum, self.parent_forum.subforum.all())

    def test_forum_str(self):
        self.assertEqual(str(self.parent_forum), 'Parent Forum')
        self.assertEqual(str(self.child_forum), 'Child Forum')

    def test_forum_uuid(self):
        self.assertIsInstance(self.parent_forum.id, uuid.UUID)
        self.assertIsInstance(self.child_forum.id, uuid.UUID)
    
    def test_forum_invalid_fields(self) :
        forum_invalid = Forum.objects.create(
            user=self.user1,
            title='Forum Dummy',
            details='This is a Forum dummy.' 
        )
        
        with self.assertRaises(ValueError) as ve:
            forum_invalid.user = self.user1
            forum_invalid.parent = "Parent"
            forum_invalid.full_clean()
        self.assertEqual(ve.exception.args[0], 'Cannot assign "\'Parent\'": "Forum.parent" must be a "Forum" instance.')
        
        with self.assertRaises(ValueError) as ve:
            forum_invalid.user = "USER"
            forum_invalid.full_clean()
        self.assertEqual(ve.exception.args[0], 'Cannot assign "\'USER\'": "Forum.user" must be a "User" instance.')
        
        
    def test_add_forum(self) :
        c = Client()
        
        url = reverse('forum:add_forum_entry_ajax')
        
        # can only use POST
        self.assertEqual(c.get(url).status_code, 405)
        self.assertEqual(c.put(url).status_code, 405)
        self.assertEqual(c.patch(url).status_code, 405)
        self.assertEqual(c.head(url).status_code, 405)
    
        # Unauthorized, getting redirected to login page
        self.assertEqual(c.post(url, {"title": "Forum Title", "details": "Forum Details"}).status_code, 302)
        
        c.login(username='testuser1', password='12345')
        
        # Success Add New Parent Forum
        self.assertEqual(c.post(url, {"title": "Forum Title", "details": "Forum Details"}).status_code, 201)
        
        # Success Add New Child Forum
        self.assertEqual(c.post(url, {"title": "Forum Title", "details": "Forum Details", "parent":self.parent_forum.id}).status_code, 201)
        
        # parent not found
        self.assertEqual(c.post(url, {"title": "Forum Title", "details": "Forum Details", "parent":self.user1.id}).status_code, 404)
        
    def test_edit_forum(self) :
        
        c = Client()
        
        url_add = reverse('forum:add_forum_entry_ajax')
        url_edit = reverse('forum:edit_forum')
        
        # can only use POST
        self.assertEqual(c.get(url_edit).status_code, 405)
        self.assertEqual(c.put(url_edit).status_code, 405)
        self.assertEqual(c.patch(url_edit).status_code, 405)
        self.assertEqual(c.head(url_edit).status_code, 405)
    
        # Unauthorized, getting redirected to login page
        self.assertEqual(c.post(url_edit, {"title": "Forum Title", "details": "Forum Details"}).status_code, 302)
        
        # login
        c.login(username='testuser1', password='12345')
        
        # needed fields
        needed_fields = {
            "title": "Forum Title Changed",
            "details": "Forum Details Changed",
            "pk": self.parent_forum.id,
            }
        
        # Success Add New Parent Forum
        self.assertEqual(c.post(url_edit, needed_fields).status_code, 201)
        
        # not found
        needed_fields["pk"] = "f8ac2b32-4cef-4da8-8068-35cc87bf2c55"
        self.assertEqual(c.post(url_edit, needed_fields).status_code, 404)
        needed_fields["pk"] = self.parent_forum.id
        
        # switch user
        c.logout()
        c.login(username='testuser2', password='12345')
        
        # Unauthorized, only the owner can edit
        self.assertEqual(c.post(url_edit, needed_fields).status_code, 401)
        
        
    def test_delete_forum(self) :
        
        c = Client()
        
        url_delete = reverse('forum:delete_forum')
        
        # can only use POST
        self.assertEqual(c.get(url_delete).status_code, 405)
        self.assertEqual(c.put(url_delete).status_code, 405)
        self.assertEqual(c.patch(url_delete).status_code, 405)
        self.assertEqual(c.head(url_delete).status_code, 405)
    
        # Unauthorized, getting redirected to login page
        self.assertEqual(c.post(url_delete, {"title": "Forum Title", "details": "Forum Details"}).status_code, 302)
        
        # login
        c.login(username='testuser1', password='12345')
        
        # needed fields
        dummy_forum = Forum.objects.create(user=self.user1,title='Dummy Forum',details='This is a dummy forum.')
        needed_fields = {
            "pk": dummy_forum.id,
            }
        
        # Success Add New Parent Forum
        self.assertEqual(c.post(url_delete, needed_fields).status_code, 201)
        
        # not found
        self.assertEqual(c.post(url_delete, needed_fields).status_code, 404)
        dummy_forum = Forum.objects.create(user=self.user1,title='Dummy Forum',details='This is a dummy forum.')
        needed_fields = {
            "pk": dummy_forum.id,
            }
        
        # switch user
        c.logout()
        c.login(username='testuser2', password='12345')
        
        # Unauthorized, only the owner can edit
        self.assertEqual(c.post(url_delete, needed_fields).status_code, 401)

    