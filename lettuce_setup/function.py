'''
Created on Jul 25, 2013

@author: antipro
'''
import pdb
import time
import sure
import urlparse
import datetime

from lettuce import step, before, after
from django.db import connection
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db.transaction import TransactionManagementError
from django.utils.translation import ugettext_lazy
from selenium.common.exceptions import NoSuchElementException

from .selenium_shortcut import *
from .short_dom import ShortDom
from . import general_steps
from lettuce_setup.utils import *
from accounts.models import User


def trans(text):
    return ugettext_lazy(text).__unicode__()


def has_class(self, class_name):
    return class_name in self.get_attribute('class').split(' ')


WebElement.has_class = has_class


def should_has_class(self, class_name):
    return self.has_class(class_name).should.be.ok


WebElement.should_has_class = should_has_class


def should_be_temp_link(self):
    self.tag_name.should.equal('a')
    self.get_attribute('href').should.equal(browser().current_url + '#')


WebElement.should_be_temp_link = should_be_temp_link


def fillin(self, value):
    assert isinstance(self, WebElement)
    if self.tag_name == 'textarea':
        if self.value_of_css_property('display').lower() == 'none':
            try:
                cke_container = self.xpath('../div')
                if cke_container.has_class('cke'):
                    browser().switch_to_frame(cke_container.find(".cke_wysiwyg_frame"))
                    find(".cke_editable").send_keys(value)
                    browser().switch_to_default_content()
                    return
            except NoSuchElementException:
                pass
    self.clear()
    self.send_keys(value)
    obj = self
    until(lambda: obj.get_attribute('value') == value)


WebElement.fillin = fillin


def django_url(url="", host='localhost'):
    base_url = "http://%s" % host
    port = getattr(settings, 'LETTUCE_SERVER_PORT', 8000)
    if port is not 80:
        base_url += ':%d' % port

    return urlparse.urljoin(base_url, url)


def visit(url):
    browser().get(django_url(url))


def visit_by_view_name(name, **kwargs):
    visit(reverse(name, **kwargs))


def current_page_link(selector):
    return find(selector + " .pagination .current")


def first_page_link(selector):
    return find(selector + " .pagination .first")


def previous_page_link(selector):
    return find(selector + " .pagination .prev")


def next_page_link(selector):
    return find(selector + " .pagination .next")


def last_page_link(selector):
    return find(selector + " .pagination .last")


def init_list_item_ids(selector):
    if not hasattr(world, 'list_items'):
        world.list_items = {}
    if world.list_items.get(selector) is None:
        world.list_items[selector] = {}


def save_list_item_ids(page, selector):
    init_list_item_ids(selector)
    items = []
    for item_object in find_all(selector):
        items.append(item_object.get_attribute('item_id'));
    world.list_items[selector][page] = items


def compare_list_item_ids(page1, page2, selector):
    init_list_item_ids(selector)
    if page1 not in world.list_items[selector].keys():
        raise Exception("Item list page %s was not saved" % page1)

    if page2 not in world.list_items[selector].keys():
        raise Exception("Item list page %s was not saved" % page2)
    return set(world.list_items[selector][page1]) == set(world.list_items[selector][page2])


def check_title(title):
    find("#content")
    browser().title.should.contain(title)


def execute_sql(sql):
    db_commit()
    cursor = connection.cursor()
    cursor.execute(sql)
    cursor.close()


def default_user(number=1):
    if number in world.users:
        return world.users[number]
    try:
        user = User.objects.create_user(
            'username%s' % number,
            'test.servicerequestsdistribute+user%s@gmail.com' % number,
            'password')
    except Exception, ex:
        pdb.set_trace()
        user = User.objects.get_by_natural_key('username%s' % number)
    user.raw_password = 'password'
    world.users[number] = user
    return user


@before.each_scenario
def clear_user(scenario):
    User.objects.all().delete()
    world.users = {}


