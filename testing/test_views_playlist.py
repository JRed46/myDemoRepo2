from django.test import TestCase
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from audio_app.models import audio_object, playlist
from audio_app.forms import audio_object_form, playlist_form, add_to_playlist_form
from django.core.files.uploadedfile import SimpleUploadedFile


#########################
# PLAYLIST LISTEN VIEWS #    # playlist related view functions
#########################

class unauthenticated_createPlaylistView(TestCase):
    def setUp(self):
        '''
        Create a playlist should be restricted to authenticated user.
        Checks no playlist can be created by unauthenticated users.
        '''
        pass

    def test_user_not_authenticated(self):
        response = self.client.get('/')
        self.assertFalse(response.context['user'].is_authenticated)

    def test_createPlaylist_url_redirects(self):
        response = self.client.get("/upload/")
        self.assertEqual(response.status_code, 302)

    def test_createPlaylist_name_redirects(self):
        response = self.client.get(reverse_lazy('upload'))
        self.assertEqual(response.status_code, 302)

    def test_createPlaylist_valid_form(self): # shouldn't be able to make a playlist
        response = self.client.get('/')
        user = response.context['user']
        response = self.client.post(reverse_lazy('createPlaylist'), data={'name': 'playlist1', 'owner': user})
        self.assertEqual(response.status_code, 302) # redirects to login
        playlists = playlist.objects.all()
        self.assertEqual(playlists.count(),0) #creation not allowed


class unauthenticated_deletePlaylistView(TestCase):
    def setUp(self):
        '''
        Delete a playlist should be restricted to authenticated user.
        Checks no playlist can be deleted by unauthenticated users.
        '''
        # create 1 user object
        self.username = 'testuser'
        self.password = 'securepassword230923!'
        self.credentials = {
            'username': self.username,
            'password': self.password
        }
        self.user1 = User.objects.create_user(**self.credentials)
        # create a playlist for user
        post_dict1 = {'name': 'Test Title', 'owner':self.user1}
        form1 = playlist_form(post_dict1)
        self.playlist1 = form1.save(commit=False)
        self.playlist1.owner = self.user1
        self.playlist1.save()

    def test_user_not_authenticated(self):
        response = self.client.get('/')
        self.assertFalse(response.context['user'].is_authenticated)

    def test_playlist_created_successfully(self):
        playlist_objects = playlist.objects.all()
        self.assertEqual(playlist_objects.count(), 1)
        self.assertEqual(playlist_objects[0].owner, self.user1)

    def test_user_cant_delete_playlist(self):
        playlist1_id = self.playlist1.id
        response = self.client.get('/deletePlaylist/{}'.format(playlist1_id))
        self.assertEqual(response.status_code, 302)
        playlist_objects = playlist.objects.all()
        self.assertEqual(playlist_objects.count(),1) # did not allow deletion


class unauthenticated_addToPlaylistView(TestCase):
    def setUp(self):
        '''
        Adding to a playlist should be restricted to authenticated user.
        Checks no file can be added to a playlist by unauthenticated users.
        '''
        # create 1 user object
        self.username = 'testuser'
        self.password = 'securepassword230923!'
        self.credentials = {
            'username': self.username,
            'password': self.password
        }
        self.user1 = User.objects.create_user(**self.credentials)
        # create a playlist for user
        post_dict1 = {'name': 'Test Title1', 'owner':self.user1}
        form1 = playlist_form(post_dict1)
        self.playlist1 = form1.save(commit=False)
        self.playlist1.owner = self.user1
        self.playlist1.save()
        # create audio object
        audio_file =  open('testing/gimme_disco.mp3', 'rb')     
        post_dict = {'title': 'Test Title', 'category':'BB'}
        file_dict = {'file': SimpleUploadedFile(audio_file.name, audio_file.read())}
        form = audio_object_form(post_dict, file_dict)
        self.dummyFileApproved = form.save(commit=False)
        self.dummyFileApproved.approved = True
        self.dummyFileApproved.save()

    def test_user_not_authenticated(self):
        response = self.client.get('/')
        self.assertFalse(response.context['user'].is_authenticated)

    def test_playlist_created_successfully(self):
        playlist_objects = playlist.objects.all()
        self.assertEqual(playlist_objects.count(), 1)
        self.assertEqual(playlist_objects[0].owner, self.user1)

    def test_audio_object_created_successfully(self):
        audio_objects = audio_object.objects.all()
        self.assertEqual(audio_objects.count(), 1)

    def test_addToPlaylist_form_url_redirects(self): # GET branch should redirect an unauthenticated user
        response = self.client.get('/addToPlaylist/{}/{}'.format(self.dummyFileApproved.id, self.dummyFileApproved.title))
        self.assertEqual(response.status_code, 302)

    def test__unauthenticated_user_cant_add_audio_object_to_their_playlist(self):
        response = self.client.post('/addToPlaylist/{}/{}'.format(self.dummyFileApproved.id, self.dummyFileApproved.title), data={'sourcePlaylist':self.playlist1.id})
        self.assertEqual(response.status_code, 302)
        playlist1_files = self.playlist1.audios.all() # not added to playlist 1
        self.assertEqual(playlist1_files.count(), 0)


