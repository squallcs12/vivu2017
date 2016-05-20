import json
import os
import subprocess
import threading
import time
from sys import platform as _platform
import platform

import django
import django_nose
from bs4 import BeautifulSoup
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import management
from django.test.testcases import LiveServerTestCase, SimpleTestCase as DjangoSimpleTestCase
from django_nose.plugin import ResultPlugin, DjangoSetUpPlugin, TestReorderer
from django_nose.runner import _get_plugins_from_settings
from nose.core import TestProgram, TextTestRunner
from nose.result import TextTestResult
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select

from common.tests.factories.user_factory import UserFactory

from faker import Faker

User = get_user_model()

fake = Faker()

WebElement.find = WebElement.find_element_by_css_selector
WebElement.find_all = WebElement.find_elements_by_css_selector
WebElement.xpath = WebElement.find_element_by_xpath


def element_by_tagname_and_text(self, tag, text):
    _xpath = ".//%s[normalize-space(.)='%s']" % (tag, text)
    try:
        return self.xpath(_xpath)
    except NoSuchElementException:
        pass
    return False
WebElement.element_by_tagname_and_text = element_by_tagname_and_text


def button(self, text):
    return self.element_by_tagname_and_text("button", text)
WebElement.button = button


def exit(self, type, value, traceback):
    return
WebElement.__enter__ = lambda x: x
WebElement.__exit__ = exit


def select_by_visible_text(self, text):
    Select(self).select_by_visible_text(text)
WebElement.select_by_visible_text = select_by_visible_text


def has_class(self, value):
    return value in self.get_attribute('class')
WebElement.has_class = has_class


class TimeoutException(AssertionError):
    pass


world = threading.local()
world.browser = None
world.browsers = []


class UserTestBaseMixin(object):
    user = None

    def init_user(self):
        user = UserFactory()
        if self.user is None:
            self.user = user
        return user

    def init_user_origin(self):
        email = fake.email()
        password = 'password'
        first_name = fake.first_name()
        user = User.objects.create( email=email, password=password, first_name=first_name,
                                    is_staff = True, is_active = True, is_active_with_code = True,
                                    is_guest = False)
        user.set_password('password')
        user.save()
        return user

    def login_user(self, user=None):
        if user is None:
            if self.user is None:
                self.init_user()
            user = self.user
        self.login(user)

    def login_user_origin(self, user=None):
        if user is None:
            if self.user is None:
                self.init_user_origin()
            user = self.user
        self.login_origin(user)

    def login_provider(self, user=None):
        self.login_user(user)
        if not self.user.is_provider:
            self.user.is_provider = True
            self.user.save()


class ChangeBrowserContext(object):
    def __init__(self, browser):
        self.browser = world.browser
        self.new_browser = browser

    def __enter__(self):
        world.browser = self.new_browser

    def __exit__(self, type, value, traceback):
        world.browser = self.browser


