from django.test import TestCase
from django.contrib.auth import get_user_model
from forum.models import Forum
import uuid

User = get_user_model()

class ForumModelTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='12345')

        # Create a parent forum
        self.parent_forum = Forum.objects.create(
            user=self.user,
            title='Parent Forum',
            details='This is a parent forum.'
        )

        # Create a child forum
        self.child_forum = Forum.objects.create(
            user=self.user,
            title='Child Forum',
            details='This is a child forum.',
            parent=self.parent_forum
        )

    def test_forum_creation(self):
        # Test parent forum creation
        self.assertEqual(self.parent_forum.title, 'Parent Forum')
        self.assertEqual(self.parent_forum.details, 'This is a parent forum.')
        self.assertEqual(self.parent_forum.user, self.user)

        # Test child forum creation
        self.assertEqual(self.child_forum.title, 'Child Forum')
        self.assertEqual(self.child_forum.details, 'This is a child forum.')
        self.assertEqual(self.child_forum.parent, self.parent_forum)

    def test_forum_parent_child_relationship(self):
        # Test parent-child relationship
        self.assertIn(self.child_forum, self.parent_forum.subforum.all())

    def test_forum_str(self):
        # Test the __str__ method
        self.assertEqual(str(self.parent_forum), 'Parent Forum')
        self.assertEqual(str(self.child_forum), 'Child Forum')

    def test_forum_uuid(self):
        # Test that the forum UUID is generated
        self.assertIsInstance(self.parent_forum.id, uuid.UUID)
        self.assertIsInstance(self.child_forum.id, uuid.UUID)
