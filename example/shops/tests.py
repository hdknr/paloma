from django.test import TestCase

import os
import uuid
from bs4 import BeautifulSoup as Soup

from paloma.models import (
    Template,
    Message,
)


class TemplateTest(TestCase):
    fixtrues = ['auth.json', ]

    def test_get_template(self):
        """
        python manage.py test shops.TemplateTest.test_get_template
        """

        # Existing mail template
        self.assertEqual(Template.objects.count(), 0)
        t = Template.objects.get_template('signin')
        self.assertIsNotNone(t)
        self.assertEqual(Template.objects.count(), 1)

        t = Template.objects.get_template('SIGNIN')
        self.assertEqual(Template.objects.count(), 2)

        path = os.path.join(
            os.path.dirname(__file__),
            'templates/paloma/mails/default_signin.html'
        )

        if not os.path.isfile(path):
            with open(path, "w") as data:
                data.write('<subject>Hello</subject>'
                           '<text>Thank You.</text>')

        soup = Soup(open(path))
        self.assertEqual(t.subject, soup.select('subject')[0].text)
        self.assertEqual(t.text, soup.select('text')[0].text)

    def test_get_template_none(self):
        """
        python manage.py test shops.TemplateTest.test_get_template_none
        """

        # Not Existing mail template test
        path = os.path.join(
            os.path.dirname(__file__),
            'templates/paloma/mails/default_signout.html'
        )
        if os.path.isfile(path):
            print "deleteing", path, "for testing..."
            os.remove(path)

        # Not Existing mail template
        t = Template.objects.get_template('SIGNOUT')
        self.assertIsNotNone(t)
        self.assertEqual(t.subject, u'')
        self.assertEqual(t.text, u'')

        # create default template
        with open(path, "w") as data:
            data.write('<subject>Hello</subject>'
                       '<text>Thank You.</text>')

        # reload default template
        t = Template.objects.get_template('SIGNOUT')
        self.assertIsNotNone(t)

        soup = Soup(open(path))
        self.assertEqual(t.subject, soup.select('subject')[0].text)
        self.assertEqual(t.text, soup.select('text')[0].text)

    def test_create_message(self):
        """
        python manage.py test shops.TemplateTest.test_create_message
        """

        # create default template
        path = os.path.join(
            os.path.dirname(__file__),
            'templates/paloma/mails/default_campaign.html'
        )
        with open(path, "w") as data:
            data.write('<subject> Camplaign </subject>'
                       '<text>Thank You.{{ code }}</text>')

        code = uuid.uuid1().hex
        params = {'code':  code, }
        msg = Message.objects.create_from_template(
            'test@hdknr.com', "CAMPAIGN", params=params, )

        self.assertIsNotNone(msg)
        self.assertTrue(msg.text.find(code) >= 0)
