from .base import FunctionalTest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

class LoginTest(FunctionalTest):

    def wait_for_element_with_id(self, element_id):
        WebDriverWait(self.browser, timeout=30).until(
            lambda b: b.find_element_by_id(element_id),
            'Could not find element with id {}. Page text was:\n{}'.format(
                element_id, self.browser.find_element_by_tag_name('body').text
            )
        )

    def wait_to_be_logged_in(self):
        self.wait_for_element_with_id('id_logout')
        self.assertRaises(NoSuchElementException, self.browser.find_element_by_id, 'id_signup')

    def wait_to_be_logged_out(self):
        self.wait_for_element_with_id('id_signup')
        self.assertRaises(NoSuchElementException, self.browser.find_element_by_id, 'id_logout')

    def test_signup(self):
        # Edith goes to the awesome Callisto site
        # and notices a "Sign in" link for the first time.
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_signup').click()

        # A login screen appears
        edith_signup_url = self.browser.current_url
        self.assertRegex(edith_signup_url, '/signup')

        # Edith signs up with her email address
        self.browser.find_element_by_id(
            'id_username'
        ).send_keys('edith@notrealemail.com')
        self.browser.find_element_by_id(
            'id_password1'
        ).send_keys('password')
        self.browser.find_element_by_id(
            'id_password2'
        ).send_keys('password')
        self.browser.find_element_by_tag_name('button').click()

        # She can see that she is logged in
        self.wait_for_element_with_id('id_logout')
        self.assertRaises(NoSuchElementException, self.browser.find_element_by_id, 'id_signup')
        # TK: what page do you go to after login?

        # Refreshing the page, she sees it's a real session login,
        # not just a one-off for that page
        self.browser.refresh()
        self.wait_to_be_logged_in()

        # She clicks logout and is no longer logged in
        self.browser.find_element_by_id('id_logout').click()
        self.wait_to_be_logged_out()

        # Logged out status also persists after refresh
        self.browser.refresh()
        self.wait_to_be_logged_out()


    #TK: test sign up validation, including duplicate username
    #TK: test login
    #TK: test logout