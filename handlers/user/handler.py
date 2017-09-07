# coding: utf8
"""
前台用户模块，包含：
   登录、注册、注销、个人页面及相关校验API
"""

import model
from handlers import base


class LoginIndex(base.BaseHandler):

    def initialize(self, **kwargs):
        super(LoginIndex, self).initialize(**kwargs)
        self._dbOperate = model.Model(self.db)

    def get(self, *args, **kwargs):
        referer = self.get_query_argument('referer', None)
        if self.current_user:
            if referer:
                urlObject = self.functions.parseURL(referer)
                if self._isDomainInWhiteLists(urlObject.hostname):
                    appInfo = self._dbOperate.getAppInfoByDomain(urlObject.hostname)
                    self.render('app_access.html', clientURL=appInfo.client_url,
                                clientName=appInfo.app_name, referer=referer)
                    return None
            self.redirect('/profile')
        else:
            if referer:
                urlObject = self.functions.parseURL(referer)
                if self._isDomainInWhiteLists(urlObject.hostname):
                    appInfo = self._dbOperate.getAppInfoByDomain(urlObject.hostname)
                    self.render('app_unauthorized_access.html', clientURL=appInfo.client_url,
                                clientName=appInfo.app_name, referer=referer)
                    return None
            self.render('login.html')

    def post(self, *args, **kwargs):
        userMail = self.get_argument('usermail', None)
        userPwd = self.get_argument('password', None)
        referer = self.get_query_argument('referer', None)
        message = {
            'status': False,
            'result': '',
            'message': ''
        }

        if not userMail and not userPwd:
            message['message'] = u'参数有误'
            return self.write(message)
        userInfo = self._dbOperate.getUserInfoByMail(userMail)
        if not userInfo:
            message['message'] = u'用户名或密码错误'
            return self.write(message)
        tempCiphertext = self.functions.generatePassword(userPwd, userInfo.user_salt)
        if tempCiphertext != userInfo.user_pwd:
            message['message'] = u'用户名或密码错误'
            return self.write(message)

        # 设置Cookie，关闭浏览器时Cookie自动失效
        self.set_secure_cookie('session', userMail, expires_days=None)

        if not referer:
            message['status'] = True
            message['result'] = '/profile'
            message['message'] = u'登录成功，正在跳转...'
        else:
            urlObject = self.functions.parseURL(referer)
            if self._isDomainInWhiteLists(urlObject.hostname):
                message['status'] = True
                message['result'] = '/access?referer=' + referer
                message['message'] = u'登录成功，正在跳转...'
            else:
                message['status'] = True
                message['result'] = '/profile'
                message['message'] = u'登录成功，正在跳转...'
        self.write(message)


    def _isDomainInWhiteLists(self, domain):
        # TODO: 目前只匹配完整域名，后期再考虑应用有子域名的情况
        whiteLists = self._dbOperate.getAppDomainLists()
        if domain in whiteLists:
            return True
        else:
            return False


class RegisterIndex(base.BaseHandler):

    def initialize(self, **kwargs):
        super(RegisterIndex, self).initialize(**kwargs)
        self._dbOperate = model.Model(self.db)

    def get(self, *args, **kwargs):
        self.render('register.html')

    def post(self, *args, **kwargs):
        username = self.get_argument('v_username')
        usermail = self.get_argument('v_usermail')
        password = self.get_argument('v_password')
        confirm = self.get_argument('v_confirm')

        message = {
            'status': False,
            'result': '',
            'message': ''
        }

        checkResult = self._checkParams(username, usermail, password, confirm)
        if not checkResult[0]:
            message['message'] = checkResult[1]
            self.write(message)
            return None
        if self._dbOperate.isUserNameExist(username):
            message['message'] = u'用户名已被注册'
            self.write(message)
            return None
        if self._dbOperate.isUserEmailExist(usermail):
            message['message'] = u'邮箱已被注册'
            self.write(message)
            return None

        salt = self.functions.generateSalt()
        cipherText = self.functions.generatePassword(password, salt)
        timestamp = self.functions.getNowTime()
        result = self._dbOperate.addUser(user_name=username, user_email=usermail, user_pwd=cipherText,
                                         user_salt=salt, user_avatar='images/gavatar.jpg', user_create_timestamp=timestamp)
        if result:
            message['status'] = True
            message['result'] = self.get_login_url()
        else:
            message['message'] = u'未知错误'
        self.write(message)

    def _checkParams(self, name, mail, pwd, confirm):
        if not name or not mail or not pwd or not confirm:
            return [False,  u'选项不能为空']
        if not self.functions.validateEmail(mail):
            return [False, u'请输入正确的邮箱']
        if len(pwd) > 32:
            return [False, u'密码长度不符合规则']
        if pwd != confirm:
            return [False, u'两次输入密码不一致']
        return [True]


class LogoutIndex(base.BaseHandler):

    def initialize(self, **kwargs):
        super(LogoutIndex, self).initialize(**kwargs)
        self._dbOperate = model.Model(self.db)

    def get(self, *args, **kwargs):
        referer = self.get_query_argument('referer', None)
        if not self.current_user:
            self.redirect(self.get_login_url())
            return self.finish()

        self.clear_cookie('session')
        if referer:
            urlObject = self.functions.parseURL(referer)
            if self._isDomainInWhiteLists(urlObject.hostname):
                self.redirect(referer)
        self.redirect(self.get_login_url())


class UserProfile(base.BaseHandler):

    def initialize(self, **kwargs):
        super(UserProfile, self).initialize(**kwargs)
        self._dbOperate = model.Model(self.db)

    def get(self, *args, **kwargs):
        self.write(self.current_user.user_name)


class CheckUserAPI(base.BaseHandler):
    """校验用户名和用户邮箱是否已被注册"""

    def initialize(self, **kwargs):
        super(CheckUserAPI, self).initialize(**kwargs)
        self._dbOperate = model.Model(self.db)

    def post(self, *args, **kwargs):
        message = {
            'status': False,
            'result': '',
            'message': ''
        }
        name = self.get_argument('username', None)
        mail = self.get_argument('usermail', None)
        if not name and not mail:
            message['message'] = u'参数不能为空'
            self.write(message)
            return None
        if self._dbOperate.isUserNameExist(name):
            message['message'] = u'用户名已存在'
            self.write(message)
            return None
        if self._dbOperate.isUserEmailExist(mail):
            message['message'] = u'邮箱已被注册'
            self.write(message)
            return None
        message['status'] = True
        self.write(message)
