'''
Created on Apr 20, 2014

@author: antipro
'''
from lettuce import step
from .selenium_shortcut import *
from lettuce_setup.short_dom import ShortDom
from lettuce_setup.utils import until_pass, until

@step(u'I should see a modal show up')
@until_pass
def i_should_see_a_modal_show_up(step):
    seen = False
    for modal in find_all(".modal"):
        if modal.is_displayed():
            seen = True
            break
    seen.should.be.true

@step(u'I should see on modal "([^"]*)"')
def i_should_see_on_modal(step, text):
    find(".modal").text.should.contain(text)

@step(u'I should see option on modal "([^"]*)"')
def i_should_see_option_on_modal(step, option_text):
    label = ShortDom.label(option_text)
    label.should.be.ok
    ShortDom.element_for_label(label).should.be.ok

@step(u'I should see button on modal "([^"]*)"')
def i_should_see_button_on_modal(step, button_text):
    ShortDom.button(button_text, ".modal").should.be.ok

@step(u'I should see checkbox on modal "([^"]*)"')
def i_should_see_checkbox_on_modal(step, checkbox_text):
    label = ShortDom.label(checkbox_text)
    label.should.be.ok
    checkbox = ShortDom.element_for_label(label)
    checkbox.should.be.ok
    checkbox.get_attribute("type").should.equal("checkbox")

@step(u'I click label on modal "([^"]*)"')
def i_click_label_on_modal(step, label_text):
    ShortDom.label(label_text, ".modal").click()

@step(u'I click button on modal "([^"]*)"')
def i_click_button_on_modal(step, button_text):
    ShortDom.button(button_text, ".modal").click()

@step(u'I fillin on modal field "([^"]*)" text "([^"]*)"')
def i_fillin_on_modal_field_by_value(step, label_text, value):
    label = ShortDom.label(label_text, ".modal")
    ShortDom.element_for_label(label).fillin(value)

@step(u'I should see the popup notification "([^"]*)"')
def i_should_see_the_popup_notification(step, text):
    until(lambda: find("#popup-notification").is_displayed().should.be.true)
    find("#popup-notification .modal-body").text.should.contain(text)
