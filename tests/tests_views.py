#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class TestVcnAccountListView(TestCase):
    """Tests ListView for Post."""

    def test_posts_list_view_empty(self):
        """Tests."""
        r = self.client.get(reverse('dj-vcn-accounts:posts-list'))
        self.assertEqual(r.status_code, 200)
        self.assertIn("No posts...", str(r.content))

    def test_posts_list_view_one_post(self):
        """Tests."""
        get_user_model().objects.create_user(username="author", password="author", first_name="Henri", last_name="Buyse")
        r = self.client.get(reverse('dj-vcn-accounts:list', kwargs={'pk': 1}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(str(r.content).count('<ul>'), 1)
        self.assertEqual(str(r.content).count('<li>'), 1)
        self.assertIn("Toto", str(r.content))
        self.assertEqual(str(r.content).count('</li>'), 1)
        self.assertEqual(str(r.content).count('</ul>'), 1)


class TestVcnAccountDetailView(TestCase):
    """Tests DetailView for Post."""

    def setUp(self):
        """Tests."""
        self.user = get_user_model().objects.create_user(username="author", password="author")

    def test_posts_detail_view_not_existing(self):
        """Tests."""
        r = self.client.get(reverse('dj-vcn-accounts:detail', kwargs={'pk': 1}))
        self.assertEqual(r.status_code, 404)

    def test_posts_detail_view(self):
        """Tests."""
        p = Post.objects.create(title="My Title", author=self.user, text="## Toto")
        r = self.client.get(reverse('dj-vcn-accounts:detail', kwargs={'pk': p.id}))
        self.assertEqual(r.status_code, 200)
        self.assertIn("Toto", str(r.content))
        session = self.client.session
        self.assertIn('post_pk', session)
        self.assertEqual(session['post_pk'], p.id)


class TestVcnAccountCreateView(TestCase):
    """Tests."""

    def setUp(self):
        """Tests."""
        self.user = get_user_model().objects.create_user(username="author", password="author")
        self.dict = {
            'title': "My Title",
            'text': "## Toto"
        }

    def test_posts_create_view_get_as_anonymous(self):
        """Tests."""
        r = self.client.get(reverse('dj-vcn-accounts:create'))
        self.assertEqual(r.status_code, 302)
        self.assertIn('?next=/create', r.url)

    def test_posts_create_view_post_as_anonymous(self):
        """Tests."""
        r = self.client.post(reverse('dj-vcn-accounts:create'), self.dict)
        self.assertEqual(r.status_code, 302)
        self.assertIn('?next=/create', r.url)

    def test_posts_create_view_get_as_logged_with_wrong_permissions(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))

        r = self.client.get(reverse('dj-vcn-accounts:create'))
        self.assertEqual(r.status_code, 302)
        self.assertIn('?next=/create', r.url)

    def test_posts_create_view_post_as_logged_with_wrong_permissions(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))

        r = self.client.post(reverse('dj-vcn-accounts:create'), self.dict)
        self.assertEqual(r.status_code, 302)
        self.assertIn('?next=/create', r.url)

    def test_posts_create_view_get_as_logged_with_right_permissions(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))
        self.assertFalse(self.user.has_perm('dj-vcn-accounts.add_post'))

        self.user.user_permissions.add(Permission.objects.get(name='Can add post'))
        r = self.client.get(reverse('dj-vcn-accounts:create'))
        self.assertEqual(r.status_code, 200)

    def test_posts_create_view_post_as_logged_with_right_permissions(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))
        self.assertFalse(self.user.has_perm('dj-vcn-accounts.add_post'))

        self.user.user_permissions.add(Permission.objects.get(name='Can add post'))
        r = self.client.post(reverse('dj-vcn-accounts:create'), data=self.dict)
        p = Post.objects.last()
        self.assertEqual(p.title, "My Title")
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, reverse('dj-vcn-accounts:detail', kwargs={'pk': p.id}))


