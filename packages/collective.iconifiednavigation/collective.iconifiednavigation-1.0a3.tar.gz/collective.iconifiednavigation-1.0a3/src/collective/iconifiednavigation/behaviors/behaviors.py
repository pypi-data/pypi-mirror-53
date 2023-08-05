# encoding: utf-8
from collective.iconifiednavigation import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.namedfile.field import NamedImage
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from zope.interface import provider



@provider(IFormFieldProvider)
class INaviagationIcon(model.Schema):

    fieldset(
        'images',
        label=_(u'Navigation icon'),
        fields=['navigation_icon'],
    )

    navigation_icon = NamedImage(
        title=_('Icon'),
        description=_(u'This image is shown on navigation bar'),
        required=False,
    )
