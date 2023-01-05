from django.test import TestCase
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


##############################
# AUTHENTICATION VIEWS TESTS #
##############################


class loginView(TestCase):
    def setUp(self):
        '''
        Checks the user login function.
        This function is in audio_server/views.py
        '''
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

    def test_login_url_loads(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='registration/login.html')
        self.assertTemplateUsed(response, template_name='base.html') # all pages should extend from base.html

    def test_login_name_loads(self):
        response = self.client.get(reverse_lazy('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='registration/login.html')
        self.assertTemplateUsed(response, template_name='base.html') # all pages should extend from base.html

    def test_correct_credentials(self): # not technically a view but checks underlying authentication system works before testing the view
        user = authenticate(username=self.username, password=self.password)
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_username(self): # not technically a view but checks underlying authentication system works before testing the view
        user = authenticate(username='wrongusername', password=self.password)
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_password(self): # not technically a view but checks underlying authentication system works before testing the view
        user = authenticate(username=self.username, password='wrongpassword')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_login_view_post(self):
        response = self.client.post('/login/', self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_view_post_invalid_username(self):
        response = self.client.post('/login/', self.credentials_wrong_username, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertEqual(response.status_code, 200) # should rerender login page on invalid login
        self.assertTrue('Sorry, that login was invalid. Please try again.' in str(response.content)) # check error message rendered

    def test_login_view_post_invalid_password(self):
        response = self.client.post('/login/', self.credentials_wrong_password, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertEqual(response.status_code, 200) # should rerender login page on invalid login
        self.assertTrue('Sorry, that login was invalid. Please try again.' in str(response.content)) # check error message rendered

    def test_login_redirects_authenticated_user(self): # logged in user should be redirected from login page
        response1 = self.client.post('/login/', self.credentials, follow=True) # log in user
        self.assertTrue(response1.context['user'].is_authenticated) # log in successful
        response2 = self.client.get('/login/') # tries to go to login page
        self.assertEqual(response2.status_code, 302) # gets redirected status code


class createAccountView(TestCase):
    def setUp(self):
        '''
        Checks the user create account function.
        This function is in audio_server/views.py
        '''
        self.firstName = 'test'
        self.lastName = 'user'
        self.username = 'testuser'
        self.email = 'testuser@email.com'
        self.password = 'securepassword230923!'

    def test_register_url_loads(self):
        response = self.client.get("/register/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='registration/register.html')
        self.assertTemplateUsed(response, template_name='base.html') # all pages should extend from base.html

    def test_register_name_loads(self):
        response = self.client.get(reverse_lazy('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='registration/register.html')
        self.assertTemplateUsed(response, template_name='base.html') # all pages should extend from base.html

    def test_register_one_account(self):
        response = self.client.post(reverse_lazy('register'), data={
            'username': self.username,
            'email': self.email,
            'firstname': self.firstName,
            'lastname':self.lastName,
            'password1': self.password,
            'password2': self.password
        })
        self.assertEqual(response.status_code, 302) # should redirect to home page on successful register
        users = User.objects.all()
        self.assertEqual(users.count(), 1) # should make account
        self.assertEqual(users[0].email, self.email) # account info correct
        self.assertEqual(users[0].username, self.username)
        self.assertTrue(users[0].check_password(self.password))

    def test_register_invalid_email(self):
        response = self.client.post(reverse_lazy('register'), data={
            'username': self.username,
            'email': 'dsd',
            'firstname': self.firstName,
            'lastname':self.lastName,
            'password1': self.password,
            'password2': self.password
        })
        self.assertEqual(response.status_code, 200) # should rerender register page on invalid login
        users = User.objects.all()
        self.assertEqual(users.count(), 0) #did not allow account creation
        self.assertTrue('Enter a valid email address.' in str(response.content)) # check error message rendered

    def test_register_common_password(self):
        response = self.client.post(reverse_lazy('register'), data={
            'username': self.username,
            'email': self.email,
            'firstname': self.firstName,
            'lastname':self.lastName,
            'password1': 'password',
            'password2': 'password'
        })
        self.assertEqual(response.status_code, 200) # should rerender register page on invalid login
        users = User.objects.all()
        self.assertEqual(users.count(), 0) #did not allow account creation
        self.assertTrue('This password is too common.' in str(response.content)) # check error message rendered


    def test_register_short_password(self):
        response = self.client.post(reverse_lazy('register'), data={
            'username': self.username,
            'email': self.email,
            'firstname': self.firstName,
            'lastname':self.lastName,
            'password1': 'p',
            'password2': 'p'
        })
        self.assertEqual(response.status_code, 200) # should rerender register page on invalid login
        users = User.objects.all()
        self.assertEqual(users.count(), 0) #did not allow account creation
        self.assertTrue('This password is too short.' in str(response.content)) # check error message rendered

    def test_register_mismatch_password(self):
        response = self.client.post(reverse_lazy('register'), data={
            'username': self.username,
            'email': self.email,
            'firstname': self.firstName,
            'lastname':self.lastName,
            'password1': 'p',
            'password2': 'b'
        })
        self.assertEqual(response.status_code, 200) # should rerender register page on invalid login
        users = User.objects.all()
        self.assertEqual(users.count(), 0) #did not allow account creation
        self.assertTrue('The two password fields didn' in str(response.content)) # check error message rendered, encoding issue checking for ' character so look for substring

    def test_register_password_similar_to_username(self):
        response = self.client.post(reverse_lazy('register'), data={
            'username': self.username,
            'email': self.email,
            'firstname': self.firstName,
            'lastname':self.lastName,
            'password1': self.username,
            'password2': self.username,
        })
        self.assertEqual(response.status_code, 200) # should rerender register page on invalid login
        users = User.objects.all()
        self.assertEqual(users.count(), 0) #did not allow account creation
        self.assertTrue('The password is too similar to the username.' in str(response.content)) # check error message rendered, encoding issue checking for ' character so look for substring

    def test_register_password_similar_to_email(self):
        response = self.client.post(reverse_lazy('register'), data={
            'username': self.username,
            'email': self.email,
            'firstname': self.firstName,
            'lastname':self.lastName,
            'password1': self.email,
            'password2': self.email,
        })
        self.assertEqual(response.status_code, 200) # should rerender register page on invalid login
        users = User.objects.all()
        self.assertEqual(users.count(), 0) #did not allow account creation
        self.assertTrue('The password is too similar to the email address.' in str(response.content)) # check error message rendered, encoding issue checking for ' character so look for substring

    def test_register_two_accounts_valid(self):
        response1 = self.client.post(reverse_lazy('register'), data={
            'username': self.username,
            'email': self.email,
            'firstname': self.firstName,
            'lastname':self.lastName,
            'password1': self.password,
            'password2': self.password
        })
        self.assertEqual(response1.status_code, 302) # redirect on success
        users = User.objects.all()
        self.assertEqual(users.count(), 1) # successful first creation

        response2 = self.client.get(reverse_lazy('register'))
        self.assertEqual(response2.status_code, 302) # should redirect an authenticated user

        response3 = self.client.get('/logout/')
        self.assertEqual(response3.status_code, 302) # logout first user, check successful, try to register another on next

        response4 = self.client.post(reverse_lazy('register'), data={
            'username': self.username + '2',
            'email': 'changedEmail' + self.email,
            'firstname': 'changedName' + self.firstName,
            'lastname': 'changedName' + self.lastName,
            'password1': self.password,
            'password2': self.password
        })
        self.assertEqual(response4.status_code, 302)
        users = User.objects.all()
        self.assertEqual(users.count(), 2)

    def test_register_10_accounts_valid(self):
        for i in range(10):
            response1 = self.client.post(reverse_lazy('register'), data={
                'username': self.username + str(i),
                'email': self.email,
                'firstname': self.firstName,
                'lastname':self.lastName,
                'password1': self.password,
                'password2': self.password
            })
            self.assertEqual(response1.status_code, 302) # redirect on success
            users = User.objects.all()

            response2 = self.client.get(reverse_lazy('register'))
            self.assertEqual(response2.status_code, 302) # should redirect an authenticated user

            response3 = self.client.get('/logout/')
            self.assertEqual(response3.status_code, 302) # logout first user, check successful, try to register another on next

        users = User.objects.all()
        self.assertEqual(users.count(), 10)

    def test_register_two_accounts_duplicate_username(self):
        response1 = self.client.post(reverse_lazy('register'), data={
            'username': self.username,
            'email': self.email,
            'firstname': self.firstName,
            'lastname':self.lastName,
            'password1': self.password,
            'password2': self.password
        })
        self.assertEqual(response1.status_code, 302) # redirect on success
        users = User.objects.all()
        self.assertEqual(users.count(), 1) # successful first creation

        response2 = self.client.get(reverse_lazy('register'))
        self.assertEqual(response2.status_code, 302) # should redirect an authenticated user

        response3 = self.client.get('/logout/')
        self.assertEqual(response3.status_code, 302) # logout first user, check successful, try to register another on next

        response4 = self.client.post(reverse_lazy('register'), data={
            'username': self.username,
            'email': 'changedEmail' + self.email,
            'firstname': 'changedName' + self.firstName,
            'lastname': 'changedName' + self.lastName,
            'password1': self.password,
            'password2': self.password
        })
        self.assertEqual(response4.status_code, 200) # should be unsuccessful and rerender the form
        users = User.objects.all()
        self.assertEqual(users.count(), 1)
        self.assertTrue('A user with that username already exists.' in str(response4.content)) # check error message rendered