def eval_sql(sql):
    db_commit()
    cursor = connection.cursor()
    cursor.execute(sql)
    value = cursor.fetchone()
    cursor.close()
    return value[0]


@step(u'I was a visitor')
def i_was_a_visitor(step):
    pass  # we dont need to do anything for now


@step(u'I was a logged in user')
def i_was_a_logged_in_user(step, number=1):
    visit_by_view_name('login')
    user = default_user(number)
    find("#id_username").send_keys(user.username)
    find("#id_password").send_keys(user.raw_password)
    find("#id_login").click()
    find("footer")


def super_group():
    if not hasattr(world, 'super_group'):
        from django.contrib.auth.models import Group

        try:
            world.super_group = Group.objects.get(name='super_group')
        except ObjectDoesNotExist:
            world.super_group = Group.objects.create(name='super_group')
        default_user(3).groups.add(world.super_group)
    return world.super_group


def right_nav_bar():
    return find(".nav.navbar-nav.navbar-right");


def logout_current_user():
    right_nav_bar().find("a").click()
    right_nav_bar().find(".logout").click()


def login_another_user(step):
    i_was_a_logged_in_user(step, 2)


def random_password():
    return settings.TEST_PASSWORD


def email_address():
    return settings.TEST_EMAIL


def db_commit():
    # try to commit database connection to fetch latest result for test
    try:
        connection.commit()
    except TransactionManagementError:
        pass  # this is expteced error


class datetime_fake:
    timedelta = datetime.timedelta(0)

    @classmethod
    def timepass(cls, timedelta):
        cls.timedelta += timedelta

    @classmethod
    def now(cls):
        return datetime.datetime.now() + cls.timedelta


@step(u'I should see the text "([^"]*)"')
def i_should_see_the_text(step, text):
    find("body").text.should.contain(text)


@step(u'I click on link "([^"]*)"')
def i_click_on_link(step, text):
    browser().find_element_by_link_text(text).click()


@step(u'I click on button "([^"]*)"')
def i_click_on(step, text, parent="body"):
    ShortDom.button(text, parent).click()


@step(u'I should see the notification "([^"]*)"')
def i_should_see_the_notification(step, notification):
    until(lambda: find(".notifications").text.should.contain(notification))


@step(u'I should see the button "([^"]*)"')
def i_should_see_the_button(step, text):
    ShortDom.button(text).should.be.ok


@step(u'I should see the link "([^"]*)"')
def i_should_see_the_link(step, text):
    ShortDom.link(text).should.be.ok


@before.each_step
def commit_db(step):
    db_commit()


def link(link_text, parent="body"):
    for node in find_all(parent):
        try:
            return node.find_element_by_link_text(link_text)
        except:
            pass
    return False


@step(u'button "([^"]*)" is set to state "([^"]*)"')
def then_button_is_set_to_state(step, button_text, state):
    ShortDom.button(button_text).has_class("btn-%s" % state)


@after.each_scenario
def after_scenario(scenario):
    if hasattr(world, 'browser'):
        world.browser.get(django_url("/"))
        world.browser.delete_all_cookies()


@after.harvest
def close_browser(total):
    if hasattr(world, 'browser'):
        world.browser.quit()
        del world.browser


def switch_to_2nd_window():
    browser().switch_to.window(browser().window_handles[1])


def switch_to_1st_window():
    browser().switch_to.window(browser().window_handles[0])


def on_second_window_do(func):
    def decorator(*args, **kwargs):
        the_browser = browser()
        current_window = the_browser.current_window_handle

        window_handles = the_browser.window_handles
        if len(window_handles) > 2:
            raise Exception("Currently have only 1 browser window.")
        window_handles.remove(current_window)
        second_window = window_handles[0]
        the_browser.switch_to_window(second_window)

        func(*args, **kwargs)

        the_browser.switch_to_window(current_window)

    return decorator
