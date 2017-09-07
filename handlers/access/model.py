# coding: utf8

from models.apps import Model as appModel
from models.tickets import Model as TicketModel


class Model(object):

    def __init__(self, dbSession):
        self._session = dbSession

    def getAppDomainLists(self):
        raw = self._session.query(appModel.client_domain).filter(appModel.client_enable==1).all()
        result = []
        for domain in raw:
            result.append(domain[0])
        return result

    def getAppInfoByDomain(self, domain):
        try:
            raw = self._session.query(appModel).filter(appModel.client_domain==domain,
                                                       appModel.client_enable==1).one()
            if not raw:
                return False
            return raw
        except Exception, e:
            return False

    def getAppInfoBySecret(self, secret):
        try:
            raw = self._session.query(appModel).filter(appModel.client_secret==secret,
                                                       appModel.client_enable==1).one()
            if not raw:
                return False
            return raw
        except Exception, e:
            return False

    def addTicket(self, value, created, expires, userID, appID):
        expires = created + expires
        ticketObject = TicketModel(ticket_value=value, ticket_created=created, ticket_expires=expires,
                                   ticket_used=0, tbl_users_id=userID, tbl_apps_id=appID)
        try:
            self._session.add(ticketObject)
            self._session.commit()
            return True
        except Exception, e:
            return False

    def getTicketInfo(self, ticket):
        try:
            raw = self._session.query(TicketModel).filter(TicketModel.ticket_value==ticket,
                                                          TicketModel.ticket_used==0).one()
            if not raw:
                return False
            return raw
        except Exception, e:
            return False

    def setTicketUsed(self, ticket):
        """设置该 ticket标志为已使用"""
        try:
            raw = self._session.query(TicketModel).filter(TicketModel.ticket_value == ticket,
                                                          TicketModel.ticket_used == 0).one()
            if not raw:
                return False
            raw.ticket_used = 1
            self._session.commit()
            return True
        except Exception, e:
            return False
