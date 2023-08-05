from django.db.models import Q
from django.template.loader import select_template
from django.utils import translation

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models import Title

from django.utils.translation import ugettext_lazy as _

from . import models


class TeaserPluginBase(CMSPluginBase):
    def get_render_template(self, context, instance, placeholder):
        return select_template((
            self.TEMPLATE_NAME % instance.style,
            self.render_template,
        ))

    def get_titles(self):
        titles = Title.objects.filter(
            page__in=self.pages
        ).filter(
            language=translation.get_language()
        ).filter(
            teaserextension__isnull=False
        ).order_by(
            'page__node__path'
        )
        return titles


class PageImagePluginBase(TeaserPluginBase):
    def render(self, context, instance, placeholder):
        pages = self.get_pages(context, instance, placeholder)

        pages = pages.published(site=context['request'].site, language=translation.get_language())
        pages = pages.filter(
            Q(imageextension__show_preview=True) |
            Q(imageextension__isnull=True)
        )

        self.pages = pages

        context['pages'] = pages
        context['instance'] = instance
        context['current_page'] = context['request'].current_page
        return context


class CMSChildPagePreviewPlugin(PageImagePluginBase):
    model = models.ChildPagePreviewPlugin
    name = _("Child Page Preview")

    TEMPLATE_NAME = "djangocms_page_image/plugins/%s.html"
    render_template = TEMPLATE_NAME % 'child_page_preview'

    #Search
    search_fields = []

    def get_pages(self, context, instance, placeholder):
        return context['request'].current_page.get_child_pages()
plugin_pool.register_plugin(CMSChildPagePreviewPlugin)


class CMSSiblingPagePreviewPlugin(PageImagePluginBase):
    model = models.SiblingPagePreviewPlugin
    name = _("Sibling Page Preview")

    TEMPLATE_NAME = "djangocms_page_image/plugins/%s.html"
    render_template = TEMPLATE_NAME % 'sibling_page_preview'

    def get_pages(self, context, instance, placeholder):
        return context['request'].current_page.parent_page.get_child_pages()
plugin_pool.register_plugin(CMSSiblingPagePreviewPlugin)


class TitleTeaserPluginBase(TeaserPluginBase):
    def render(self, context, instance, placeholder):
        pages = self.get_pages(context, instance, placeholder)
        self.pages = pages.published(site=context['request'].site, language=translation.get_language())

        context['titles'] = self.get_titles()
        context['instance'] = instance

        return context


class ChildPageTeasersPlugin(TitleTeaserPluginBase):
    model = models.ChildPageTeasersPlugin
    name = _("Child Page Teasers")

    TEMPLATE_NAME = "djangocms_page_image/plugins/%s.html"
    render_template = TEMPLATE_NAME % 'child_page_teasers'

    #Search
    search_fields = []

    def get_pages(self, context, instance, placeholder):
        if instance.parent_page:
            return instance.parent_page.get_child_pages()
        else:
            return context['request'].current_page.get_child_pages()
plugin_pool.register_plugin(ChildPageTeasersPlugin)