class unauthenticated_removeFromPlaylistView(TestCase):
    def setUp(self):
        '''
        Removing a file from a playlist should be restricted to authenticated user.
        Checks no file can be removed by unauthenticated users.
        '''
        # create user object
        self.username = 'testuser'
        self.password = 'securepassword230923!'
        self.credentials = {
            'username': self.username,
            'password': self.password
        }
        self.user1 = User.objects.create_user(**self.credentials)
        # create a playlist
        post_dict1 = {'name': 'Test Title1', 'owner':self.user1}
        form1 = playlist_form(post_dict1)
        self.playlist1 = form1.save(commit=False)
        self.playlist1.owner = self.user1
        self.playlist1.save()
        # create audio object
        audio_file =  open('testing/gimme_disco.mp3', 'rb')     
        post_dict = {'title': 'Test Title', 'category':'BB'}
        file_dict = {'file': SimpleUploadedFile(audio_file.name, audio_file.read())}
        form = audio_object_form(post_dict, file_dict)
        self.dummyFileApproved = form.save(commit=False)
        self.dummyFileApproved.approved = True
        self.dummyFileApproved.save()
        # Add object to playlist
        form = add_to_playlist_form(self.user1, {'file':self.dummyFileApproved, 'sourcePlaylist':self.playlist1})
        newPlaylistFile = form.save(commit=False)
        newPlaylistFile.file = audio_object.objects.get(id=self.dummyFileApproved.id)
        newPlaylistFile.save()

    def test_user_not_authenticated(self):
        response = self.client.get('/')
        self.assertFalse(response.context['user'].is_authenticated)

    def test_playlist_created_successfully(self):
        playlist_objects = playlist.objects.all()
        self.assertEqual(playlist_objects.count(), 1)
        self.assertEqual(self.playlist1.owner, self.user1)
        playlist1_files = self.playlist1.audios.all()
        self.assertEqual(playlist1_files.count(), 1)

    def test_audio_object_created_successfully(self):
        audio_objects = audio_object.objects.all()
        self.assertEqual(audio_objects.count(), 1)

    def test_cant_remove_object_from_playlist(self):
        response = self.client.post('/removeFromPlaylist/{}/{}'.format(self.playlist1.id, self.dummyFileApproved.id))
        self.assertEqual(response.status_code, 302)
        playlist1_files = self.playlist1.audios.all() # still in playlist 1
        self.assertEqual(playlist1_files.count(), 1)


