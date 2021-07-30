#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model
from django.conf import settings
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys

from tests.config import USER1_EMAIL, USER1_PASSWORD, USER1_USERNAME, USER1_FIRSTNAME, USER1_LASTNAME, USER2_EMAIL, USER2_PASSWORD, USER2_USERNAME, USER2_FIRSTNAME, USER2_LASTNAME

firefox_options = webdriver.FirefoxOptions()
firefox_options.headless = True

class FirefoxFunctionalTestCases(StaticLiveServerTestCase):
    """
       This class allows us to test the different search engines of the application for Firefox browser
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Firefox(
            executable_path=str(settings.BASE_DIR / 'webdrivers' / 'geckodriver'),
            options=firefox_options,
        )
        cls.driver.implicitly_wait(30)
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.driver.quit()

    def setUp(self):
        User = get_user_model()
        User.objects.create_user(            
            username=USER1_USERNAME,
            first_name=USER1_FIRSTNAME,
            last_name=USER1_LASTNAME,
            email=USER1_EMAIL,
            password=USER1_PASSWORD,
        )

    def test_homepage_large_search_form(self):
        """
          We test the large search engine on the homepage
        """
        # We call the web application
        self.driver.get(self.live_server_url)
        # We localise the text field 
        search_field = self.driver.find_element_by_id("large-search-form")
        search_field.clear()

        # We enter and confirm a search keyword
        search_field.send_keys("nutella")
        search_field.submit()

        # We look at the list of results displayed after the search
        # using the find_elements_by_class_name method
        lists= self.driver.find_elements_by_class_name("product-card")

        # We review the elements and return the individual content
        i = 0
        for listitem in lists:
          print (listitem.get_attribute("innerHTML"))
          i += 1
          if(i > 2):
            break

    def test_registration_form(self):
        """
            We test the registration form
        """
        # We call the web application
        self.driver.get(self.live_server_url)
        # We go to the registration page
        self.driver.find_element_by_class_name('register-link').click()

        # We localise the text field and we enter and confirm a email
        register_email = self.driver.find_element_by_id("id_email").send_keys(USER2_EMAIL)
        # Idem for firstname, lastname and username
        register_email = self.driver.find_element_by_id("id_first_name").send_keys(USER2_FIRSTNAME)        
        register_email = self.driver.find_element_by_id("id_last_name").send_keys(USER2_LASTNAME)
        register_email = self.driver.find_element_by_id("id_username").send_keys(USER2_USERNAME)        
        # Idem for password (x2)
        register_password1 = self.driver.find_element_by_id("id_password1").send_keys(USER2_PASSWORD)
        register_password2 = self.driver.find_element_by_id("id_password2").send_keys(USER2_PASSWORD)
        # We submit form
        self.driver.find_element_by_css_selector("section.regitration-main-section form button").click();

        # To know if we have been redirected to the home page after login, we look for a specific tag for this page
        class_to_find = self.driver.find_element_by_class_name("alert-success")
        # We check that the chosen tag contains a text that is only found on the home page
        self.assertEqual(
            class_to_find.text ,
            "Votre compte a bien été créé, vous pouvez désormais vous connecter.",
        )

        # We close the browser window
        self.driver.close()

    def test_login_form(self):
        """
            We test the login form
        """
        # We call the web application
        self.driver.get(self.live_server_url)
        # We go to the login page
        self.driver.find_element_by_class_name('connect-link').click()

        # We localise the text field and we enter and confirm a email
        login_email = self.driver.find_element_by_id("id_username").send_keys(USER1_EMAIL)
        # idem for password
        login_password = self.driver.find_element_by_id("id_password").send_keys(USER1_PASSWORD)
        # We submit form
        self.driver.find_element_by_css_selector("section.login-main-section form button").click()

        # To know if we have been redirected to the home page after login, we look for a specific
        # tag for this page
        class_to_find = self.driver.find_element_by_class_name("index-about-title")
        # We check that the chosen tag contains a text that is only found on the home page
        self.assertEqual(
            class_to_find.text ,
            "Colette et Rémy",
        )
