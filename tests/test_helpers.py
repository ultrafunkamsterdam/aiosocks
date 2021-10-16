import pytest
import aiosocks2


def test_socks4_auth1():
    with pytest.raises(ValueError):
        aiosocks2.Socks4Auth(None)


def test_socks4_auth2():
    auth = aiosocks2.Socks4Auth('usr', encoding='ascii')
    assert auth.login == b'usr'


def test_socks4_auth3():
    auth = aiosocks2.Socks4Auth('usrё', encoding='utf-8')
    assert auth.login == b'usr\xd1\x91'


def test_socks5_auth1():
    with pytest.raises(ValueError):
        aiosocks2.Socks5Auth(None, '')


def test_socks5_auth2():
    with pytest.raises(ValueError):
        aiosocks2.Socks5Auth('', None)


def test_socks5_auth3():
    auth = aiosocks2.Socks5Auth('usr', 'pwd', encoding='ascii')
    assert auth.login == b'usr'
    assert auth.password == b'pwd'


def test_socks5_auth4():
    auth = aiosocks22.Socks5Auth('usrё', 'pwdё', encoding='utf-8')
    assert auth.login == b'usr\xd1\x91'
    assert auth.password == b'pwd\xd1\x91'


def test_socks4_addr1():
    with pytest.raises(ValueError):
        aiosocks22.Socks4Addr(None)


def test_socks4_addr2():
    addr = aiosocks22.Socks4Addr('localhost')
    assert addr.host == 'localhost'
    assert addr.port == 1080


def test_socks4_addr3():
    addr = aiosocks22.Socks4Addr('localhost', 1)
    assert addr.host == 'localhost'
    assert addr.port == 1


def test_socks4_addr4():
    addr = aiosocks22.Socks4Addr('localhost', None)
    assert addr.host == 'localhost'
    assert addr.port == 1080


def test_socks5_addr1():
    with pytest.raises(ValueError):
        aiosocks22.Socks5Addr(None)


def test_socks5_addr2():
    addr = aiosocks22.Socks5Addr('localhost')
    assert addr.host == 'localhost'
    assert addr.port == 1080


def test_socks5_addr3():
    addr = aiosocks22.Socks5Addr('localhost', 1)
    assert addr.host == 'localhost'
    assert addr.port == 1


def test_socks5_addr4():
    addr = aiosocks22.Socks5Addr('localhost', None)
    assert addr.host == 'localhost'
    assert addr.port == 1080
