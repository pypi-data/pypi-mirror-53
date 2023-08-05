# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import INonInstallable
from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import queryUtility
from zope.interface import implementer
from collective.iconifiednavigation.behaviors.behaviors import INaviagationIcon

@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            'collective.iconifiednavigation:uninstall',
        ]


def post_install(context):
    """Post install script"""
    """Add a behavior to a type"""
    portal_types = getToolByName(api.portal.get(), "portal_types")
    types = portal_types.listContentTypes()
    for type in types:
        fti = queryUtility(IDexterityFTI, name=type)
        if not fti:
            continue
        behaviors = list(fti.behaviors)
        print ""
        if INaviagationIcon.__identifier__ not in behaviors:
            behaviors.append(INaviagationIcon.__identifier__)
            fti._updateProperty('behaviors', tuple(behaviors))

# Do something at the end of the installation of this package.


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
