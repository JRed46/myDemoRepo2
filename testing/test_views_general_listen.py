from django.test import TestCase
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from audio_app.models import audio_object
from audio_app.forms import audio_object_form
from django.core.files.uploadedfile import SimpleUploadedFile
from audio_app.utils import abreviationToCategory, categoryToAbreviation
from django.contrib.auth.models import Group
from audio_app.utils import is_admin


##############################
# GENERAL LISTEN VIEWS TESTS #    # non playlist related view functions
##############################


class unauthenticated_uploadFileView(TestCase):
    def setUp(self):
        '''
        File uploading should be restricted to authenticated user.
        Checks no files can be uploaded by unauthenticated users.
        '''
        pass

    def test_user_not_authenticated(self):
        response = self.client.get('/')
        self.assertFalse(response.context['user'].is_authenticated)

    def test_upload_url_redirects(self):
        response = self.client.get("/upload/")
        self.assertEqual(response.status_code, 302)

    def test_upload_name_redirects(self):
        response = self.client.get(reverse_lazy('upload'))
        self.assertEqual(response.status_code, 302)

    def test_upload_valid_file(self):
        with open('testing/gimme_disco.mp3', 'rb') as fp:
            response = self.client.post(reverse_lazy('upload'), {'title': 'file title', 'file': fp, 'category':'BB'})
            self.assertEqual(response.status_code, 302)
            audio_objects = audio_object.objects.all()
            self.assertEqual(audio_objects.count(), 0) #upload denied


class unauthenticated_deleteFileView(TestCase):
    def setUp(self):
        '''
        File deletion should be restricted to authenticated user.
        Checks no files can be deleted by unauthenticated users.
        '''
        audio_file =  open('testing/gimme_disco.mp3', 'rb')     
        post_dict = {'title': 'Test Title', 'category':'BB'}
        file_dict = {'file': SimpleUploadedFile(audio_file.name, audio_file.read())}
        form = audio_object_form(post_dict, file_dict)
        self.dummyFile = form.save()

    def test_user_not_authenticated(self):
        response = self.client.get('/')
        self.assertFalse(response.context['user'].is_authenticated)

    def test_dummy_file_uploaded(self):
        audio_objects = audio_object.objects.all()
        self.assertEqual(audio_objects.count(), 1)

    def test_delete_dummy_file(self): # shouldn't be allowed to delete file
        category, file_id = self.dummyFile.category, self.dummyFile.id
        response = self.client.get('/delete_file/{}/{}'.format(category, file_id))
        self.assertEqual(response.status_code, 302)
        audio_objects = audio_object.objects.all()
        self.assertEqual(audio_objects.count(), 1) # not deleted


class unauthenticated_listenCategoryView(TestCase):
    def setUp(self):
        '''
        Users should be authenticated to listen to any files
        '''
        pass

    def test_user_not_authenticated(self):
        response = self.client.get('/')
        self.assertFalse(response.context['user'].is_authenticated)

    def test_category_not_viewable_without_authentication(self):
        for category_url in categoryToAbreviation.keys():
            response = self.client.get('/listen/{}'.format(category_url))
            self.assertEqual(response.status_code, 302) # gets redirected


