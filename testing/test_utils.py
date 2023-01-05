from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User, AnonymousUser
from audio_app.utils import *
from audio_app.forms import playlist_form
from django.contrib.auth.models import Group

class isAdminUtil(TestCase):
    def setUp(self):
        '''
        tests the is_admin util
        '''
        self.username = 'testuser'
        self.password = 'securepassword230923!'
        self.credentials = {
            'username': self.username,
            'password': self.password
        }
        self.user = User.objects.create_user(**self.credentials)
        self.user2 = User.objects.create_user({'username': 'other_user','password': self.password})
        adminGroup, _ = Group.objects.get_or_create(name='Admin')
        adminGroup.user_set.add(self.user)

    def test_returns_true_if_admin(self):
        self.assertTrue(is_admin(self.user))

    def test_returns_false_if_not_admin(self):
        self.assertFalse(is_admin(self.user2))


class getPlaylistsUtil(TestCase):
    def setUp(self):
        '''
        test the get_playlists util
        '''
        self.factory = RequestFactory()
        self.username = 'testuser'
        self.password = 'securepassword230923!'
        self.credentials = {
            'username': self.username,
            'password': self.password
        }
        self.user = User.objects.create_user(**self.credentials)

    def test_unauthenticated_correct(self):
        request = self.factory.get('/') # request type shouldnt matter, just if they are authenticated
        request.user = AnonymousUser()
        res = get_playlists(request)
        self.assertEqual(type(res), dict)
        self.assertTrue('userPlaylists' in res)
        self.assertEqual(res['userPlaylists'], [])

    def test_authenticated_correct_no_playlist(self):
        request = self.factory.get('/') # request type shouldnt matter, just if they are authenticated
        request.user = self.user
        res = get_playlists(request)
        self.assertEqual(type(res), dict)
        self.assertTrue('userPlaylists' in res)
        self.assertQuerysetEqual(res['userPlaylists'], [])

    def test_authenticated_correct_with_playlist(self):
        request = self.factory.get('/') # request type shouldnt matter, just if they are authenticated
        request.user = self.user
        # create a playlist
        post_dict1 = {'name': 'Test Title1', 'owner':self.user}
        form1 = playlist_form(post_dict1)
        self.playlist1 = form1.save(commit=False)
        self.playlist1.owner = self.user
        self.playlist1.save()
        res = get_playlists(request)
        self.assertEqual(type(res), dict)
        self.assertTrue('userPlaylists' in res)
        self.assertQuerysetEqual(res['userPlaylists'], [self.playlist1]) # works for user with playlist