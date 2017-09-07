# coding: utf-8
from sqlalchemy import asc, desc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


__all__ = ['Base', 'init', 'ASC', 'DESC']


Base = declarative_base()
ASC = asc
DESC = desc


def init(settings):
    engine = create_engine('{0}://{1}:{2}@{3}:{4}/{5}'.format(settings['driver'], settings['user'],
                                                              settings['pass'], settings['host'],
                                                              settings['port'], settings['db']),
                           encoding=settings['charset'], echo=settings.get('debug', False))
    engine.recycle = 3600
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    session.execute('SET NAMES {0}'.format(settings['charset']))  # 解决在部分机器上的编码问题
    return session
