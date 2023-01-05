from django.test import TestCase
from audio_app.forms import audio_object_form, playlist_form, add_to_playlist_form
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User


class allForms(TestCase):
    def setUp(self):
        '''
        Checks all the forms work as expected
        '''
        self.username = 'testuser'
        self.password = 'securepassword230923!'
        self.credentials = {
            'username': self.username,
            'password': self.password
        }
        self.user = User.objects.create_user(**self.credentials)

    def test_upload_form_valid(self):
        audio_file =  open('testing/gimme_disco.mp3', 'rb')
        post_dict = {'title': 'Test Title', 'category':'BB'}
        file_dict = {'file': SimpleUploadedFile(audio_file.name, audio_file.read())}
        form = audio_object_form(post_dict, file_dict)
        self.assertTrue(form.is_valid())

    def test_upload_form_invalid1(self):
        audio_file =  open('testing/gimme_disco.mp3', 'rb')
        post_dict = {'title': 'Test Title',}
        file_dict = {'file': SimpleUploadedFile(audio_file.name, audio_file.read())}
        form = audio_object_form(post_dict, file_dict)
        self.assertFalse(form.is_valid())

    def test_upload_form_invalid2(self):
        audio_file =  open('testing/gimme_disco.mp3', 'rb')
        post_dict = { 'category':'BB'}
        file_dict = {'file': SimpleUploadedFile(audio_file.name, audio_file.read())}
        form = audio_object_form(post_dict, file_dict)
        self.assertFalse(form.is_valid())

    def test_upload_form_invalid3(self):
        post_dict = {'title': 'Test Title', 'category':'BB'}
        file_dict = {'file': ''}
        form = audio_object_form(post_dict, file_dict)
        self.assertFalse(form.is_valid())

    def test_playlist_form_valid(self): # needs a name, owner should be accepted but is auto populated by the view
        post_dict = {'name': 'Test Title', 'owner':self.user}
        form = playlist_form(post_dict)
        self.assertTrue(form.is_valid())

    def test_playlist_form_invalid1(self):
        post_dict = { 'owner':self.user}
        form = playlist_form(post_dict)
        self.assertFalse(form.is_valid())

    def test_add_to_playlist_form_valid(self):
        post_dict1 = {'name': 'Test Title1', 'owner':self.user} 
        form1 = playlist_form(post_dict1)
        playlist1 = form1.save(commit=False)
        playlist1.owner = self.user
        playlist1.save()
        form2 = add_to_playlist_form(self.user, {'sourcePlaylist':playlist1}) # should be ok
        self.assertTrue(form2.is_valid())

    def test_add_to_playlist_form_invalid(self):
        form2 = add_to_playlist_form(self.user, {}) # should not validate
        self.assertFalse(form2.is_valid())