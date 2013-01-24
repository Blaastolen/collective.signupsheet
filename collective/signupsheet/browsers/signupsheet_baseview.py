# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView

from zope.component import getUtility

from collective.signupsheet.interfaces import IGetRegistrants
from collective.signupsheet import signupsheetMessageFactory as _


class SignupSheetBaseView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def getSignupStatus(self, nextstatus=0):
        """Returns the status of the SignupSheet container"""
        status = ''
        event_size = self.context.getEventsize()
        waitlist_size = self.context.getWaitlist_size()
        utility = getUtility(IGetRegistrants)
        registrant_folder = utility.get_registrants_folder(self.context)
        current_size = len(registrant_folder.contentIds(filter={'portal_type': 'registrant'}))
        max_size = event_size + waitlist_size

        if current_size + nextstatus <= event_size:
            status = 'open'
        elif max_size - current_size <= waitlist_size:
            status = 'waitlist'

        if current_size >= max_size:
            status = 'full'

        if max_size == 0:
            status = 'open'

        return status

    def getSignupMessage(self):
        """ returns signup message for signupsheet_view """
        if self.getSignupStatus(nextstatus=1) == 'open':
            msg = _(u'sign_up', default='Sign up!')
        else:
            msg = _(u'sign_up_for_waitinglist', default='Signup for waiting list')
        return msg

    def getSeatsLeft(self):
        registrants = getUtility(IGetRegistrants).get_registrants_brains_anon
        registrants_number = len((registrants(self.context)))
        return self.context.getEventsize() +\
               self.context.getWaitlist_size() -\
               registrants_number
