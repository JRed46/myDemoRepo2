from django.test import TestCase
from django.urls import reverse_lazy


######################
# STATIC VIEWS TESTS #
######################


class staticPagesViews(TestCase):
    def setUp(self):
        '''
        Checks static home pages load.
        Also includes the landing page for listen
        These functions are in audio_app/views.py
        '''
        pass

    def test_index_name_loads(self):
        response = self.client.get(reverse_lazy('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='home/index.html')
        self.assertTemplateUsed(response, template_name='home/homeLinks.html') # snippet linking static home pages
        self.assertTemplateUsed(response, template_name='base.html') # all pages should extend from base.html
    
    def test_index_url_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='home/index.html')
        self.assertTemplateUsed(response, template_name='home/homeLinks.html') # snippet linking static home pages
        self.assertTemplateUsed(response, template_name='base.html') # all pages should extend from base.html
    
    def test_about_name_loads(self):
        response = self.client.get(reverse_lazy('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='home/about.html')
        self.assertTemplateUsed(response, template_name='home/homeLinks.html') # snippet linking static home pages
        self.assertTemplateUsed(response, template_name='base.html') # all pages should extend from base.html
    
    def test_about_url_loads(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='home/about.html')
        self.assertTemplateUsed(response, template_name='home/homeLinks.html') # snippet linking static home pages
        self.assertTemplateUsed(response, template_name='base.html') # all pages should extend from base.html

    def test_background_name_loads(self):
        response = self.client.get(reverse_lazy('background'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='home/background.html')
        self.assertTemplateUsed(response, template_name='home/homeLinks.html') # snippet linking static home pages
        self.assertTemplateUsed(response, template_name='base.html') # all pages should extend from base.html
    
    def test_background_url_loads(self):
        response = self.client.get('/background/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='home/background.html')
        self.assertTemplateUsed(response, template_name='home/homeLinks.html') # snippet linking static home pages
        self.assertTemplateUsed(response, template_name='base.html') # all pages should extend from base.html

    def test_disclaimer_name_loads(self):
        response = self.client.get(reverse_lazy('disclaimer'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='home/disclaimer.html')
        self.assertTemplateUsed(response, template_name='home/homeLinks.html') # snippet linking static home pages
        self.assertTemplateUsed(response, template_name='base.html') # all pages should extend from base.html
    
    def test_disclaimer_url_loads(self):
        response = self.client.get('/disclaimer/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='home/disclaimer.html')
        self.assertTemplateUsed(response, template_name='home/homeLinks.html') # snippet linking static home pages
        self.assertTemplateUsed(response, template_name='base.html') # all pages should extend from base.html

    def test_instructions_name_loads(self):
        response = self.client.get(reverse_lazy('instructions'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='home/instructions.html')
        self.assertTemplateUsed(response, template_name='home/homeLinks.html') # snippet linking static home pages
        self.assertTemplateUsed(response, template_name='base.html') # all pages should extend from base.html
    
    def test_instructions_url_loads(self):
        response = self.client.get('/instructions/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='home/instructions.html')
        self.assertTemplateUsed(response, template_name='home/homeLinks.html') # snippet linking static home pages
        self.assertTemplateUsed(response, template_name='base.html') # all pages should extend from base.html

    def test_sponsors_name_loads(self):
        response = self.client.get(reverse_lazy('sponsors'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='home/sponsors.html')
        self.assertTemplateUsed(response, template_name='home/homeLinks.html') # snippet linking static home pages
        self.assertTemplateUsed(response, template_name='base.html') # all pages should extend from base.html
    
    def test_sponsors_url_loads(self):
        response = self.client.get('/sponsors/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='home/sponsors.html')
        self.assertTemplateUsed(response, template_name='home/homeLinks.html') # snippet linking static home pages
        self.assertTemplateUsed(response, template_name='base.html') # all pages should extend from base.html

    def test_listen_name_loads(self):
        response = self.client.get(reverse_lazy('listen'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='listen_landing.html')
        self.assertTemplateUsed(response, template_name='base.html') # all pages should extend from base.html
    
    def test_listen_url_loads(self):
        response = self.client.get(('/listen/'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='listen_landing.html')
        self.assertTemplateUsed(response, template_name='base.html') # all pages should extend from base.html

