from five import grok
from plone.directives import dexterity, form
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from zope import schema
from zope.component import getUtility
from zope.component import getMultiAdapter
from plone.app.imaging.scale import ImageScale
from plone.app.imaging.scaling import ImageScaling
from plone.namedfile.field import NamedImage
from Products.CMFPlone.utils import safe_unicode

from z3c.form import group, field
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget

from lpt import ILPT

from whermuth.landingpage import MessageFactory as _

# Interface class; used to define content-type schema.

class ILandingPage(form.Schema):
    """
    landinpage
    """
    title = schema.TextLine(
            title=_(u"Name"),
            required=True,
    )
    
    description = schema.Text(
                  title=_(u"A short summary"),
                  required=False,
    )
    
    form.widget(attainment="plone.app.z3cform.wysiwyg.widget.WysiwygFieldWidget")
    attainment = schema.Text(
                  title=_(u"Attainment"),
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

class LandingPage(dexterity.Item):
    grok.implements(ILandingPage)
    
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

class LandingPageView(grok.View):
    grok.context(ILandingPage)
    grok.require('zope2.View')
    grok.name('view')
    
    def haveLPTs(self):
        return len(self.contained_lpts()) > 0
    
    def contained_lpts(self):
        """ Return a list of contained teasers in order to construct a scrollable. """
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(object_provides=ILPT.__identifier__,
                          path='/'.join(context.getPhysicalPath()),
                          review_state='published',
                          sort_on='getObjPositionInParent')
        lpts = []
        for ref in results:
            lpt={}
            lpt ['title']=safe_unicode(ref.Title)
            lpt ['description']=safe_unicode(ref.Description)
            lpt ['url']=ref.getURL()
            lpt ['imageTag']=self.constructLPTTag(ref.getObject())
            lpts.append(lpt)
        return lpts
        
    def constructLPTTag(self, obj):

        scales = getMultiAdapter((obj, self.request), name='images')
        scale = scales.scale('image', scale='thumb', height='100', width='100')
        lptTag = None,
        if scale is not None:
            lptTag = scale.tag()
        return lptTag   
