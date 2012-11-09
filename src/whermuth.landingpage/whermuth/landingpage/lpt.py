from five import grok
from plone.directives import dexterity, form
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from zope import schema

from plone.namedfile.field import NamedImage

from z3c.form import group, field
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget

from whermuth.landingpage import MessageFactory as _


# Interface class; used to define content-type schema.

class ILPT(form.Schema):
    """
    teaser
    """
    title = schema.TextLine(
            title=_(u"Name"),
            required=True,
    )
    
    description = schema.Text(
                  title=_(u"A short summary"),
                  required=False,
    )
    
    image = NamedImage(
            title=_(u"Picture"),
            description=_(u"Please upload an image"),
            required=False,
    )

    # If you want a schema-defined interface, delete the form.model
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/contacttype.xml to define the content type
    # and add directives here as necessary.


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class LPT(dexterity.Item):
    grok.implements(ILPT)
    
    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# contacttype_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class LPTView(grok.View):
    grok.context(ILPT)
    grok.require('zope2.View')
#    grok.name('view')
