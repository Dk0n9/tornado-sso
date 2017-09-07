# coding: utf-8
from sqlalchemy import Column
from sqlalchemy.dialects.mysql.types import INTEGER,VARCHAR, CHAR, TINYINT

import db


class Model(db.Base):
    __tablename__ = 'tbl_apps'
    app_id = Column(INTEGER(11), primary_key=True, autoincrement=True)
    app_name = Column(VARCHAR(50))
    client_url = Column(VARCHAR(255))
    client_api = Column(VARCHAR(255))
    client_domain = Column(VARCHAR(255))
    client_secret = Column(CHAR(32))
    client_ticket_expires = Column(INTEGER(11))
    client_enable = Column(TINYINT(1))  # boolean