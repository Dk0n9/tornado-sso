# coding: utf8

from models.apps import Model as appModel
from models.users import Model as userModel

from tornado.log import app_log


class Model(object):

    def __init__(self, dbSession):
        self._session = dbSession

    def getUserInfoByMail(self, email):
        try:
            raw = self._session.query(userModel).filter(userModel.user_email == email).one()
            if not raw:
                return False
            return raw
        except Exception, e:
            return False

    def addUser(self, **kwargs):
        userObject = userModel(**kwargs)
        try:
            self._session.add(userObject)
            self._session.commit()
            return True
        except Exception, error:
            app_log.error(error)
            return False

    def isUserNameExist(self, name):
        raw = self._session.query(userModel).filter(userModel.user_name==name).first()
        if raw:
            return True
        else:
            return False

    def isUserEmailExist(self, email):
        raw = self._session.query(userModel).filter(userModel.user_email == email).first()
        if raw:
            return True
        else:
            return False

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
