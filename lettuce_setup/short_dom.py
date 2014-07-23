'''
Created on Apr 10, 2014

@author: eastagile
'''

from selenium_shortcut import find, find_all

class ShortDom(object):
    @classmethod
    def element_by_tagname_and_text(cls, tag, text, parent="body"):
        _xpath = ".//%s[.='%s']" % (tag, text)
        for node in find_all(parent):
            try:
                return node.xpath(_xpath)
            except:
                pass
        return False

    @classmethod
    def button(cls, button_text, parent="body"):
        return cls.element_by_tagname_and_text("button", button_text, parent)

    @classmethod
    def label(cls, label_text, parent="body"):
        return cls.element_by_tagname_and_text("label", label_text, parent)

    @classmethod
    def link(cls, link_text, parent="body"):
        return cls.element_by_tagname_and_text("a", link_text, parent)

    @classmethod
    def element_for_label(cls, label):
        return find("#%s" % label.get_attribute("for"))
