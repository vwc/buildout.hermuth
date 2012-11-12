from five import grok
from Acquisition import aq_inner
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from plone.app.layout.navigation.interfaces import INavigationRoot
from Products.CMFPlone.utils import safe_unicode

from whermuth.landingpage.landingpage import ILandingPage
from whermuth.landingpage.lpt import ILPT


class FrontPageView(grok.View):
    grok.context(INavigationRoot)
    grok.require('zope2.View')
    grok.name('frontpage-view')

    def update(self):
        self.has_landingpage = len(self.landingpage()) > 0

    def landingpage(self):
        """ Get the first contained object of type landing page.
        """
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(object_provides=ILandingPage.__identifier__,
                          review_state='published',
                          path=dict(query='/'.join(context.getPhysicalPath()),
                                    depth=1),)
        if len(results) > 0:
            result = results[:1]
            result_obj = result[0].getObject()
            frontpage = {}
            frontpage['text'] = result_obj.attainment
            frontpage['teasers'] = self.contained_teasers(result_obj)
            return frontpage
        else:
            return ''

    def contained_teasers(self, obj):
        """ Return a list of contained teasers in order to construct a
            scrollable.
        """
        context = aq_inner(obj)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(object_provides=ILPT.__identifier__,
                          path='/'.join(context.getPhysicalPath()),
                          review_state='published',
                          sort_on='getObjPositionInParent')
        lpts = []
        for result in results:
            lpt = {}
            lpt['title'] = safe_unicode(result.Title)
            lpt['description'] = safe_unicode(result.Description)
            lpt['url'] = result.getURL()
            lpt['imageTag'] = self.constructImageTag(result.getObject())
            lpts.append(lpt)
        return lpts

    def constructImageTag(self, obj):
        scales = getMultiAdapter((obj, self.request), name='images')
        scale = scales.scale('image', scale='thumb', height='100', width='100')
        lptTag = None,
        if scale is not None:
            lptTag = scale.tag()
        return lptTag
