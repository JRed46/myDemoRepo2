from django.test import TestCase
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from audio_app.models import audio_object
from audio_app.forms import audio_object_form
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile



class indexTest(TestCase):
    def setUp(self):
        '''
        Checks index page gets rendered
        '''
        pass #Set things up before running tests here

    def test_index_loads(self):
        response = self.client.get(reverse_lazy('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='index.html')



class registerTest(TestCase):
    def setUp(self):
        '''
        Checks register page functionality
        '''
        self.firstName = 'test'
        self.lastName = 'user'
        self.username = 'testuser'
        self.email = 'testuser@email.com'
        self.password = 'securepassword230923!'

    def test_register_page_url(self):
        response = self.client.get("/register/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='registration/register.html')

    def test_register_page_name(self):
        response = self.client.get(reverse_lazy('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='registration/register.html')

    def test_register_one_account(self):
        response = self.client.post(reverse_lazy('register'), data={
            'username': self.username,
            'email': self.email,
            'firstname': self.firstName,
            'lastname':self.lastName,
            'password1': self.password,
            'password2': self.password
        })
        self.assertEqual(response.status_code, 302)
        users = User.objects.all()
        self.assertEqual(users.count(), 1) # should make account
        self.assertEqual(users[0].email, self.email)
        self.assertEqual(users[0].username, self.username)

    def test_register_invalid_email(self):
        response = self.client.post(reverse_lazy('register'), data={
            'username': self.username,
            'email': 'dsd',
            'firstname': self.firstName,
            'lastname':self.lastName,
            'password1': self.password,
            'password2': self.password
        })
        self.assertEqual(response.status_code, 200)
        users = User.objects.all()
        self.assertEqual(users.count(), 0) #should not allow account creation

    def test_register_insecure_password(self):
        response = self.client.post(reverse_lazy('register'), data={
            'username': self.username,
            'email': self.email,
            'firstname': self.firstName,
            'lastname':self.lastName,
            'password1': 'password',
            'password2': 'password'
        })
        self.assertEqual(response.status_code, 200)
        users = User.objects.all()
        self.assertEqual(users.count(), 0) #should not allow account creation

    def test_register_two_accounts_valid(self):
        response = self.client.post(reverse_lazy('register'), data={
            'username': self.username,
            'email': self.email,
            'firstname': self.firstName,
            'lastname':self.lastName,
            'password1': self.password,
            'password2': self.password
        })
        response = self.client.post(reverse_lazy('register'), data={
            'username': self.username + '2',
            'email': 'changedEmail' + self.email,
            'firstname': 'changedName' + self.firstName,
            'lastname': 'changedName' + self.lastName,
            'password1': self.password,
            'password2': self.password
        })
        self.assertEqual(response.status_code, 302)
        users = User.objects.all()
        self.assertEqual(users.count(), 2)

    def test_register_two_accounts_duplicate_username(self):
        response = self.client.post(reverse_lazy('register'), data={
            'username': self.username,
            'email': self.email,
            'firstname': self.firstName,
            'lastname':self.lastName,
            'password1': self.password,
            'password2': self.password
        })
        response = self.client.post(reverse_lazy('register'), data={
            'username': self.username,
            'email': 'changedEmail' + self.email,
            'firstname': 'changedName' + self.firstName,
            'lastname': 'changedName' + self.lastName,
            'password1': self.password,
            'password2': self.password
        })
        self.assertEqual(response.status_code, 200)
        users = User.objects.all()
        self.assertEqual(users.count(), 1) #should not allow second account creation



class LogInTest(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'securepassword230923!'
        self.credentials = {
            'username': self.username,
            'password': self.password
        }
        self.credentials_wrong_password = {
            'username': self.username,
            'password': 'wrong'
        }
        self.credentials_wrong_username = {
            'username': 'wrong',
            'password': self.password
        }
        User.objects.create_user(**self.credentials)

    def test_login_page_url(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='registration/login.html')

    def test_login_page_name(self):
        response = self.client.get(reverse_lazy('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='registration/login.html')

    def test_correct_credentials(self):
        user = authenticate(username=self.username, password=self.password)
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(username='wrongusername', password=self.password)
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_pssword(self):
        user = authenticate(username=self.username, password='wrongpassword')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_login_form_valid(self):
        response = self.client.post('/login/', self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_form_invalid_username(self):
        response = self.client.post('/login/', self.credentials_wrong_username, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_login_form_invalid_password(self):
        response = self.client.post('/login/', self.credentials_wrong_password, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)



class uploadFileTest(TestCase):
    def setUp(self):
        pass

    def test_upload_page_url(self):
        response = self.client.get("/upload/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='upload.html')

    def test_upload_page_name(self):
        response = self.client.get(reverse_lazy('upload'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='upload.html')

    def test_upload_form(self):
        audio_file =  open('testing/gimme_disco.mp3', 'rb')
        post_dict = {'title': 'Test Title'}
        file_dict = {'file': SimpleUploadedFile(audio_file.name, audio_file.read())}
        form = audio_object_form(post_dict, file_dict)
        self.assertTrue(form.is_valid())

    def test_upload_integration(self):
        with open('testing/gimme_disco.mp3', 'rb') as fp:
            response = self.client.post(reverse_lazy('upload'), {'title': 'file title', 'file': fp})
            self.assertEqual(response.status_code, 200)
            users = audio_object.objects.all()
            self.assertEqual(users.count(), 1) #full process works



class filesListTest(TestCase):
    def setUp(self):
        fileObject = audio_object()
        fileObject.title = 'Foo Title'
        fileObject.file = File(open("testing/gimme_disco.mp3", "rb"))
        fileObject.save()

    def test_files_page_url(self):
        response = self.client.get("/files/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='files.html')

    def test_files_page_name(self):
        response = self.client.get(reverse_lazy('files'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='files.html')
            
    def test_files_render(self):
        files = audio_object.objects.all()
        self.assertEqual(files.count(), 1) #make sure file in database
        response = self.client.get(reverse_lazy('files'))
        self.assertContains(response, '</audio>', 1)
    
    def test_delete_file(self):
        files = audio_object.objects.all()
        file_id = files[0].id
        _ = self.client.get('/delete_file/{}'.format(file_id))
        files_updated = audio_object.objects.all()
        self.assertEqual(files_updated.count(), 0)
