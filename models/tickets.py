# coding: utf-8
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql.types import INTEGER, CHAR, TINYINT

import db


class Model(db.Base):
    __tablename__ = 'tbl_app_grant_tickets'
    ticket_id = Column(INTEGER(11), primary_key=True, autoincrement=True)
    ticket_value = Column(CHAR(32))
    ticket_created = Column(INTEGER(11))
    ticket_expires = Column(INTEGER(11))
    ticket_used = Column(TINYINT(1))  # boolean
    tbl_users_id = Column(INTEGER(11), ForeignKey('tbl_users.user_id'))
    tbl_apps_id = Column(INTEGER(11), ForeignKey('tbl_apps.app_id'))