class authenticated_uploadFileView(TestCase):
    def setUp(self):
        '''
        Checks that a file can be uploaded.
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

    def test_upload_url_loads(self):
        response = self.client.get("/upload/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='upload.html')
        self.assertTemplateUsed(response, template_name='base.html') # all pages should extend from base.html

    def test_upload_name_loads(self):
        response = self.client.get(reverse_lazy('upload'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='upload.html')
        self.assertTemplateUsed(response, template_name='base.html') # all pages should extend from base.html

    def test_upload_single_file_NOT_ADMIN(self):
        with open('testing/gimme_disco.mp3', 'rb') as fp:
            response = self.client.post(reverse_lazy('upload'), {'title': 'file title', 'file': fp, 'category':'BB'})
            self.assertEqual(response.status_code, 200)
            audio_objects = audio_object.objects.all()
            self.assertEqual(audio_objects.count(), 1) #upload worked
            self.assertFalse(audio_objects[0].approved) #file should not be approved yet since it wasn't submitted by an admin
            self.assertTrue('Creation success- we will review your submission and add it to the library soon. Thank you.' in str(response.content)) # displays success message
            
    def test_upload_single_file_IS_ADMIN(self):
        with open('testing/gimme_disco.mp3', 'rb') as fp:
            adminGroup, _ = Group.objects.get_or_create(name='Admin')
            adminGroup.user_set.add(self.user)
            response = self.client.post(reverse_lazy('upload'), {'title': 'file title', 'file': fp, 'category':'BB'})
            self.assertEqual(response.status_code, 200)
            audio_objects = audio_object.objects.all()
            self.assertEqual(audio_objects.count(), 1) #upload worked
            self.assertTrue(audio_objects[0].approved) #file should approved since it was submitted by an admin
            self.assertTrue('Creation success- file has been added to library.' in str(response.content)) # displays success message

    def test_upload_bad_category_NOT_ADMIN(self):
        with open('testing/gimme_disco.mp3', 'rb') as fp:
            response = self.client.post(reverse_lazy('upload'), {'title': 'file title', 'file': fp, 'category':'bad_cat_neofiwhfouhwfuckadka'})
            self.assertEqual(response.status_code, 200)
            audio_objects = audio_object.objects.all()
            self.assertEqual(audio_objects.count(), 0) #upload worked
            self.assertTrue('Creation failure- please submit a valid audio file.' in str(response.content)) # displays success message

    def test_upload_bad_category_IS_ADMIN(self):
        with open('testing/gimme_disco.mp3', 'rb') as fp:
            adminGroup, _ = Group.objects.get_or_create(name='Admin')
            adminGroup.user_set.add(self.user)
            response = self.client.post(reverse_lazy('upload'), {'title': 'file title', 'file': fp, 'category':'bad_cat_neofiwhfouhwfuckadka'})
            self.assertEqual(response.status_code, 200)
            audio_objects = audio_object.objects.all()
            self.assertEqual(audio_objects.count(), 0) #upload worked
            self.assertTrue('Creation failure- please submit a valid audio file.' in str(response.content)) # displays success message

    def test_upload_bad_file_NOT_ADMIN(self):
        with open('testing/test_views_general_listen.py', 'rb') as fp: # try submitting a python file
            response = self.client.post(reverse_lazy('upload'), {'title': 'file title', 'file': fp, 'category':'BB'})
            self.assertEqual(response.status_code, 200)
            audio_objects = audio_object.objects.all()
            self.assertEqual(audio_objects.count(), 0) #upload worked
            self.assertTrue('Creation failure- please submit a valid audio file.' in str(response.content)) # displays success message

    def test_upload_bad_file_IS_ADMIN(self):
        with open('testing/test_views_general_listen.py', 'rb') as fp: # try submitting a python file
            adminGroup, _ = Group.objects.get_or_create(name='Admin')
            adminGroup.user_set.add(self.user)
            response = self.client.post(reverse_lazy('upload'), {'title': 'file title', 'file': fp, 'category':'BB'})
            self.assertEqual(response.status_code, 200)
            audio_objects = audio_object.objects.all()
            self.assertEqual(audio_objects.count(), 0) #upload worked
            self.assertTrue('Creation failure- please submit a valid audio file.' in str(response.content)) # displays success message

    def test_upload_all_categories(self):
        categories = abreviationToCategory.keys()
        for cat in categories:
            with open('testing/gimme_disco.mp3', 'rb') as fp:
                response = self.client.post(reverse_lazy('upload'), {'title': 'file title', 'file': fp, 'category':cat})
                self.assertEqual(response.status_code, 200)
        audio_objects = audio_object.objects.all()
        self.assertEqual(audio_objects.count(), len(categories)) # all uploads successful
        for cat in categories:
            cat_audio_objects = audio_object.objects.filter(category=cat)
            self.assertEqual(cat_audio_objects.count(), 1) # can filter by category


class authenticated_deleteFileView(TestCase):
    def setUp(self):
        '''
        Checks that a file can be deleted.
        Additionally checks user authentication layer on this functionality.
        '''
        audio_file =  open('testing/gimme_disco.mp3', 'rb')     
        post_dict = {'title': 'Test Title', 'category':'BB'}
        file_dict = {'file': SimpleUploadedFile(audio_file.name, audio_file.read())}
        form = audio_object_form(post_dict, file_dict)
        self.dummyFile = form.save()
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

    def test_dummy_file_uploaded(self):
        audio_objects = audio_object.objects.all()
        self.assertEqual(audio_objects.count(), 1)

    def test_delete_dummy_file_NOT_ADMIN(self): # shouldnt be able to
        category, file_id = self.dummyFile.category, self.dummyFile.id
        response = self.client.get('/delete_file/{}/{}'.format(category, file_id))
        self.assertEqual(response.status_code, 302)
        audio_objects = audio_object.objects.all()
        self.assertEqual(audio_objects.count(), 1) # not deleted

    def test_delete_dummy_file_IS_ADMIN(self): # should work
        adminGroup, _ = Group.objects.get_or_create(name='Admin')
        adminGroup.user_set.add(self.user)
        category, file_id = self.dummyFile.category, self.dummyFile.id
        response = self.client.get('/delete_file/{}/{}'.format(category, file_id))
        self.assertEqual(response.status_code, 302)
        audio_objects = audio_object.objects.all()
        self.assertEqual(audio_objects.count(), 0) # deleted


class authenticated_listenCategoryView(TestCase):
    def setUp(self):
        '''
        Checks that a file can be deleted.
        Additionally checks user authentication layer on this functionality.
        '''
        # create two audio_object in every category
        # remember that we should only display authenticated = True files
        # so we make one with trie and one with false
        self.categories = abreviationToCategory.keys()
        for cat in self.categories:
            audio_file =  open('testing/gimme_disco.mp3', 'rb')     
            post_dict = {'title': 'Test Title', 'category':cat}
            file_dict = {'file': SimpleUploadedFile(audio_file.name, audio_file.read())}
            form = audio_object_form(post_dict, file_dict)
            dummyFileUnapproved = form.save()
            form = audio_object_form(post_dict, file_dict)
            dummyFileApproved = form.save(commit=False)
            dummyFileApproved.approved = True
            dummyFileApproved.save()
        # create a user
        self.username = 'testuser'
        self.password = 'securepassword230923!'
        self.credentials = {
            'username': self.username,
            'password': self.password
        }
        User.objects.create_user(**self.credentials)
        # log in user
        self.response = self.client.login(username=self.username, password=self.password)

    def test_user_authenticated(self):
        response = self.client.get('/')
        self.assertTrue(response.context['user'].is_authenticated)

    def test_dummy_files_uploaded(self):
        audio_objects = audio_object.objects.all()
        self.assertEqual(audio_objects.count(), 2*len(self.categories))
        for cat in self.categories:
            audio_objects_cat = audio_object.objects.filter(category=cat)
            self.assertEqual(audio_objects_cat.count(), 2)

    def test_valid_categories_load(self):
        for category_url in categoryToAbreviation.keys():
            response = self.client.get('/listen/{}'.format(category_url))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template_name='listen_files.html')
            self.assertTemplateUsed(response, template_name='base.html') # all pages should extend from base.html
            self.assertContains(response, 'class="playlistItemContainer"', 1) # only showing approved files

    def test_invalid_category_load(self):
        response = self.client.get('/listen/{}'.format('bad_category_849038479284ydiuewiu'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='listen_files.html')
        self.assertTemplateUsed(response, template_name='base.html') # all pages should extend from base.html
        self.assertContains(response, 'class="playlistItemContainer"', 0) # only showing approved files