from five import grok
from plone.directives import dexterity, form
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from zope import schema
from zope.component import getMultiAdapter
from plone.namedfile.field import NamedImage
from Products.CMFPlone.utils import safe_unicode

from teaser import ITeaser

from whermuth.sitecontent import MessageFactory as _


class IProduct(form.Schema):
    """
    single product
    """
    title = schema.TextLine(
        title=_(u"Name"),
        required=True,
    )
    description = schema.Text(
        title=_(u"A short summary"),
        required=False,
    )
    ovImage = NamedImage(
        title=_(u"Picture"),
        description=_(u"Please upload an image"),
        required=False,
    )
    form.widget(main="plone.app.z3cform.wysiwyg.widget.WysiwygFieldWidget")
    main = schema.Text(
        title=_(u"Main Content"),
        required=False,
    )


class Product(dexterity.Item):
    grok.implements(IProduct)


class ProductView(grok.View):
    grok.context(IProduct)
    grok.require('zope2.View')
    grok.name('view')

    def haveTeasers(self):
        return len(self.contained_teasers()) > 0

    def contained_teasers(self):
        """ Return a list of contained teasers in order to construct a
            scrollable.
        """
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(object_provides=ITeaser.__identifier__,
                          path='/'.join(context.getPhysicalPath()),
                          review_state='published',
                          sort_on='getObjPositionInParent')
        teasers = []
        for ref in results:
            teaser = {}
            teaser['title'] = safe_unicode(ref.Title)
            teaser['description'] = safe_unicode(ref.Description)
            teaser['url'] = ref.getURL()
            teaser['imageTag'] = self.constructTeaserTag(ref.getObject())
            teasers.append(teaser)
        return teasers

    def constructTeaserTag(self, obj):
        scales = getMultiAdapter((obj, self.request), name='images')
        scale = scales.scale('image', scale='thumb')
        teaserTag = None,
        if scale is not None:
            teaserTag = scale.tag()
        return teaserTag
