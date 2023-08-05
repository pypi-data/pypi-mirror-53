# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db.models import Q
from django.core.exceptions import ValidationError

from cms.apphook_pool import apphook_pool
from cms.models import Page
from menus.base import Menu


class CMSAttachMenu(Menu):
    cms_enabled = True
    instance = None
    name = None

    def __init__(self, *args, **kwargs):
        super(CMSAttachMenu, self).__init__(*args, **kwargs)
        if self.cms_enabled and not self.name:
            raise ValidationError(
                "the menu %s is a CMSAttachMenu but has no name defined!" %
                self.__class__.__name__)

    @classmethod
    def get_apphooks(cls):
        """
        Returns a list of apphooks to which this CMSAttachMenu is attached.

        Calling this does NOT produce DB queries.
        """
        apps = []
        for key, _ in apphook_pool.get_apphooks():
            app = apphook_pool.get_apphook(key)
            if cls in app.get_menus():
                apps.append(app)
        return apps

    @classmethod
    def get_instances(cls):
        """
        Return a list (queryset, really) of all CMS Page objects (in this case)
        that are currently using this CMSAttachMenu either directly as a
        navigation_extender, or, as part of an apphook.

        Calling this DOES perform a DB query.
        """
        parent_apps = []
        for app in cls.get_apphooks():
            parent_apps.append(app.__class__.__name__)
        return Page.objects.filter(
            Q(application_urls__in=parent_apps)
            | Q(navigation_extenders=cls.__name__)
        )
