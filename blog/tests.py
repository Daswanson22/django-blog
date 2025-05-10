import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

from .models import UserProfile, Post

def create_user(username, email, password):
    return User(username, email, password)

class UserProfileTests(TestCase):
    def test_has_a_favorite_team_that_exists(self):
        """
        Should return true if the  UserProfile has a favorite
        team that exists in the league.
        """
        teams = UserProfile._meta.get_field('favorite_team').choices
        favorite_team = teams[1]

        self.assertIn(favorite_team, teams)

    def test_favorite_team_does_not_exist(self):
        """
        Should return true if the team is not in the favorite team
        choices.
        """
        teams = UserProfile._meta.get_field('favorite_team').choices
        favorite_team = ('DIA', 'Durango Yetis')

        self.assertNotIn(favorite_team, teams)

    def test_user_has_favorite_team(self):
        """
        Should return true if the user has set their favorite team
        """
        user = User.objects.create_user(
            username="Dylan",
            email="dylan@mail.com",
            password="password123"
        )
        user_profile = UserProfile(user, ('ARI', 'Arizona Diamonbacks'))
        favorite_team = user_profile.favorite_team
        self.assertIsNotNone(favorite_team)

    def test_user_has_no_favorite_team(self):
        """
        Should return true if the user has not set their favorite team
        """
        user = User.objects.create_user(
            username="Dylan",
            email="dylan@mail.com",
            password="password123"
        )
        user_profile = UserProfile(user, None)
        favorite_team = user_profile.favorite_team
        self.assertEqual(favorite_team, '')

class PostModelTests(TestCase):
    def test_post_was_published_recently(self):
        """
        was_published_recently() returns False for posts
        whose published_date is in the future
        """
        time = timezone.now() - datetime.timedelta(days=30)
        future_post = Post(title="Hello", text="Hello, to all the mlb fans", published_date=time)
        self.assertIs(future_post.was_published_recently(), False)

    def test_post_was_published_recently_with_old_post(self):
        """
        was_published_recently() returns False for posts
        whose published_date is older than one day
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_post = Post(title="Hello", text="Hello, to all the mlb fans", published_date=time)
        self.assertIs(old_post.was_published_recently(), False)

    def test_post_not_published_before_creation_time(self):
        """
        Should return True if the (published_date) is
        after the current time (now)
        """
        now = timezone.now()
        pub_date = timezone.now() - datetime.timedelta(days=2, seconds=12)
        new_post = Post(title="hellow", text="Whats up fam?", published_date=pub_date)
        self.assertGreaterEqual(now, new_post.published_date)

    def test_post_has_slug(self):
        """
        Should return True if the post has a slug
        """
        user = User.objects.create(username="testuser", password="password")
        user.save()
        post = Post(author=user, title="Hello", text="Hello, to all the mlb fans")
        post.save()
        self.assertIsNotNone(post.slug)

class PostListViewTests(TestCase):
    def test_post_list_view_with_no_posts(self):
        """
        If no posts exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['message'], "No posts are available.")
        self.assertQuerySetEqual(response.context['posts'], [])

    def test_post_list_view_with_posts(self):
        """
        If posts exist, they should be displayed in the post list view.
        """
        user = User.objects.create_user(username='testuser', password='password')
        post = Post.objects.create(author=user, title='Test Post', text='This is a test post.')
        post.publish()
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, post)

    def test_post_list_view_with_oldest_query(self):
        """
        If the query is 'oldest', posts should be ordered by published_date ascending.
        """
        user = User.objects.create_user(username='testuser', password='password')
        post1 = Post.objects.create(author=user, title='Test Post 1', text='This is a test post 1.')
        post2 = Post.objects.create(author=user, title='Test Post 2', text='This is a test post 2.')
        post1.publish()
        post2.publish()
        response = self.client.get(reverse('blog:post_list') + '?q=oldest')
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['posts'], [post1, post2], ordered=False)

    def test_post_list_view_with_invalid_query(self):
        """
        If the query is invalid, posts should be ordered by published_date descending.
        """
        user = User.objects.create_user(username='testuser', password='password')
        post1 = Post.objects.create(author=user, title='Test Post 1', text='This is a test post 1.')
        post2 = Post.objects.create(author=user, title='Test Post 2', text='This is a test post 2.')
        post1.publish()
        post2.publish()
        response = self.client.get(reverse('blog:post_list') + '?q=invalid_query')
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['posts'], [post2, post1], ordered=False)

class PostDetailViewTests(TestCase):
    def test_post_detail_view_with_valid_slug(self):
        """
        If the slug is valid, the post detail view should display the post.
        """
        user = User.objects.create_user(username='testuser', password='password')
        post = Post.objects.create(author=user, title='Test Post', text='This is a test post.')
        post.publish()
        response = self.client.get(reverse('blog:post_detail', args=[post.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, post.title)
        self.assertContains(response, post.text)
        self.assertContains(response, post.author.username)

    def test_post_detail_view_is_published(self):
        """
        Should return True if the post is published
        """
        user = User.objects.create_user(username='testuser', password='password')
        post = Post.objects.create(author=user, title='Test Post', text='This is a test post.')
        post.publish()
        response = self.client.get(reverse('blog:post_detail', args=[post.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(post.published_date)

    def test_post_detail_view_is_not_published(self):
        """
        Should return False if the post is not published
        """
        user = User.objects.create_user(username='testuser', password='password')
        post = Post.objects.create(author=user, title='Test Post', text='This is a test post.')
        response = self.client.get(reverse('blog:post_detail', args=[post.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(post.published_date)
        self.assertContains(response, "This post has not been published yet.")

    def test_post_detail_view_has_author(self):
        """
        Should return True if the post has an author
        """
        user = User.objects.create_user(username='testuser', password='password')
        post = Post.objects.create(author=user, title='Test Post', text='This is a test post.')
        self.assertIsNotNone(post.author)

class PostUpvoteViewTests(TestCase):
    def test_upvote_post(self):
        """
        Should return True if the post is upvoted
        """
        user = User.objects.create_user(username='testuser', password='password')
        post = Post.objects.create(author=user, title='Test Post', text='This is a test post.')
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('blog:upvote', args=[post.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn(user, post.upvotes.all())

    def test_remove_upvote_post(self):
        """
        Should return False if the post is unvote
        Must call the upvote view twice to remove the upvote
        1. First call adds the user to upvotes
        2. Second call removes the user from upvotes
        3. The user should not be in the upvotes list after the second call
        """
        user = User.objects.create_user(username='testuser', password='password')
        post = Post.objects.create(author=user, title='Test Post', text='This is a test post.')
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('blog:upvote', args=[post.pk]))
        downvote_response = self.client.post(reverse('blog:upvote', args=[post.pk]))
        self.assertEqual(downvote_response.status_code, 302)
        self.assertNotIn(user, post.upvotes.all())

    def test_upvote_without_login(self):
        """
        Should redirect to signup page if the user is not logged in
        """
        user = User.objects.create_user(username='testuser', password='password')
        post = Post.objects.create(author=user, title='Test Post', text='This is a test post.')
        response = self.client.post(reverse('blog:upvote', args=[post.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('blog:signup'))

