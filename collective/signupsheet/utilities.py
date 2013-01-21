# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName

from zope.interface import implements

from collective.signupsheet.interfaces import IGetRegistrants


class GetRegistrant(object):
    implements(IGetRegistrants)

    def get_registrants_brains(self, form):
        catalog = getToolByName(form, 'portal_catalog')
        registrants_folder = self.get_registrants_folder(form)
        if registrants_folder:
            path = '/'.join(registrants_folder.getPhysicalPath())
            brains = catalog(path={'query': path, 'depth': 1})
            return brains
        return []

    def get_registrants_folder(self, form):
        adapters = form.actionAdapter
        registrants_folder = None
        for ad in adapters:
            #I will take only the first object I will find in form
            if form[ad].portal_type == 'FormSaveData2ContentAdapter':
                registrants_folder = form[ad]
                break

        if not registrants_folder:
            return []

        return registrants_folder

    def get_registrants(self, form):
        """
        get all the registrants under this form
        """
        brains = self.get_registrants_brains(form)
        registrants = []
        for brain in brains:
            registrants.append(brain.getObject())

        return registrants

    #http://plone.293351.n2.nabble.com/PloneFormGen-activating-and-executing-a-different-mailer-adapter-depending-on-form-input-td5566077.html