class unauthenticated_viewPlaylistView(TestCase):
    def setUp(self):
        '''
        Checks a user can view their playlist properly.
        Additionally checks user authentication layer on this functionality.
        '''
        # create user object
        self.username = 'testuser'
        self.password = 'securepassword230923!'
        self.credentials = {
            'username': self.username,
            'password': self.password
        }
        self.user1 = User.objects.create_user(**self.credentials)
        # create a playlist
        post_dict1 = {'name': 'Test Title1', 'owner':self.user1}
        form1 = playlist_form(post_dict1)
        self.playlist1 = form1.save(commit=False)
        self.playlist1.owner = self.user1
        self.playlist1.save()
        # create audio object
        audio_file =  open('testing/gimme_disco.mp3', 'rb')     
        post_dict = {'title': 'Test Title', 'category':'BB'}
        file_dict = {'file': SimpleUploadedFile(audio_file.name, audio_file.read())}
        form = audio_object_form(post_dict, file_dict)
        self.dummyFileApproved = form.save(commit=False)
        self.dummyFileApproved.approved = True
        self.dummyFileApproved.save()
        # Add object to both playlist
        form = add_to_playlist_form(self.user1, {'file':self.dummyFileApproved, 'sourcePlaylist':self.playlist1})
        newPlaylistFile = form.save(commit=False)
        newPlaylistFile.file = audio_object.objects.get(id=self.dummyFileApproved.id)
        newPlaylistFile.save()

    def test_user_not_authenticated(self):
        response = self.client.get('/')
        self.assertFalse(response.context['user'].is_authenticated)

    def test_playlist_created_successfully(self):
        playlist_objects = playlist.objects.all()
        self.assertEqual(playlist_objects.count(), 1)
        self.assertEqual(self.playlist1.owner, self.user1)
        playlist1_files = self.playlist1.audios.all()
        self.assertEqual(playlist1_files.count(), 1)

    def test_audio_object_created_successfully(self):
        audio_objects = audio_object.objects.all()
        self.assertEqual(audio_objects.count(), 1)

    def test_cant_view_playlist_when_unauthenticated(self):
        response = self.client.get('/listen/playlist/{}'.format(self.playlist1.id))
        self.assertEqual(response.status_code, 302) # got redirected



