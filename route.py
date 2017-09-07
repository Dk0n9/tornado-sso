# coding: utf-8

from tornado.web import url

from handlers.user.handler import *
from handlers.access.handler import *


def getRoutes(options):
    routes = []

    # <-- USER MODULE --> #
    routes.extend([url(r'^/login$', LoginIndex, dict(options), name='login'),
                   url(r'^/register$', RegisterIndex, dict(options), name='register'),
                   url(r'^/logout$', LogoutIndex, dict(options), name='logout'),
                   url(r'^/profile$', UserProfile, dict(options)),
                   url(r'^/check$', CheckUserAPI, dict(options))
                  ])
    # <-- ACCESS MODULE --> #
    routes.extend([url(r'^/access$', AccessIndex, dict(options)),
                   url(r'^/access_check$', AccessCheck, dict(options))
                   ])

    return routes
