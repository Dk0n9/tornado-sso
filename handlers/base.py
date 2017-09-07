# coding: utf-8
from tornado.web import RequestHandler

from models.users import Model as UserModel


class BaseHandler(RequestHandler):

    db = None
    functions = None
    logging = None

    def initialize(self, **kwargs):
        if kwargs:
            self.db = kwargs.get('db')
            self.functions = kwargs.get('functions')
            self.logging = kwargs.get('logging')

    @property
    def getUserIP(self):
        return self.request.remote_ip

    def get_login_url(self):
        return self.reverse_url('login')

    def get_current_user(self):
        userMail = self.get_secure_cookie('session', None)
        if userMail is None:
            return None
        try:
            raw = self.db.query(UserModel).filter(UserModel.user_email==userMail).one()
            return raw
        except Exception, e:
            return False

    def get_template_namespace(self):
        """
        update namespace
        """
        namespace = super(BaseHandler, self).get_template_namespace()
        name = {
            'sftime': self.functions.formatTime
        }
        namespace.update(name)
        return namespace

    def on_finish(self):
        self.db.close()

    def write_error(self, status_code, **kwargs):
        # 405状态码转404
        if status_code == 405:
            status_code = 404
        self.set_status(200)
        self.render('error.html', error=status_code)
