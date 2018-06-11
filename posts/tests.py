from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import login
from django.contrib import auth
from django.contrib.auth.models import User

from .models import Post, Comment, Tag


def create_post(title, text):
    return Post.objects.create(title=title, text=text)


class PostModelTests(TestCase):
    def test_post_with_no_tag(self):
        post = create_post("test my post", "lalala")
        self.assertQuerysetEqual(post.tag.all(), [])

    def test_post_with_tag(self):
        tag = Tag.objects.create(name="tag name")
        post = create_post("test my post", "lalala")
        post.tag.add(tag)
        self.assertIn(tag, post.tag.all())


class IndexViewTests(TestCase):
    def test_display_posts(self):
        create_post("test my post", "lalala")
        create_post("test again", "lululu")

        response = self.client.get(reverse('posts:index'))
        self.assertQuerysetEqual(
            response.context['post_list'],
            ['<Post: test my post>', '<Post: test again>'],
            ordered=False
        )

    def test_no_posts(self):
        response = self.client.get(reverse('posts:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No posts yet.")
        self.assertQuerysetEqual(response.context['post_list'], [])


class DetailViewTests(TestCase):
    def test_redirect_on_successful_post_comment(self):
        post = create_post("test my post", "lalala")
        post_data = {'text': 'test comment'}
        response = self.client.post(reverse('posts:detail', kwargs={'post_id': post.id}), post_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('posts:detail', kwargs={'post_id': post.id}))

    def test_create_comment_on_successful_post_comment(self):
        post = create_post("test my post", "lalala")
        post_data = {'text': 'test comment'}
        self.client.post(reverse('posts:detail', kwargs={'post_id': post.id}), post_data)

        self.assertQuerysetEqual(post.comment_set.all(), ['<Comment: test comment>'])

    def test_display_posted_comment(self):
        post = create_post("test my post", "lalala")
        Comment.objects.create(post=post, text="test comment")
        response = self.client.get(reverse('posts:detail', kwargs={'post_id': post.id}))

        self.assertQuerysetEqual(response.context['post'].comment_set.all(), ['<Comment: test comment>'])

    def test_comment_from_anomynous_user(self):
        post = create_post("test my post", "lalala")
        post_data = {'text': 'my comment for test'}
        self.client.post(reverse('posts:detail', kwargs={'post_id': post.id}), post_data)

        self.assertEqual(post.comment_set.get(text='my comment for test').user, None)

    def test_comment_from_logged_in_user(self):
        post = create_post("test my post", "lalala")
        post_data = {'text': 'my comment for test'}
        user = User.objects.create_user("testuser", "test@test.com", "12345678")
        self.client.login(username="testuser", password="12345678")

        self.client.post(reverse('posts:detail', kwargs={'post_id': post.id}), post_data)
        self.assertEqual(post.comment_set.get(text='my comment for test').user, user)
