from django.test import TestCase
from django.urls import reverse_lazy


#######################
# CHATBOT VIEWS TESTS #     # Expand these tests as chotbot is implemented, for now just checks static page loads
#######################


class chatbotViews(TestCase):
    def setUp(self):
        '''
        Checks static home pages load.
        Also includes the landing page for listen
        These functions are in audio_app/views.py
        '''
        pass

    def test_index_name_loads(self):
        response = self.client.get(reverse_lazy('chatbot'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='chatbot.html')
        self.assertTemplateUsed(response, template_name='base.html') # all pages should extend from base.html

    def test_chatbot_url_loads(self):
        response = self.client.get('/chatbot/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='chatbot.html')
        self.assertTemplateUsed(response, template_name='base.html') # all pages should extend from base.html