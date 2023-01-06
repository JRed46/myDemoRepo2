from django.test import TestCase
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from audio_app.models import audio_object
from audio_app.forms import audio_object_form
from django.core.files.uploadedfile import SimpleUploadedFile
from audio_app.utils import abreviationToCategory, categoryToAbreviation
from django.contrib.auth.models import Group
from audio_app.utils import is_admin


####################
# ADMIN VIEWS TEST #    # non playlist related view functions
####################


class nonadmin_manageSubmissionsView(TestCase):
    def setUp(self):
        '''
        Managing file submissions should be restricted to admin users.
        Checks non admin users cant use this functionality.
        '''
        # create 10 dummy files
        self.files = {}
        for i in range(10):
            audio_file =  open('testing/gimme_disco.mp3', 'rb')     
            post_dict = {'title': 'Test Title', 'category':'BB'}
            file_dict = {'file': SimpleUploadedFile(audio_file.name, audio_file.read())}
            form = audio_object_form(post_dict, file_dict)
            self.dummyFile = form.save()
            self.files[i] = self.dummyFile
        # create a user and log them in
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

    def test_manageSubmissions_url_redirects(self): # not an admin
        response = self.client.get("/admin/manageSubmissions/")
        self.assertEqual(response.status_code, 302) # should redirect

    def test_manageSubmissions_name_redirects(self):
        response = self.client.get(reverse_lazy('manageSubmissions')) # not an admin
        self.assertEqual(response.status_code, 302) # should redirect

    def test_approveSubmission_fails(self): # should not be able to approve
        response = self.client.post("/admin/approveSubmission/{}".format(self.files[0].id))
        self.assertEqual(response.status_code, 302) # should not throw an error
        self.assertFalse(audio_object.objects.get(id=self.files[0].id).approved) # file should not have been approved

    def test_denySubmission_fails(self): # should not be able to deny
        response = self.client.post("/admin/denySubmission/{}".format(self.files[0].id))
        self.assertEqual(response.status_code, 302) # should not throw an error
        self.assertTrue(audio_object.objects.filter(id=self.files[0].id).exists()) # file should not have been deleted


class admin_manageSubmissionsView(TestCase):
    def setUp(self):
        '''
        File uploading should be restricted to authenticated user.
        Checks no files can be uploaded by unauthenticated users.
        '''
        # create 10 unapproved dummy files
        self.files = {}
        for i in range(10):
            audio_file =  open('testing/gimme_disco.mp3', 'rb')     
            post_dict = {'title': 'Test Title', 'category':'BB'}
            file_dict = {'file': SimpleUploadedFile(audio_file.name, audio_file.read())}
            form = audio_object_form(post_dict, file_dict)
            self.dummyFile = form.save()
            self.files[i] = self.dummyFile
        # create 10 approved dummy files
        for i in range(10,20):
            audio_file =  open('testing/gimme_disco.mp3', 'rb')     
            post_dict = {'title': 'Test Title', 'category':'BB'}
            file_dict = {'file': SimpleUploadedFile(audio_file.name, audio_file.read())}
            form = audio_object_form(post_dict, file_dict)
            self.dummyFile = form.save(commit=False)
            self.dummyFile.approved = True
            self.dummyFile.save()
            self.files[i] = self.dummyFile
        # create a user and log them in
        self.username = 'testuser'
        self.password = 'securepassword230923!'
        self.credentials = {
            'username': self.username,
            'password': self.password
        }
        self.user = User.objects.create_user(**self.credentials)
        self.response = self.client.login(username=self.username, password=self.password)
        adminGroup, _ = Group.objects.get_or_create(name='Admin')
        adminGroup.user_set.add(self.user)

    def test_user_authenticated(self):
        response = self.client.get('/')
        self.assertTrue(response.context['user'].is_authenticated)

    def test_user_is_admin(self):
        self.assertTrue(is_admin(self.user))

    def test_dummy_files_created(self):
        audio_objects = audio_object.objects.all()
        approved_audio_objects = audio_object.objects.filter(approved=False)
        unapproved_audio_objects = audio_object.objects.filter(approved=False)
        self.assertEqual(audio_objects.count(), 20)
        self.assertEqual(approved_audio_objects.count(), 10)
        self.assertEqual(unapproved_audio_objects.count(), 10)

    def test_manageSubmissions_url_loads(self): # not an admin
        response = self.client.get("/admin/manageSubmissions/")
        self.assertEqual(response.status_code, 200) # should render page
        self.assertContains(response, 'class="playlistItemContainer"', 10) # should show 10 unapproved submissions

    def test_manageSubmissions_name_loads(self):
        response = self.client.get(reverse_lazy('manageSubmissions')) # not an admin
        self.assertEqual(response.status_code, 200) # should render page
        self.assertContains(response, 'class="playlistItemContainer"', 10) # should show 10 unapproved submissions

    def test_approveSubmission_works(self): # should not be able to approve
        response = self.client.post("/admin/approveSubmission/{}".format(self.files[0].id))
        self.assertEqual(response.status_code, 302) # should not throw an error
        self.assertTrue(audio_object.objects.get(id=self.files[0].id).approved) # file should have been approved

    def test_submission_approval_integration(self):
        response = self.client.post("/admin/approveSubmission/{}".format(self.files[0].id))
        self.assertEqual(response.status_code, 302) # should not throw an error
        self.assertTrue(audio_object.objects.get(id=self.files[0].id).approved) # file should have been approved
        response = self.client.get("/admin/manageSubmissions/") # check the view renders
        self.assertEqual(response.status_code, 200) # should render page
        self.assertContains(response, 'class="playlistItemContainer"', 9) # should now show 9 unapproved submissions

    def test_denySubmission_works(self): # should not be able to deny
        response = self.client.post("/admin/denySubmission/{}".format(self.files[0].id))
        self.assertEqual(response.status_code, 302) # should not throw an error
        self.assertFalse(audio_object.objects.filter(id=self.files[0].id).exists()) # file should have been deleted

    def test_submission_denial_integration(self):
        response = self.client.post("/admin/denySubmission/{}".format(self.files[0].id))
        self.assertEqual(response.status_code, 302) # should not throw an error
        self.assertFalse(audio_object.objects.filter(id=self.files[0].id).exists()) # file should have been deleted
        response = self.client.get("/admin/manageSubmissions/") # check the view renders
        self.assertEqual(response.status_code, 200) # should render page
        self.assertContains(response, 'class="playlistItemContainer"', 9) # should now show 9 unapproved submissions