# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import utils
from Products.CMFPlone.browser.interfaces import INavigationTabs
from Products.CMFPlone.browser.navigation import CatalogNavigationTabs
from Products.CMFPlone.browser.navigation import get_id
from Products.CMFPlone.browser.navigation import get_view_url
from Products.CMFPlone.interfaces import INavigationSchema
from plone.registry.interfaces import IRegistry
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.interface import implementer


@implementer(INavigationTabs)
class CatalogNavigationTabsHandlingLinks(CatalogNavigationTabs):

    def topLevelTabs(self, actions=None, category='portal_tabs'):
        context = aq_inner(self.context)
        registry = getUtility(IRegistry)
        navigation_settings = registry.forInterface(
            INavigationSchema,
            prefix="plone",
            check=False
        )
        mtool = getToolByName(context, 'portal_membership')
        member = mtool.getAuthenticatedMember().id
        catalog = getToolByName(context, 'portal_catalog')

        if actions is None:
            context_state = getMultiAdapter(
                (context, self.request),
                name=u'plone_context_state'
            )
            actions = context_state.actions(category)

        # Build result dict
        result = []
        # first the actions
        for actionInfo in actions:
            data = actionInfo.copy()
            data['name'] = data['title']
            data['object_url'] = data['url']
            result.append(data)

        # check whether we only want actions
        if not navigation_settings.generate_tabs:
            return result

        query = self._getNavQuery()

        rawresult = catalog.searchResults(query)

        def _get_url(item):
            if item.getRemoteUrl and not member == item.Creator:
                return (get_id(item), item.getRemoteUrl)
            return get_view_url(item)

        # now add the content to results
        for item in rawresult:
            if item.exclude_from_nav:
                continue
            cid, item_url = _get_url(item)
            data = {
                'name': utils.pretty_title_or_id(context, item),
                'id': item.getId,
                'url': item_url,
                'object_url': item.getURL(),
                'description': item.Description,
                'review_state': item.review_state
            }
            result.append(data)

        return result