class TestVcnAccountUpdateView(TestCase):
    """Tests."""

    def setUp(self):
        """Tests."""
        self.user = get_user_model().objects.create_user(username="author", password="author")
        self.dict = {
            'title': "My Title",
            'author': self.user,
            'text': "## Toto"
        }
        self.post = Post.objects.create(**self.dict)

    def test_posts_update_view_get_as_anonymous(self):
        """Tests."""
        r = self.client.get(reverse('dj-vcn-accounts:update', kwargs={'pk': self.post.id}))
        self.assertEqual(r.status_code, 302)
        self.assertIn('?next=/{}/update'.format(self.post.id), r.url)

    def test_posts_update_view_post_as_anonymous(self):
        """Tests."""
        r = self.client.post(reverse('dj-vcn-accounts:update', kwargs={'pk': self.post.id}), self.dict)
        self.assertEqual(r.status_code, 302)
        self.assertIn('?next=/{}/update'.format(self.post.id), r.url)

    def test_posts_update_view_get_as_logged_with_wrong_permissions(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))

        r = self.client.get(reverse('dj-vcn-accounts:update', kwargs={'pk': self.post.id}))
        self.assertEqual(r.status_code, 302)
        self.assertIn('?next=/{}/update'.format(self.post.id), r.url)

    def test_posts_update_view_post_as_logged_with_wrong_permissions(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))

        r = self.client.post(reverse('dj-vcn-accounts:update', kwargs={'pk': self.post.id}), self.dict)
        self.assertEqual(r.status_code, 302)
        self.assertIn('?next=/{}/update'.format(self.post.id), r.url)

    def test_posts_update_view_get_as_logged_with_right_permissions(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))
        self.assertFalse(self.user.has_perm('dj-vcn-accounts.change_post'))

        self.user.user_permissions.add(Permission.objects.get(name='Can change post'))
        r = self.client.get(reverse('dj-vcn-accounts:update', kwargs={'pk': self.post.id}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(str(r.content).count('<label'), 2)
        self.assertEqual(str(r.content).count('</label>'), 2)
        self.assertIn('Post title', str(r.content))
        self.assertIn('My Title', str(r.content))
        self.assertIn('Post text', str(r.content))
        self.assertIn('# Toto', str(r.content))

    def test_posts_update_view_post_as_logged_with_right_permissions(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))
        self.assertFalse(self.user.has_perm('dj-vcn-accounts.change_post'))

        self.user.user_permissions.add(Permission.objects.get(name='Can change post'))
        self.dict['title'] = 'Toto new'
        r = self.client.post(reverse('dj-vcn-accounts:update', kwargs={'pk': self.post.id}), data=self.dict)
        p = Post.objects.get(id=self.post.id)
        self.assertEqual(p.title, "Toto new")
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, reverse('dj-vcn-accounts:detail', kwargs={'pk': p.id}))


class TestVcnAccountDeleteView(TestCase):
    """Tests."""

    def setUp(self):
        """Tests."""
        self.user = get_user_model().objects.create_user(username="author", password="author")
        self.dict = {
            'title': "My Title",
            'author': self.user,
            'text': "## Toto"
        }
        self.post = Post.objects.create(**self.dict)

    def test_posts_delete_view_get_as_anonymous(self):
        """Tests."""
        r = self.client.get(reverse('dj-vcn-accounts:delete', kwargs={'pk': self.post.id}))
        self.assertEqual(r.status_code, 302)
        self.assertIn('?next=/{}/delete'.format(self.post.id), r.url)

    def test_posts_delete_view_post_as_anonymous(self):
        """Tests."""
        r = self.client.post(reverse('dj-vcn-accounts:delete', kwargs={'pk': self.post.id}), self.dict)
        self.assertEqual(r.status_code, 302)
        self.assertIn('?next=/{}/delete'.format(self.post.id), r.url)

    def test_posts_delete_view_get_as_logged_with_wrong_permissions(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))

        r = self.client.get(reverse('dj-vcn-accounts:delete', kwargs={'pk': self.post.id}))
        self.assertEqual(r.status_code, 302)
        self.assertIn('?next=/{}/delete'.format(self.post.id), r.url)

    def test_posts_delete_view_post_as_logged_with_wrong_permissions(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))

        r = self.client.post(reverse('dj-vcn-accounts:delete', kwargs={'pk': self.post.id}), self.dict)
        self.assertEqual(r.status_code, 302)
        self.assertIn('?next=/{}/delete'.format(self.post.id), r.url)

    def test_posts_delete_view_get_as_logged_with_right_permissions(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))
        self.assertFalse(self.user.has_perm('dj-vcn-accounts.delete_post'))

        self.user.user_permissions.add(Permission.objects.get(name='Can delete post'))
        r = self.client.get(reverse('dj-vcn-accounts:delete', kwargs={'pk': self.post.id}))
        self.assertEqual(r.status_code, 200)
        self.assertIn("<h1 class=\"float-left\">{}</h1>".format(self.post.title), str(r.content))
        self.assertIn("<p>Do you really want to delete that post?</p>", str(r.content))

    def test_posts_delete_view_post_as_logged_with_right_permissions(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))
        self.assertFalse(self.user.has_perm('dj-vcn-accounts.delete_post'))

        self.user.user_permissions.add(Permission.objects.get(name='Can delete post'))
        self.assertEqual(Post.objects.count(), 1)
        r = self.client.post(reverse('dj-vcn-accounts:delete', kwargs={'pk': self.post.id}))
        self.assertEqual(Post.objects.count(), 0)
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, reverse('dj-vcn-accounts:posts-list'))
