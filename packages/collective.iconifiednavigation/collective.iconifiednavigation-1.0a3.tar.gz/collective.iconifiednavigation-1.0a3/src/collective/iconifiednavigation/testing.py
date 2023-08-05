# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.iconifiednavigation


class CollectiveIconifiednavigationLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.iconifiednavigation)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.iconifiednavigation:default')


COLLECTIVE_ICONIFIEDNAVIGATION_FIXTURE = CollectiveIconifiednavigationLayer()


COLLECTIVE_ICONIFIEDNAVIGATION_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_ICONIFIEDNAVIGATION_FIXTURE,),
    name='CollectiveIconifiednavigationLayer:IntegrationTesting',
)


COLLECTIVE_ICONIFIEDNAVIGATION_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_ICONIFIEDNAVIGATION_FIXTURE,),
    name='CollectiveIconifiednavigationLayer:FunctionalTesting',
)


COLLECTIVE_ICONIFIEDNAVIGATION_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_ICONIFIEDNAVIGATION_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='CollectiveIconifiednavigationLayer:AcceptanceTesting',
)
