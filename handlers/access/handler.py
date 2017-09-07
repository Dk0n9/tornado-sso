# coding: utf8
import model
from handlers import base


class AccessIndex(base.BaseHandler):

    def initialize(self, **kwargs):
        super(AccessIndex, self).initialize(**kwargs)
        self._dbOperate = model.Model(self.db)

    def get(self, *args, **kwargs):
        referer = self.get_query_argument('referer', None)

        if not self.current_user:
            return self.write_error(500)
        urlObject = self.functions.parseURL(referer)
        if self._isDomainInWhiteLists(urlObject.hostname):
            appObject = self._dbOperate.getAppInfoByDomain(urlObject.hostname)
            if not appObject:
                return self.write_error(500)
            ticket = self._grantTicket(appObject.app_id, appObject.client_ticket_expires, appObject.client_secret)
            if not ticket:
                return self.write_error(500)
            url = appObject.client_api + '?ticket={0}&referer={1}'.format(ticket, referer)
            return self.redirect(url)
        return self.write_error(500)

    def _grantTicket(self, appID, ticketExpires, appSecret):
        """分配 Service Ticket"""
        ticket = self.functions.generateServiceTicket(appSecret)
        userID = self.current_user.user_id
        created = self.functions.getNowTime()
        if self._dbOperate.addTicket(ticket, created, ticketExpires, userID, appID):
            return ticket
        else:
            return False

    def _isDomainInWhiteLists(self, domain):
        # TODO: 目前只匹配完整域名，后期再考虑应用有子域名的情况
        whiteLists = self._dbOperate.getAppDomainLists()
        if domain in whiteLists:
            return True
        else:
            return False


class AccessCheck(base.BaseHandler):

    def initialize(self, **kwargs):
        super(AccessCheck, self).initialize(**kwargs)
        self._dbOperate = model.Model(self.db)

    def get(self, *args, **kwargs):
        secret = self.get_query_argument('secret', None)
        ticket = self.get_query_argument('ticket', None)
        referer = self.get_query_argument('referer', None)

        appObject = self._dbOperate.getAppInfoBySecret(secret)
        urlObject = self.functions.parseURL(referer)
        if not appObject:
            return self.write_error(500)
        if urlObject:
            if urlObject.hostname != appObject.client_domain:
                return self.write_error(500)
        else:
            referer = appObject.client_url

        ticketObject = self._dbOperate.getTicketInfo(ticket)
        if not ticketObject:
            return self.write_error(500)
        if ticketObject.tbl_apps_id != appObject.app_id:
            return self.write_error(500)
        result = self._dbOperate.setTicketUsed(ticket)
        if not result:
            return self.write_error(500)
        self.redirect(referer)

    def _isDomainInWhiteLists(self, domain):
        # TODO: 目前只匹配完整域名，后期再考虑应用有子域名的情况
        whiteLists = self._dbOperate.getAppDomainLists()
        if domain in whiteLists:
            return True
        else:
            return False