class authenticated_createPlaylistView(TestCase):
    def setUp(self):
        '''
        Checks that a playlist can be created
        Additionally checks user authentication layer on this functionality.
        '''
        self.username = 'testuser'
        self.password = 'securepassword230923!'
        self.credentials = {
            'username': self.username,
            'password': self.password
        }
        self.user = User.objects.create_user(**self.credentials)
        self.response = self.client.login(username=self.username, password=self.password)

    def test_user_authenticated(self):
        response = self.client.get('/')
        self.assertTrue(response.context['user'].is_authenticated)

    def test_createPlaylist_url_loads(self):
        response = self.client.get("/createPlaylist/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='createPlaylist.html')
        self.assertTemplateUsed(response, template_name='base.html') # all pages should extend from base.html

    def test_createPlaylist_name_loads(self):
        response = self.client.get(reverse_lazy('createPlaylist'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='createPlaylist.html')
        self.assertTemplateUsed(response, template_name='base.html') # all pages should extend from base.html

    def test_createPlaylist_valid_form(self):
        response = self.client.post(reverse_lazy('createPlaylist'), data={'name': 'playlist1'})
        self.assertEqual(response.status_code, 302)
        playlists = playlist.objects.all()
        self.assertEqual(playlists.count(),1) #created successfully
        self.assertEqual(playlists[0].owner, self.user) # view function should auto make owner the request user

    def test_createPlaylist_invalid_form(self):
        response = self.client.post(reverse_lazy('createPlaylist'), data={})
        self.assertEqual(response.status_code, 200)
        playlists = playlist.objects.all()
        self.assertEqual(playlists.count(),0) # not created

    def test_createPlaylist_10playlists(self):
        for i in range(10):
            self.client.post(reverse_lazy('createPlaylist'), data={'name': 'playlist{}'.format(i)})
        playlists = playlist.objects.all()
        self.assertEqual(playlists.count(),10) # all created
        response = self.client.get('/')
        self.assertContains(response, '/listen/playlist', 10) # all playlists rendered on dropdown


class authenticated_deletePlaylistView(TestCase):
    def setUp(self):
        '''
        Checks that a playlist can be deleted
        Additionally checks user authentication layer on this functionality.
        '''
        # create 2 user objects and log in the first one
        self.username = 'testuser'
        self.password = 'securepassword230923!'
        self.credentials = {
            'username': self.username,
            'password': self.password
        }
        self.user1 = User.objects.create_user(**self.credentials)
        self.user2 = User.objects.create_user({'username':'otheruser', 'password':self.password})
        self.response = self.client.login(username=self.username, password=self.password)
        # create a playlist for each user
        post_dict1 = {'name': 'Test Title', 'owner':self.user1}
        form1 = playlist_form(post_dict1)
        self.playlist1 = form1.save(commit=False)
        self.playlist1.owner = self.user1
        self.playlist1.save()
        post_dict2 = {'name': 'Test Title', 'owner':self.user2}
        form2 = playlist_form(post_dict2)
        self.playlist2 = form2.save(commit=False)
        self.playlist2.owner = self.user2
        self.playlist2.save()

    def test_user1_authenticated(self):
        response = self.client.get('/')
        self.assertTrue(response.context['user'].is_authenticated)

    def test_playlists_created_successfully(self):
        playlist_objects = playlist.objects.all()
        self.assertEqual(playlist_objects.count(), 2)
        user1_playlist = playlist.objects.filter(owner=self.user1)
        user2_playlist = playlist.objects.filter(owner=self.user2)
        self.assertEqual(user1_playlist.count(), 1)
        self.assertEqual(user2_playlist.count(), 1)

    def test_user_can_delete_their_playlist(self):
        playlist1_id = self.playlist1.id
        response = self.client.get('/deletePlaylist/{}'.format(playlist1_id))
        self.assertEqual(response.status_code, 302)
        playlist_objects = playlist.objects.all()
        self.assertEqual(playlist_objects.count(),1) # deleted
        self.assertEqual(playlist_objects[0].owner, self.user2) # deleted correct playlist

    def test_user_cant_delete_others_playlist(self):
        playlist2_id = self.playlist2.id
        response = self.client.get('/deletePlaylist/{}'.format(playlist2_id))
        self.assertEqual(response.status_code, 302)
        playlist_objects = playlist.objects.all()
        self.assertEqual(playlist_objects.count(),2) # did not allow deletion


class authenticated_addToPlaylistView(TestCase):
    def setUp(self):
        '''
        Checks that audio_objects can be added to a playlist
        Additionally checks user authentication layer on this functionality.
        '''
        # create 2 user objects and log in the first one
        self.username = 'testuser'
        self.password = 'securepassword230923!'
        self.credentials = {
            'username': self.username,
            'password': self.password
        }
        self.user1 = User.objects.create_user(**self.credentials)
        self.user2 = User.objects.create_user({'username':'otheruser', 'password':self.password})
        self.response = self.client.login(username=self.username, password=self.password)
        # create a playlist for each user
        post_dict1 = {'name': 'Test Title1', 'owner':self.user1}
        form1 = playlist_form(post_dict1)
        self.playlist1 = form1.save(commit=False)
        self.playlist1.owner = self.user1
        self.playlist1.save()
        post_dict2 = {'name': 'Test Title2', 'owner':self.user2}
        form2 = playlist_form(post_dict2)
        self.playlist2 = form2.save(commit=False)
        self.playlist2.owner = self.user2
        self.playlist2.save()
        # create two audio objects
        audio_file =  open('testing/gimme_disco.mp3', 'rb')     
        post_dict = {'title': 'Test Title', 'category':'BB'}
        file_dict = {'file': SimpleUploadedFile(audio_file.name, audio_file.read())}
        form = audio_object_form(post_dict, file_dict)
        self.dummyFileApproved = form.save(commit=False)
        self.dummyFileApproved.approved = True
        self.dummyFileApproved.save()
        post_dict = {'title': 'Other File', 'category':'BB'}
        form2 = audio_object_form(post_dict, file_dict)
        self.dummyFileApproved2 = form2.save(commit=False)
        self.dummyFileApproved2.approved = True
        self.dummyFileApproved2.save()

    def test_user1_authenticated(self):
        response = self.client.get('/')
        self.assertTrue(response.context['user'].is_authenticated)

    def test_playlist_created_successfully(self):
        playlist_objects = playlist.objects.all()
        self.assertEqual(playlist_objects.count(), 2)
        self.assertEqual(self.playlist1.owner, self.user1)
        playlist1_files = self.playlist1.audios.all()
        self.assertEqual(playlist1_files.count(), 0)
        self.assertEqual(self.playlist2.owner, self.user2)
        playlist2_files = self.playlist2.audios.all()
        self.assertEqual(playlist2_files.count(), 0)

    def test_audio_objects_created_successfully(self):
        audio_objects = audio_object.objects.all()
        self.assertEqual(audio_objects.count(), 2)

    def test_addToPlaylist_form_url_loads(self):
        response = self.client.get('/addToPlaylist/{}/{}'.format(self.dummyFileApproved.id, self.dummyFileApproved.title))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='addToPlaylist.html')
        self.assertTemplateUsed(response, template_name='base.html') # all pages should extend from base.html

    def test_addToPlaylist_form_shows_only_user_playlist(self): # should not show another user's playlist in the GET branch
        response = self.client.get('/addToPlaylist/{}/{}'.format(self.dummyFileApproved.id, self.dummyFileApproved.title))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Test Title1' in str(response.content)) # dropdown shows the user playlist
        self.assertFalse('Test Title2' in str(response.content)) # dropdown does not show the other user playlist

    def test_user_can_add_audio_object_to_their_playlist(self):
        response = self.client.post('/addToPlaylist/{}/{}'.format(self.dummyFileApproved.id, self.dummyFileApproved.title), data={'sourcePlaylist':self.playlist1.id})
        self.assertEqual(response.status_code, 302)
        playlist1_files = self.playlist1.audios.all() # added to playlist 1
        self.assertEqual(playlist1_files.count(), 1)
        playlist2_files = self.playlist2.audios.all() 
        self.assertEqual(playlist2_files.count(), 0) # not added to playlist 2

    def test_user_can_add_multiple_audio_objects_to_their_playlist(self):
        response = self.client.post('/addToPlaylist/{}/{}'.format(self.dummyFileApproved.id, self.dummyFileApproved.title), data={'sourcePlaylist':self.playlist1.id})
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/addToPlaylist/{}/{}'.format(self.dummyFileApproved2.id, self.dummyFileApproved2.title), data={'sourcePlaylist':self.playlist1.id})
        self.assertEqual(response.status_code, 302)
        playlist1_files = self.playlist1.audios.all() # added to playlist 1
        self.assertEqual(playlist1_files.count(), 2)
        playlist2_files = self.playlist2.audios.all() 
        self.assertEqual(playlist2_files.count(), 0) # not added to playlist 2

    def test_user_cannot_add_to_someone_elses_playlist(self):
        response = self.client.post('/addToPlaylist/{}/{}'.format(self.dummyFileApproved.id, self.dummyFileApproved.title), data={'sourcePlaylist':self.playlist2.id}) # not user 1 playlist
        self.assertEqual(response.status_code, 200) # should rerender form
        playlist1_files = self.playlist1.audios.all() # not added to playlist 1
        self.assertEqual(playlist1_files.count(), 0)
        playlist2_files = self.playlist2.audios.all() # not added to playlist 1
        self.assertEqual(playlist2_files.count(), 0) 


class authenticated_removeFromPlaylistView(TestCase):
    def setUp(self):
        '''
        Checks that audio_objects can be removed from a playlist
        Additionally checks user authentication layer on this functionality.
        '''
        # create 2 user objects and log in the first one
        self.username = 'testuser'
        self.password = 'securepassword230923!'
        self.credentials = {
            'username': self.username,
            'password': self.password
        }
        self.user1 = User.objects.create_user(**self.credentials)
        self.user2 = User.objects.create_user({'username':'otheruser', 'password':self.password})
        self.response = self.client.login(username=self.username, password=self.password)
        # create a playlist for each user
        post_dict1 = {'name': 'Test Title1', 'owner':self.user1}
        form1 = playlist_form(post_dict1)
        self.playlist1 = form1.save(commit=False)
        self.playlist1.owner = self.user1
        self.playlist1.save()
        post_dict2 = {'name': 'Test Title2', 'owner':self.user2}
        form2 = playlist_form(post_dict2)
        self.playlist2 = form2.save(commit=False)
        self.playlist2.owner = self.user2
        self.playlist2.save()
        # create two audio objects
        audio_file =  open('testing/gimme_disco.mp3', 'rb')     
        post_dict = {'title': 'Test Title', 'category':'BB'}
        file_dict = {'file': SimpleUploadedFile(audio_file.name, audio_file.read())}
        form = audio_object_form(post_dict, file_dict)
        self.dummyFileApproved = form.save(commit=False)
        self.dummyFileApproved.approved = True
        self.dummyFileApproved.save()
        post_dict = {'title': 'Other File', 'category':'BB'}
        form2 = audio_object_form(post_dict, file_dict)
        self.dummyFileApproved2 = form2.save(commit=False)
        self.dummyFileApproved2.approved = True
        self.dummyFileApproved2.save()
        # Add both objects to both playlists
        form = add_to_playlist_form(self.user1, {'file':self.dummyFileApproved, 'sourcePlaylist':self.playlist1})
        newPlaylistFile = form.save(commit=False)
        newPlaylistFile.file = audio_object.objects.get(id=self.dummyFileApproved.id)
        newPlaylistFile.save()
        form = add_to_playlist_form(self.user2, {'file':self.dummyFileApproved, 'sourcePlaylist':self.playlist2})
        newPlaylistFile = form.save(commit=False)
        newPlaylistFile.file = audio_object.objects.get(id=self.dummyFileApproved.id)
        newPlaylistFile.save()
        form = add_to_playlist_form(self.user1, {'file':self.dummyFileApproved2, 'sourcePlaylist':self.playlist1})
        newPlaylistFile = form.save(commit=False)
        newPlaylistFile.file = audio_object.objects.get(id=self.dummyFileApproved2.id)
        newPlaylistFile.save()
        form = add_to_playlist_form(self.user2, {'file':self.dummyFileApproved2, 'sourcePlaylist':self.playlist2})
        newPlaylistFile = form.save(commit=False)
        newPlaylistFile.file = audio_object.objects.get(id=self.dummyFileApproved2.id)
        newPlaylistFile.save()

    def test_user1_authenticated(self):
        response = self.client.get('/')
        self.assertTrue(response.context['user'].is_authenticated)

    def test_playlist_created_successfully(self):
        playlist_objects = playlist.objects.all()
        self.assertEqual(playlist_objects.count(), 2)
        self.assertEqual(self.playlist1.owner, self.user1)
        playlist1_files = self.playlist1.audios.all()
        self.assertEqual(playlist1_files.count(), 2)
        self.assertEqual(self.playlist2.owner, self.user2)
        playlist2_files = self.playlist2.audios.all()
        self.assertEqual(playlist2_files.count(), 2)

    def test_audio_objects_created_successfully(self):
        audio_objects = audio_object.objects.all()
        self.assertEqual(audio_objects.count(), 2)

    def test_can_remove_object_from_playlist(self):
        response = self.client.post('/removeFromPlaylist/{}/{}'.format(self.playlist1.id, self.dummyFileApproved.id))
        self.assertEqual(response.status_code, 302)
        playlist1_files = self.playlist1.audios.all() # removed from playlist 1
        self.assertEqual(playlist1_files.count(), 1)
        playlist2_files = self.playlist2.audios.all() 
        self.assertEqual(playlist2_files.count(), 2) # not removed from playlist 2

    def test_can_remove_multiple_objects_from_playlist(self):
        response = self.client.post('/removeFromPlaylist/{}/{}'.format(self.playlist1.id, self.dummyFileApproved.id))
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/removeFromPlaylist/{}/{}'.format(self.playlist1.id, self.dummyFileApproved2.id))
        self.assertEqual(response.status_code, 302)
        playlist1_files = self.playlist1.audios.all() # removed from playlist 1
        self.assertEqual(playlist1_files.count(), 0)
        playlist2_files = self.playlist2.audios.all() 
        self.assertEqual(playlist2_files.count(), 2) # not removed from playlist 2

    def test_can_handle_removing_file_not_in_playlist(self):
        response = self.client.post('/removeFromPlaylist/{}/{}'.format(self.playlist1.id, self.dummyFileApproved.id)) # remove once
        playlist1_files = self.playlist1.audios.all() # removed
        self.assertEqual(playlist1_files.count(), 1)
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/removeFromPlaylist/{}/{}'.format(self.playlist1.id, self.dummyFileApproved.id)) # remove again
        playlist1_files = self.playlist1.audios.all() # handled ok
        self.assertEqual(playlist1_files.count(), 1)
        self.assertEqual(response.status_code, 302)

    def test_cant_remove_objects_from_someone_elses_playlist(self):
        response = self.client.post('/removeFromPlaylist/{}/{}'.format(self.playlist2.id, self.dummyFileApproved.id))
        self.assertEqual(response.status_code, 302)
        playlist1_files = self.playlist1.audios.all() # not removed from playlist 1
        self.assertEqual(playlist1_files.count(), 2)
        playlist2_files = self.playlist2.audios.all() 
        self.assertEqual(playlist2_files.count(), 2) # not removed from playlist 2


class authenticated_viewPlaylistView(TestCase):
    def setUp(self):
        '''
        Checks a user can view their playlist properly.
        Additionally checks user authentication layer on this functionality.
        '''
        # create 2 user objects and log in the first one
        self.username = 'testuser'
        self.password = 'securepassword230923!'
        self.credentials = {
            'username': self.username,
            'password': self.password
        }
        self.user1 = User.objects.create_user(**self.credentials)
        self.user2 = User.objects.create_user({'username':'otheruser', 'password':self.password})
        self.response = self.client.login(username=self.username, password=self.password)
        # create a playlist for each user
        post_dict1 = {'name': 'Test Title1', 'owner':self.user1}
        form1 = playlist_form(post_dict1)
        self.playlist1 = form1.save(commit=False)
        self.playlist1.owner = self.user1
        self.playlist1.save()
        post_dict2 = {'name': 'Test Title2', 'owner':self.user2}
        form2 = playlist_form(post_dict2)
        self.playlist2 = form2.save(commit=False)
        self.playlist2.owner = self.user2
        self.playlist2.save()
        # create two audio objects
        audio_file =  open('testing/gimme_disco.mp3', 'rb')     
        post_dict = {'title': 'Test Title', 'category':'BB'}
        file_dict = {'file': SimpleUploadedFile(audio_file.name, audio_file.read())}
        form = audio_object_form(post_dict, file_dict)
        self.dummyFileApproved = form.save(commit=False)
        self.dummyFileApproved.approved = True
        self.dummyFileApproved.save()
        post_dict = {'title': 'Other File', 'category':'BB'}
        form2 = audio_object_form(post_dict, file_dict)
        self.dummyFileApproved2 = form2.save(commit=False)
        self.dummyFileApproved2.approved = True
        self.dummyFileApproved2.save()
        # Add both objects to both playlists
        form = add_to_playlist_form(self.user1, {'file':self.dummyFileApproved, 'sourcePlaylist':self.playlist1})
        newPlaylistFile = form.save(commit=False)
        newPlaylistFile.file = audio_object.objects.get(id=self.dummyFileApproved.id)
        newPlaylistFile.save()
        form = add_to_playlist_form(self.user2, {'file':self.dummyFileApproved, 'sourcePlaylist':self.playlist2})
        newPlaylistFile = form.save(commit=False)
        newPlaylistFile.file = audio_object.objects.get(id=self.dummyFileApproved.id)
        newPlaylistFile.save()
        form = add_to_playlist_form(self.user1, {'file':self.dummyFileApproved2, 'sourcePlaylist':self.playlist1})
        newPlaylistFile = form.save(commit=False)
        newPlaylistFile.file = audio_object.objects.get(id=self.dummyFileApproved2.id)
        newPlaylistFile.save()
        form = add_to_playlist_form(self.user2, {'file':self.dummyFileApproved2, 'sourcePlaylist':self.playlist2})
        newPlaylistFile = form.save(commit=False)
        newPlaylistFile.file = audio_object.objects.get(id=self.dummyFileApproved2.id)
        newPlaylistFile.save()

    def test_user1_authenticated(self):
        response = self.client.get('/')
        self.assertTrue(response.context['user'].is_authenticated)

    def test_playlist_created_successfully(self):
        playlist_objects = playlist.objects.all()
        self.assertEqual(playlist_objects.count(), 2)
        self.assertEqual(self.playlist1.owner, self.user1)
        playlist1_files = self.playlist1.audios.all()
        self.assertEqual(playlist1_files.count(), 2)
        self.assertEqual(self.playlist2.owner, self.user2)
        playlist2_files = self.playlist2.audios.all()
        self.assertEqual(playlist2_files.count(), 2)

    def test_audio_objects_created_successfully(self):
        audio_objects = audio_object.objects.all()
        self.assertEqual(audio_objects.count(), 2)

    def test_user_can_view_their_playlist(self):
        response = self.client.get('/listen/playlist/{}'.format(self.playlist1.id))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="playlistItemContainer"', 2) # showing both playlist items

    def test_user_cant_view_someone_elses_playlist(self):
        response = self.client.get('/listen/playlist/{}'.format(self.playlist2.id))
        self.assertEqual(response.status_code, 302) # redirects you trying to peek someone else's playlist
