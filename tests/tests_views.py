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
        r = self.client.get(reverse('dj-vcn-accounts:list'))
        self.assertEqual(r.status_code, 200)
        self.assertIn("No accounts...", str(r.content))

    def test_posts_list_view_one_post(self):
        """Tests."""
        u = get_user_model().objects.create_user(username="hbuyse",
                                                 password="usermodel",
                                                 first_name="Henri",
                                                 last_name="Buyse")
        r = self.client.get(reverse('dj-vcn-accounts:list'))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(str(r.content).count('<ul>'), 1)
        self.assertEqual(str(r.content).count('<li>'), 1)
        self.assertIn(u.get_full_name(), str(r.content))
        self.assertEqual(str(r.content).count('</li>'), 1)
        self.assertEqual(str(r.content).count('</ul>'), 1)


class TestVcnAccountDetailView(TestCase):
    """Tests DetailView for Post."""

    def test_posts_detail_view_not_existing(self):
        """Tests."""
        r = self.client.get(reverse('dj-vcn-accounts:detail', kwargs={'slug': 'toto'}))
        self.assertEqual(r.status_code, 404)

    def test_posts_detail_view(self):
        """Tests."""
        u = get_user_model().objects.create_user(username="hbuyse",
                                                 password="usermodel",
                                                 first_name="Henri",
                                                 last_name="Buyse")
        r = self.client.get(reverse('dj-vcn-accounts:detail', kwargs={'slug': u.username}))
        self.assertEqual(r.status_code, 200)
        self.assertIn(u.get_full_name(), str(r.content))
        self.assertIn(u.username, str(r.content))


class TestVcnAccountCreateView(TestCase):
    """Tests."""

    def setUp(self):
        """Setup for al the following tests."""
        self.dict = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse"
        }

    def test_posts_create_view_get_as_anonymous(self):
        """Tests."""
        r = self.client.get(reverse('dj-vcn-accounts:create'))
        self.assertEqual(r.status_code, 200)

    def test_posts_create_view_post_as_anonymous(self):
        """Tests."""
        r = self.client.post(reverse('dj-vcn-accounts:create'), self.dict)
        self.assertEqual(r.status_code, 302)
        self.assertIn('/{}'.format(self.dict['username']), r.url)

    def test_posts_create_view_get_as_logged(self):
        """Tests."""
        u = get_user_model().objects.create_user(**self.dict)
        self.assertTrue(self.client.login(username=self.dict['username'],
                                          password=self.dict['password']))

        r = self.client.get(reverse('dj-vcn-accounts:create'))
        self.assertEqual(r.status_code, 302)
        self.assertIn('/{}/update'.format(u.username), r.url)

    def test_posts_create_view_post_as_logged_with_right_permissions(self):
        """Tests."""
        get_user_model().objects.create_user(**self.dict)
        self.assertTrue(self.client.login(username=self.dict['username'],
                                          password=self.dict['password']))

        r = self.client.post(reverse('dj-vcn-accounts:create'), data=self.dict)
        self.assertEqual(r.status_code, 403)


# class TestVcnAccountUpdateView(TestCase):
#     """Tests."""

#     def setUp(self):
#         """Tests."""
#         self.dict = {
#             'username': "hbuyse",
#             'password': "usermodel",
#             'first_name': "Henri",
#             'last_name': "Buyse"
#         }
#         self.user = get_user_model().objects.create_user(**self.dict)

#     def test_posts_update_view_get_as_anonymous(self):
#         """Tests."""
#         r = self.client.get(reverse('dj-vcn-accounts:update', kwargs={'slug': self.user.username}))
#         self.assertEqual(r.status_code, 403)

#     def test_posts_update_view_post_as_anonymous(self):
#         """Tests."""
#         r = self.client.post(reverse('dj-vcn-accounts:update', kwargs={'slug': self.user.username}), self.dict)
#         self.assertEqual(r.status_code, 403)

#     def test_posts_update_view_get_as_logged_not_own_account(self):
#         """Tests."""
#         u = get_user_model().objects.create_user(username="toto", password="toto")
#         self.client.login(username=self.dict['username'], password=self.dict['password'])
#         r = self.client.get(reverse('dj-vcn-accounts:update', kwargs={'slug': u.id}))
#         self.assertEqual(r.status_code, 403)

#     def test_posts_update_view_post_as_logged_not_own_account(self):
#         """Tests."""
#         r = self.client.post(reverse('dj-vcn-accounts:update', kwargs={'slug': self.user.username}), self.dict)
#         self.assertEqual(r.status_code, 302)
#         self.assertIn('/{}'.format(self.user.username), r.url)

#     def test_posts_update_view_get_as_logged_with_right_permissions(self):
#         """Tests."""
#         self.assertTrue(self.user.is_active)
#         self.assertTrue(self.client.login(username="author", password="author"))
#         self.assertFalse(self.user.has_perm('dj-vcn-accounts.change_post'))

