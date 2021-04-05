"""Module with base class of functional tests."""
from selenium import webdriver
from django.conf import settings
from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class Functional(StaticLiveServerTestCase):
    """Base class used for functional tests."""

    host = 'website'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        selenium_server = 'http://selenium:4444/wd/hub'
        options = webdriver.ChromeOptions()
        options.add_experimental_option('prefs',
            {'intl.accept_languages': 'en,en_US'})

        capabilities = options.to_capabilities()
        capabilities['loggingPrefs'] = { 'browser':'ALL' }

        cls.browser =  webdriver.Remote(desired_capabilities=capabilities,
                                        command_executor=selenium_server)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def check_el_text(self, text, el_text='', xpath=None, test_msg=''):
        """Check if the given text is equal the tag text."""
        if xpath:
            el = self.browser.find_element_by_xpath(xpath)
            el_text = el.text
            if not el_text:
                el_text = el.get_attribute('text')
                el_text = el_text.strip().replace('\n', '')

        with self.subTest(test_msg):
            self.assertEqual(text, el_text)

    def check_translations(self, translations, path):
        """Useful method to check the page translations."""
        for lang, elements in translations.items():
            lang_prefix = f'{lang}/'
            path = path.lstrip('/')

            if lang == settings.LANGUAGE_CODE:
                lang_prefix = "" # The default lang (en) has no prefix.

            self.browser.get(f'{self.live_server_url}/{lang_prefix}{path}')
            #import pdb; pdb.set_trace()

            for el in elements:
                self.check_el_text(el[0], xpath=el[1],
                    test_msg=f'{lang}: element {el[1]}')

    def login(self):
        """Login in the authentication sistem.

        This is a helper fuction used to login in the authentication system.
        Usually used to test pages where the user needs to be authenticated.
        """
        login_url = '{}{}'.format(self.live_server_url,
                                  reverse('account:login'))
        self.browser.get(login_url)

        username = self.browser.find_element_by_name('username')
        username.send_keys(self.user.username)

        password = self.browser.find_element_by_name('password')
        password.send_keys(self.user_pass)

        submit_button = self.browser.find_element_by_class_name('btn-login')
        submit_button.click()

    def logout(self):
        """Logout of the authentication system.

        This is a helper fuction used to logout in the authentication system.
        Usually this function is used to logout a user after test a page where
        the user needed to be authenticated.

        After call the login function in a test. Is important to call the logout
        function in the end of the test to avoid interfere with another test.
        """
        logout_url = '{}{}'.format(self.live_server_url,
                                   reverse('account:logout'))
        self.browser.get(logout_url)
