from five import grok
from plone.directives import dexterity, form
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from zope import schema
from zope.component import getMultiAdapter

from whermuth.sitecontent import MessageFactory as _

from product import IProduct


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


class ProductFolder(dexterity.Item):
    grok.implements(IProductFolder)


class ProductOverView(grok.View):
    grok.context(IProductFolder)
    grok.require('zope2.View')
    grok.name('view')

    def haveProducts(self):
        return len(self.contained_products()) > 0

    def contained_products(self):
        """ Return a list of contained teasers in order to construct a
            item scrollable.
        """
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(object_provides=IProduct.__identifier__,
                          path='/'.join(context.getPhysicalPath()),
                          review_state='published',
                          sort_on='getObjPositionInParent')
        items = []
        for r in results:
            item = {}
            item['title'] = r.Title
            item['description'] = r.Description
            item['url'] = r.getURL()
            item['imageTag'] = self.constructImageTag(r.getObject())
            items.append(item)
        return items

    def constructImageTag(self, obj):
        scales = getMultiAdapter((obj, self.request), name='images')
        scale = scales.scale('ovImage',
                             scale='thumb',
                             height='150',
                             width='115')
        imageTag = None,
        if scale is not None:
            imageTag = scale.tag()
        return imageTag
