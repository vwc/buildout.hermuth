from five import grok
from plone.directives import dexterity, form
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from zope import schema
from zope.component import getUtility
from zope.component import getMultiAdapter
from plone.namedfile.field import NamedImage
from plone.app.imaging.scale import ImageScale
from plone.app.imaging.scaling import ImageScaling
from z3c.form import group, field
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget

from whermuth.sitecontent import MessageFactory as _

from product import IProduct

# Interface class; used to define content-type schema.

class IProductFolder(form.Schema):   
    """
    Products Folder
    """
    title = schema.TextLine(
            title=_(u"Name"),
            required=True,
    )
    
    description = schema.Text(
                  title=_(u"A short summary"),
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

class ProductFolder(dexterity.Item):
    grok.implements(IProductFolder)
    
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

class ProductOverView(grok.View):
    grok.context(IProductFolder)
    grok.require('zope2.View')
    grok.name('view')    
    
    def haveProducts(self):
        return len(self.contained_products()) > 0
    
    def contained_products(self):
        """ Return a list of contained teasers in order to construct aitem scrollable. """
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(object_provides=IProduct.__identifier__,
                          path='/'.join(context.getPhysicalPath()),
                          review_state='published',
                          sort_on='getObjPositionInParent')
        items = []
        for r in results:
            item={}
            item ['title']=r.Title
            item ['description']=r.Description
            item ['url']=r.getURL()
            item ['imageTag']=self.constructImageTag(r.getObject())
            items.append(item)
        return items
        
    def constructImageTag(self, obj):

        scales = getMultiAdapter((obj, self.request), name='images')
        scale = scales.scale('ovImage', scale='thumb', height='150', width='115')
        imageTag = None,
        if scale is not None:
            imageTag = scale.tag()
        return imageTag                     
