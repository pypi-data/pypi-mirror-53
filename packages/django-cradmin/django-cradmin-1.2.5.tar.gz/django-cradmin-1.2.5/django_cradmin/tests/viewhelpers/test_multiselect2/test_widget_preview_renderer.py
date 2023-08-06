import htmls
from django import test

from django_cradmin.viewhelpers.multiselect2 import widget_preview_renderer


class TestValue(test.TestCase):
    def test_css_class_added(self):
        selector = htmls.S(widget_preview_renderer.Value(
            value='testvalue').render())
        self.assertTrue(selector.exists('.django-cradmin-multiselect2-preview-list-value'))

    def test_wrap_in_li_element_false(self):
        selector = htmls.S(widget_preview_renderer.Value(
            value='testvalue', wrap_in_li_element=False).render())
        self.assertFalse(selector.exists('li'))

    def test_wrap_in_li_element_true(self):
        selector = htmls.S(widget_preview_renderer.Value(
            value='testvalue', wrap_in_li_element=True).render())
        self.assertTrue(selector.exists('li'))

    def test_render_value_wrap_in_li_element_false(self):
        selector = htmls.S(widget_preview_renderer.Value(
            value='testvalue', wrap_in_li_element=False).render())
        self.assertEqual(
            'testvalue',
            selector.one('.django-cradmin-listbuilder-itemvalue').alltext_normalized)

    def test_render_value_wrap_in_li_element_true(self):
        selector = htmls.S(widget_preview_renderer.Value(
            value='testvalue', wrap_in_li_element=True).render())
        self.assertEqual(
            'testvalue',
            selector.one('.django-cradmin-listbuilder-itemvalue').alltext_normalized)


class TestList(test.TestCase):
    def test_css_class_added(self):
        selector = htmls.S(widget_preview_renderer.List().render())
        self.assertTrue(selector.one('ol').hasclass('django-cradmin-multiselect2-preview-list'))

    def test_from_value_iterable_uses_the_new_default_value_render(self):
        listbuilder_list = widget_preview_renderer.List.from_value_iterable(
            value_iterable=['testvalue'])
        selector = htmls.S(listbuilder_list.render())
        self.assertTrue(selector.exists('.django-cradmin-multiselect2-preview-list-value'))
