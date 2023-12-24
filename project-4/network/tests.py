from django.test import TestCase
from network.models import User, Profile, Following, Post, Comment

class NetworkTestCase(TestCase):

    def setUp(self):
        # Create Users.
        user1 = User.objects.create_user(username="user1", password="password")
        user2 = User.objects.create_user(username="user2", password="password")
        user3 = User.objects.create_user(username="user3", password="password")
        user4 = User.objects.create_user(username="user4", password="password")
        user5 = User.objects.create_user(username="user5", password="password")
        # Create Profiles
        profile1 = Profile.objects.create(user=user1, name="user1name", bio="this is some text")
        profile2 = Profile.objects.create(user=user2, name="user2name", bio="this is some text")
        profile3 = Profile.objects.create(user=user3, name="user3name", bio="this is some text")
        profile4 = Profile.objects.create(user=user4, name="user4name", bio="this is some text")
        profile5 = Profile.objects.create(user=user5, name="user5name", bio="this is some text")
        # Create User 2 Followers
        follow1 = Following.objects.create(user=user1, user_followed=user2)
        follow2 = Following.objects.create(user=user3, user_followed=user2)
        follow3 = Following.objects.create(user=user4, user_followed=user2)
        follow4 = Following.objects.create(user=user5, user_followed=user2)
        # Create User 2 Following
        follow5 = Following.objects.create(user=user2, user_followed=user3)
        follow6 = Following.objects.create(user=user2, user_followed=user4)
        # Create Posts
        post1 = Post.objects.create(user=user1, body="I love tennis!", likes=5)
        post2 = Post.objects.create(user=user2, body="Test 1", likes=3)
        post3 = Post.objects.create(user=user2, body="Test 2", likes=7)
        # Create Comments
        comment1 = Comment.objects.create(user=user1, post=post1, body="I also like tennis!")
    
    def test_profile(self):
        user3 = User.objects.get(username="user3")
        name = user3.profile.name
        self.assertEqual(name, 'user3name') # Test user 3 profile name

    def test_number_followers(self):
        user2 = User.objects.get(username="user2")
        followers_count = Following.objects.filter(user_followed=user2).count()
        self.assertEqual(followers_count, 4) # Test user 2 number of followers

    def test_number_following(self):
        user2 = User.objects.get(username="user2")
        following_count = Following.objects.filter(user=user2).count()
        self.assertEqual(following_count, 2) #Test user 2 number of users they're following

    def test_post(self):
        user1 = User.objects.get(username="user1")
        post = Post.objects.get(user=user1)
        self.assertEqual(post.body, "I love tennis!")
        self.assertEqual(post.likes, 5)

    def test_post_count(self):
        user2 = User.objects.get(username="user2")
        post_count = Post.objects.filter(user=user2).count()
        self.assertEqual(post_count, 2)
    
    def test_comment(self):
        user1 = User.objects.get(username="user1")
        post1 = Post.objects.get(user=user1)
        comment_for_post1 = post1.comments.first()
        self.assertEqual(comment_for_post1.body, "I also like tennis!")

    

    
    

    