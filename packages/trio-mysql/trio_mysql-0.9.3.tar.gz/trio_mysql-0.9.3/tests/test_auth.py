"""Test for auth methods supported by MySQL 8"""

import os
import trio_mysql
from .base import testdb_host as host, testdb_port as port

# trio_mysql.connections.DEBUG = True
# trio_mysql._auth.DEBUG = True

import trustme
import tempfile
_ca = trustme.CA()
ca = tempfile.mktemp(".pem")
# ca = os.path.expanduser("~/ca.pem")
_ca.cert_pem.write_to_path(ca)

ssl = {'ca': ca, 'check_hostname': False}


async def test_sha256_no_password():
    async with trio_mysql.connect(user="nopass_sha256", host=host, port=port, ssl=None):
        pass


async def test_sha256_no_passowrd_ssl():
    async with trio_mysql.connect(user="nopass_sha256", host=host, port=port, ssl=ssl):
        pass


async def test_sha256_password():
    async with trio_mysql.connect(user="user_sha256", password="pass_sha256", host=host, port=port, ssl=None):
        pass


async def test_sha256_password_ssl():
    async with trio_mysql.connect(user="user_sha256", password="pass_sha256", host=host, port=port, ssl=ssl):
        pass


async def test_caching_sha2_no_password():
    async with trio_mysql.connect(user="nopass_caching_sha2", host=host, port=port, ssl=None):
        pass


async def test_caching_sha2_no_password():
    async with trio_mysql.connect(user="nopass_caching_sha2", host=host, port=port, ssl=ssl):
        pass


async def test_caching_sha2_password():
    async with trio_mysql.connect(user="user_caching_sha2", password="pass_caching_sha2", host=host, port=port, ssl=None):
        pass

    # Fast path of caching sha2
    async with trio_mysql.connect(user="user_caching_sha2", password="pass_caching_sha2", host=host, port=port, ssl=None) as con:
        await con.query("FLUSH PRIVILEGES")


async def test_caching_sha2_password_ssl():
    async with trio_mysql.connect(user="user_caching_sha2", password="pass_caching_sha2", host=host, port=port, ssl=ssl):
        pass

    # Fast path of caching sha2
    async with trio_mysql.connect(user="user_caching_sha2", password="pass_caching_sha2", host=host, port=port, ssl=None) as con:
        await con.query("FLUSH PRIVILEGES")
