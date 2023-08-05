from django.contrib import admin
from cms.extensions import PageExtensionAdmin, TitleExtensionAdmin

from . import models

class ImageExtensionAdmin(PageExtensionAdmin):
    pass
admin.site.register(models.ImageExtension, ImageExtensionAdmin)


class TeaserExtensionAdmin(TitleExtensionAdmin):
    pass
admin.site.register(models.TeaserExtension, TeaserExtensionAdmin)