#         self.user.user_permissions.add(Permission.objects.get(name='Can change post'))
#         r = self.client.get(reverse('dj-vcn-accounts:update', kwargs={'slug': self.user.username}))
#         self.assertEqual(r.status_code, 200)
#         self.assertEqual(str(r.content).count('<label'), 2)
#         self.assertEqual(str(r.content).count('</label>'), 2)
#         self.assertIn('Post title', str(r.content))
#         self.assertIn('My Title', str(r.content))
#         self.assertIn('Post text', str(r.content))
#         self.assertIn('# Toto', str(r.content))

#     def test_posts_update_view_post_as_logged_with_right_permissions(self):
#         """Tests."""
#         self.assertTrue(self.user.is_active)
#         self.assertTrue(self.client.login(username="author", password="author"))
#         self.assertFalse(self.user.has_perm('dj-vcn-accounts.change_post'))

#         self.user.user_permissions.add(Permission.objects.get(name='Can change post'))
#         self.dict['title'] = 'Toto new'
#         r = self.client.post(reverse('dj-vcn-accounts:update', kwargs={'slug': self.user.username}), data=self.dict)
#         self.assertEqual(r.status_code, 302)
#         self.assertEqual(r.url, reverse('dj-vcn-accounts:detail', kwargs={'slug': p.id}))


# class TestVcnAccountDeleteView(TestCase):
#     """Tests."""

#     def setUp(self):
#         """Tests."""
#         self.user = get_user_model().objects.create_user(username="author", password="author")
#         self.dict = {
#             'title': "My Title",
#             'author': self.user,
#             'text': "## Toto"
#         }
#         self.post = Post.objects.create(**self.dict)

#     def test_posts_delete_view_get_as_anonymous(self):
#         """Tests."""
#         r = self.client.get(reverse('dj-vcn-accounts:delete', kwargs={'slug': self.user.username}))
#         self.assertEqual(r.status_code, 302)
#         self.assertIn('?next=/{}/delete'.format(self.post.id), r.url)

#     def test_posts_delete_view_post_as_anonymous(self):
#         """Tests."""
#         r = self.client.post(reverse('dj-vcn-accounts:delete', kwargs={'slug': self.post.id}), self.dict)
#         self.assertEqual(r.status_code, 302)
#         self.assertIn('?next=/{}/delete'.format(self.post.id), r.url)

#     def test_posts_delete_view_get_as_logged_with_wrong_permissions(self):
#         """Tests."""
#         self.assertTrue(self.user.is_active)
#         self.assertTrue(self.client.login(username="author", password="author"))

#         r = self.client.get(reverse('dj-vcn-accounts:delete', kwargs={'slug': self.post.id}))
#         self.assertEqual(r.status_code, 302)
#         self.assertIn('?next=/{}/delete'.format(self.post.id), r.url)

#     def test_posts_delete_view_post_as_logged_with_wrong_permissions(self):
#         """Tests."""
#         self.assertTrue(self.user.is_active)
#         self.assertTrue(self.client.login(username="author", password="author"))

#         r = self.client.post(reverse('dj-vcn-accounts:delete', kwargs={'slug': self.post.id}), self.dict)
#         self.assertEqual(r.status_code, 302)
#         self.assertIn('?next=/{}/delete'.format(self.post.id), r.url)

#     def test_posts_delete_view_get_as_logged_with_right_permissions(self):
#         """Tests."""
#         self.assertTrue(self.user.is_active)
#         self.assertTrue(self.client.login(username="author", password="author"))
#         self.assertFalse(self.user.has_perm('dj-vcn-accounts.delete_post'))

#         self.user.user_permissions.add(Permission.objects.get(name='Can delete post'))
#         r = self.client.get(reverse('dj-vcn-accounts:delete', kwargs={'slug': self.post.id}))
#         self.assertEqual(r.status_code, 200)
#         self.assertIn("<h1 class=\"float-left\">{}</h1>".format(self.post.title), str(r.content))
#         self.assertIn("<p>Do you really want to delete that post?</p>", str(r.content))

#     def test_posts_delete_view_post_as_logged_with_right_permissions(self):
#         """Tests."""
#         self.assertTrue(self.user.is_active)
#         self.assertTrue(self.client.login(username="author", password="author"))
#         self.assertFalse(self.user.has_perm('dj-vcn-accounts.delete_post'))

#         self.user.user_permissions.add(Permission.objects.get(name='Can delete post'))
#         self.assertEqual(Post.objects.count(), 1)
#         r = self.client.post(reverse('dj-vcn-accounts:delete', kwargs={'slug': self.post.id}))
#         self.assertEqual(Post.objects.count(), 0)
#         self.assertEqual(r.status_code, 302)
#         self.assertEqual(r.url, reverse('dj-vcn-accounts:posts-list'))
