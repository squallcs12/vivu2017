'''
Created on Aug 25, 2013

@author: antipro
'''
from selenium.common.exceptions import NoSuchWindowException
from lettuce_setup.function import *
import facebook
from django.conf import settings


@step(u'I login using my facebook account')
def i_login_using_my_facebook_account(step):
    visit_by_view_name('login')
    find("#social_login #facebook").click()
    try:
        browser().find_element_by_name('__CONFIRM__').click()
    except NoSuchElementException:
        if find_all("#email"):
            find("#email").fillin("lisa_ubhedvc_narayananman@tfbnw.net")
            find("#pass").fillin(settings.TEST_PASSWORD)
            find("#loginbutton").click()


@step(u'I was asked to update my account password')
def i_was_asked_to_update_my_account_password(step):
    find("#set_password_form")


@step(u'I update my account password')
def i_update_my_account_password(step):
    find("#set_password_form input[name='new_password1']").send_keys(random_password())
    find("#set_password_form input[name='new_password2']").send_keys(random_password())
    find("#set_password_form input[type='submit']").click()

    until(lambda: browser().title.should.contain(trans(u"Password set successful")))


@step(u'I login using my twitter account')
def i_login_using_my_twitter_account(step):
    visit_by_view_name('login')
    find("#social_login #twitter").click()
    if len(find_all("#oauth_form #username_or_email")):  # if need login
        find("#oauth_form #username_or_email").send_keys(email_address())
        find("#oauth_form #password").send_keys(random_password())
        find("#oauth_form #allow").click()
    until(lambda: browser().current_url.find("/accounts/") != -1)


@step(u'my account was associated with both facebook and twitter')
def my_account_was_associated_with_both_facebook_and_twitter(step):
    then_my_account_was_associated_with_facebook(step)
    len(find_all("#social_accounts .social-twitter")).should.equal(1)


@step(u'I login using my google account')
def i_login_using_my_google_account(step):
    visit_by_view_name('login')
    find("#social_login #google").click()
    if len(browser().window_handles) == 2:  # google login window appear
        switch_to_2nd_window()

        find("#gaia_loginform #Email").send_keys(email_address())
        find("#gaia_loginform #Passwd").send_keys(random_password())
        find("#gaia_loginform #signIn").click()

        time.sleep(5)  # fix the case window is closed
        try:
            find("#submit_approve_access")
        except NoSuchWindowException:
            pass

        if len(browser().window_handles) == 2:  # first time accept
            until(lambda: find("#submit_approve_access").get_attribute('disabled') is None, 10)
            find("#submit_approve_access").click()

        switch_to_1st_window()

@step(u'my account was associated with facebook, twitter and google')
def my_account_was_associated_with_facebook_twitter_and_google(step):
    my_account_was_associated_with_both_facebook_and_twitter(step)
    len(find_all("#social_accounts .social-google-plus")).should.equal(1)


@step(u'When I go to the login page')
def when_i_go_to_the_login_page(step):
    visit_by_view_name('login')


@step(u'Then I did not see the login form')
def then_i_did_not_see_the_login_form(step):
    len(find_all("#login_form")).should.equal(0)


@step(u'And I see the notification that I am currently login')
def and_i_see_the_notification_that_i_am_currently_login(step):
    find("body").text.should.contain(trans(u"You are currently logged in as"))


@step(u'Then my account was associated with facebook')
def then_my_account_was_associated_with_facebook(step):
    visit_by_view_name('accounts_social_list')
    len(find_all("#social_accounts .social-facebook")).should.equal(1)

