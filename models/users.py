# coding: utf-8
from sqlalchemy import Column
from sqlalchemy.dialects.mysql.types import INTEGER,VARCHAR, CHAR

import db


class Model(db.Base):
    __tablename__ = 'tbl_users'
    user_id = Column(INTEGER(11), primary_key=True, autoincrement=True)
    user_name = Column(VARCHAR(50))
    user_email = Column(VARCHAR(255))
    user_pwd = Column(CHAR(64))
    user_salt = Column(CHAR(8))
    user_avatar = Column(VARCHAR(255))
    user_create_timestamp = Column(INTEGER(11))