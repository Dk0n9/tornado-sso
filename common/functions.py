# coding: utf8
import re
import json
import time
import random
import urlparse
import binascii
from hashlib import pbkdf2_hmac
from string import ascii_letters


def getNowTime():
    return int(time.time())  # 取十位


def formatTime(timestamp, format='%Y-%m-%d %H:%M:%S'):
    timeObj = time.localtime(int(timestamp))
    return time.strftime(format, timeObj)


def object2Json(dictObject):
    try:
        result = json.dumps(dictObject)
        return result
    except Exception, e:
        return False


def json2Object(jsonString):
    try:
        result = json.loads(jsonString)
        return result
    except Exception, e:
        return False


def validateEmail(email):
    match = r'^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$'
    try:
        if re.match(match, email) is not None:
            return True
    except Exception, e:
        print e
    return False


def parseURL(url):
    result = urlparse.urlparse(url)
    return result


def generateSalt(length=8):
    salt = ''.join(random.sample(ascii_letters, length))
    return salt


def generatePassword(source, salt):
    plainText = source[0] + salt + source[1:]
    mcrypt = pbkdf2_hmac('sha256', plainText, salt, 100000)
    return binascii.hexlify(mcrypt)  # length: 64


def generateAppSecret():
    randomString = generateSalt(16)
    randomSalt = generateSalt()
    return generatePassword(randomString, randomSalt)[32:]  # length: 32


def generateServiceTicket(appSecret):
    randomString = generateSalt(16)
    randomSalt = generateSalt()
    return generatePassword(appSecret + '+' + randomString, randomSalt)[32:]  # length: 32