class BaseLiveTestCase(LiveServerTestCase, UserTestBaseMixin):
    source = 0
    source_dir = os.environ.get('CIRCLE_ARTIFACTS')
    node_server_thread = None

    @classmethod
    def close_browsers(cls):
        for browser in world.browsers:
            try:
                browser.quit()
            except WebDriverException:
                pass
        world.browsers = []
        world.browser = None

    def init_firefox(self):
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference('media.navigator.permission.disabled', True)
        firefox_profile.set_preference('dom.disable_beforeunload', True)
        firefox_profile.update_preferences()

        browser = webdriver.Firefox(firefox_profile)
        browser.implicitly_wait(10)
        browser.set_window_size(width=1200, height=800)

        return browser

    def init_chrome(self):
        options = webdriver.ChromeOptions()
        options.add_argument('enable-usermedia-screen-capturing')
        options.add_argument('auto-select-desktop-capture-source=Entire screen')
        options.add_argument('use-fake-device-for-media-stream')
        options.add_argument('use-fake-ui-for-media-stream')
        options.add_argument('disable-web-security')
        options.add_extension('_tests/extensions/Cooler-Platform_v1.1.crx')
        driver_location = ""

        if _platform == "linux" or _platform == "linux2":
            # linux
            driver_location = platform.machine().endswith('32') and "_tests/chromedriver-linux32" or "_tests/chromedriver-linux64"
        elif _platform == "darwin":
            # OS X
            driver_location = "_tests/chromedriver-mac"
        elif _platform == "win32":
            # Windows...
            driver_location = "_tests/chromedriver-win.exe"

        browser = webdriver.Chrome(executable_path=driver_location, chrome_options=options)

        browser.implicitly_wait(10)
        browser.set_window_size(width=1200, height=800)
        return browser

    def init_phantomjs(self):
        return webdriver.PhantomJS()

    def init_browser(self):
        if os.environ.get('BROWSER') == 'phantomjs':
            browser = self.init_phantomjs()
        else:
            browser = self.init_chrome()
        world.browsers.append(browser)
        return browser

    def in_browser(self, browser):
        return ChangeBrowserContext(browser)

    @property
    def browser(self):
        if world.browser is None:
            world.browser = self.init_browser()
        return world.browser

    @classmethod
    def start_node_server(cls):
        if cls.source_dir:  # no need to run server per test case on circleci
            return

        stderr = stdout = subprocess.PIPE
        if os.environ.get('NODE_LOG', '0') == '1':
            stderr = stdout = None
        env = os.environ.copy()
        env.update({
            'DB_NAME': settings.DATABASES['default']['NAME'],
            'SOCKET_PORT': '3005',
        })
        cls.node_server_thread = subprocess.Popen(
            ["node socket/index.js"],
            shell=True,
            env=env,
            stdout=stdout,
            stderr=stderr
        )

    @classmethod
    def end_node_server(cls):
        if not cls.node_server_thread:
            return

        cls.node_server_thread.terminate()
        netstat = subprocess.Popen("netstat -ltnpu".split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        grep = subprocess.Popen("grep 3005".split(), stdin=netstat.stdout, stdout=subprocess.PIPE)
        output = grep.communicate()[0]
        try:
            pid = output.split()[-1].decode().split("/")[0]
        except IndexError:
            pass
        else:
            subprocess.Popen(['kill', pid], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    @classmethod
    def setUpClass(cls):
        if not hasattr(LiveServerTestCase, 'static_collected') or not LiveServerTestCase.static_collected:
            management.call_command('collectstatic', interactive=False, verbosity=0)
            LiveServerTestCase.static_collected = True

        cls.start_node_server()
        super(BaseLiveTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.end_node_server()
        super(BaseLiveTestCase, cls).tearDownClass()

    def visit(self, page):
        self.browser.get('%s%s' % (self.live_server_url, page))

    def should_see_text(self, text):
        if not isinstance(text, str):
            text = str(text)
        self.assertIn(text, self.find('body').text)

    def should_see_texts(self, texts):
        body_text = self.find("body").text
        texts = [str(x) for x in texts]
        for text in texts:
            body_text.should.contain(text)

    def should_see_one_among_texts(self, texts):
        body_text = self.find("body").text
        texts = [str(x) for x in texts]
        found = any(x in body_text for x in texts)
        found.should.be.true

    def should_not_see_text(self, text):
        self.assertNotIn(text, self.find('body').text)

    def login(self, user):
        self.visit(settings.LOGIN_URL)
        self.find("#id_username").send_keys(user.email)
        self.find("#id_password").send_keys(user.raw_password)
        self.find("input[type='submit']").click()
        self.until(lambda: self.browser.page_source.should.contain(user.first_name))  # login successfully

    def login_origin(self, user):
        self.visit(settings.LOGIN_URL)
        self.find("#id_username").send_keys(user.email)
        self.find("#id_password").send_keys('password')
        self.find("input[type='submit']").click()
        self.until(lambda: self.browser.page_source.should.contain(user.first_name))  # login successfully

    def logout(self):
        self.visit('/accounts/logout')

    def element_exist(self, css_selector):
        try:
            self.find(css_selector)
            return True
        except NoSuchElementException:
            return False

    def element_by_tagname_and_text(self, tag, text, parent="body"):
        _xpath = ".//%s[normalize-space(.)='%s']" % (tag, text)
        for node in self.find_all(parent):
            try:
                return node.xpath(_xpath)
            except NoSuchElementException:
                pass
        return False

    def element_by_classname_and_text(self, class_name, text, parent="body"):
        _xpath = ".//*[contains(@class, '%s')][normalize-space(.)='%s']" % (class_name, text)
        for node in self.find_all(parent):
            try:
                return node.xpath(_xpath)
            except NoSuchElementException:
                pass
        return False

    def button(self, button_text, parent="body"):
        return self.element_by_tagname_and_text("button", button_text, parent)

    def link(self, label_text, parent="body"):
        return self.element_by_tagname_and_text("a", label_text, parent)

    def label(self, label_text, parent="body"):
        return self.element_by_tagname_and_text("label", label_text, parent)

    def element_for_label(self, label):
        if isinstance(label, str):
            label = self.label(label)
        return self.find("#%s" % label.get_attribute("for"))

    def find_all(self, selector):
        return self.browser.find_elements_by_css_selector(selector)

    def find(self, selector):
        try:
            return self.browser.find_element_by_css_selector(selector)
        except NoSuchElementException:
            if self.source_dir:
                BaseLiveTestCase.source += 1
                with open("%s/current_html_%s.html" % (self.source_dir, BaseLiveTestCase.source), "w") as f:
                    f.write(selector)
                    f.write("\r\n")
                    f.write(self.browser.page_source)
            raise

    @classmethod
    def take_screen_shot(cls):
        if cls.source_dir:
            BaseLiveTestCase.source += 1
            dir_path = os.path.join(cls.source_dir, str(BaseLiveTestCase.source))
            if not os.path.isdir(dir_path):
                os.mkdir(dir_path)
            for index, browser in enumerate(world.browsers):
                filename = os.path.join(dir_path, "current_page_{index}.png".format(index=index))
                print(filename)
                browser.get_screenshot_as_file(filename)

    def fill_in(self, selector, value):
        try:
            selector_input = self.find(selector)
            selector_input.clear()
            selector_input.send_keys(value)
        except:
            raise

    def sleep(self, seconds):
        time.sleep(seconds)

    def until(self, method, timeout=10, message='', interval=0.5):
        """Calls the method provided with the driver as an argument until the \
        return value is not False."""
        end_time = time.time() + timeout
        error = None
        while True:
            try:
                value = method()
                if value or value is None:
                    return value
            except Exception as ex:
                if error:
                    try:
                        raise ex from error
                    except Exception as ex2:
                        error = ex2
                else:
                    error = ex
            time.sleep(interval)
            if time.time() > end_time:
                break
        self.take_screen_shot()
        raise TimeoutException(message) from error

    def is_displayed_in_viewport(self, element):
        """
        Check if an element is displayed on current view port
        For now check against only y-position
        """
        if isinstance(element, str):
            element = self.find(element)

        element_location = element.location
        viewport_y = self.browser.execute_script("return window.scrollY")
        viewport_height = self.browser.execute_script("return window.innerHeight")

        return viewport_y + viewport_height >= element_location['y'] >= viewport_y

    def ajax_complete(self):
        return 0 == self.browser.execute_script("return jQuery.active")

    def get_js_var(self, var_name):
        return self.browser.execute_script("return {var_name}".format(var_name=var_name))

    def until_ajax_complete(self):
        self.until(self.ajax_complete)


class SimpleTestCase(DjangoSimpleTestCase, UserTestBaseMixin):
    response = None
    _soup = None

    @property
    def soup(self):
        if self._soup is None:
            self._soup = BeautifulSoup(self.response.content)
        return self._soup

    def login(self, user):
        self.client.login(username=user.username, password=user.raw_password)

    def visit(self, path, *args, **kwargs):
        self.response = self.client.get(path, *args, **kwargs)
        self._soup = None

    def find_all(self, selector):
        return self.soup.select(selector)

    def link(self, text):
        return self.soup.find('a', text=text)

    def should_see_text(self, text):
        self.soup.text.should.contain(text)

    def should_not_see_text(self, text):
        self.soup.text.shouldnt.contain(text)

    def json(self, response):
        return json.loads(response.content.decode())

    def should_see_texts(self, texts):
        for text in texts:
            self.soup.text.should.contain(text)


class DjangoNoseTextTestResult(TextTestResult):

    def addError(self, test, err):
        BaseLiveTestCase.take_screen_shot()
        BaseLiveTestCase.close_browsers()
        super(DjangoNoseTextTestResult, self).addError(test, err)

    def addFailure(self, test, err):
        BaseLiveTestCase.take_screen_shot()
        BaseLiveTestCase.close_browsers()
        super(DjangoNoseTextTestResult, self).addFailure(test, err)

    def addSuccess(self, test):
        BaseLiveTestCase.close_browsers()
        super(DjangoNoseTextTestResult, self).addSuccess(test)


class DjangoNoseTextTestRunner(TextTestRunner):
    resultclass = DjangoNoseTextTestResult

    def _makeResult(self):
        return self.resultclass(self.stream,
                                self.descriptions,
                                self.verbosity,
                                self.config)


class NoseTestProgram(TestProgram):
    def runTests(self):
        if isinstance(self.testRunner, type):
            self.testRunner = self.testRunner(stream=self.config.stream,
                                              verbosity=self.config.verbosity,
                                              config=self.config)
        return super(NoseTestProgram, self).runTests()


class DjangoNoseTestSuiteRunner(django_nose.NoseTestSuiteRunner):
    test_runner = DjangoNoseTextTestRunner
    test_program = NoseTestProgram

    def run_suite(self, nose_argv):
        """Run the test suite."""
        result_plugin = ResultPlugin()
        plugins_to_add = [DjangoSetUpPlugin(self),
                          result_plugin,
                          TestReorderer()]

        for plugin in _get_plugins_from_settings():
            plugins_to_add.append(plugin)
        try:
            django.setup()
        except AttributeError:
            # Setup isn't necessary in Django < 1.7
            pass

        self.test_program(argv=nose_argv, exit=False, addplugins=plugins_to_add, testRunner=DjangoNoseTextTestRunner)
        return result_plugin.result
