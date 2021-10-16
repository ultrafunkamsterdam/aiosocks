SOCKS proxy client for asyncio and aiohttp
==========================================
.. image:: https://travis-ci.org/ultrafunkamsterdam/aiosocks2.svg?branch=master
  :target: https://travis-ci.org/ultrafunkamsterdam/aiosocks2
  :align: right

.. image:: https://coveralls.io/repos/github/ultrafunkamsterdam/aiosocks2/badge.svg?branch=master
  :target: https://coveralls.io/github/ultrafunkamsterdam/aiosocks2?branch=master
  :align: right

.. image:: https://badge.fury.io/py/aiosocks2.svg
  :target: https://badge.fury.io/py/aiosocks2


Dependencies
------------
python 3.5+
aiohttp 2.3.2+

Features
--------
- Fixed original library to use in 2021 onwards
- SOCKS4, SOCKS4a and SOCKS5 version
- ProxyConnector for aiohttp
- SOCKS "CONNECT" command

TODO
----
- UDP associate
- TCP port binding

Installation
------------
You can install it using Pip:

.. code-block::

  pip install aiosocks2

If you want the latest development version, you can install it from source:

.. code-block::

  git clone git@github.com:ultrafunkamsterdam/aiosocks2.git
  cd aiosocks2
  python setup.py install

Usage
-----
direct usage
^^^^^^^^^^^^

.. code-block:: python

  import asyncio
  import aiosocks2


  async def connect():
    socks5_addr = aiosocks2.Socks5Addr('127.0.0.1', 1080)
    socks4_addr = aiosocks2.Socks4Addr('127.0.0.1', 1080)
    
    socks5_auth = aiosocks2.Socks5Auth('login', 'pwd')
    socks4_auth = aiosocks2.Socks4Auth('ident')
  
    dst = ('github.com', 80)
    
    # socks5 connect
    transport, protocol = await aiosocks2.create_connection(
        lambda: Protocol, proxy=socks5_addr, proxy_auth=socks5_auth, dst=dst)
    
    # socks4 connect
    transport, protocol = await aiosocks2.create_connection(
        lambda: Protocol, proxy=socks4_addr, proxy_auth=socks4_auth, dst=dst)
        
    # socks4 without auth and local domain name resolving
    transport, protocol = await aiosocks2.create_connection(
        lambda: Protocol, proxy=socks4_addr, proxy_auth=None, dst=dst, remote_resolve=False)

    # use socks protocol
    transport, protocol = await aiosocks2.create_connection(
        None, proxy=socks4_addr, proxy_auth=None, dst=dst)
  
  if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(connect())
    loop.close()


**A wrapper for create_connection() returning a (reader, writer) pair**

.. code-block:: python

    # StreamReader, StreamWriter
    reader, writer = await aiosocks2.open_connection(
        proxy=socks5_addr, proxy_auth=socks5_auth, dst=dst, remote_resolve=True)

    data = await reader.read(10)
    writer.write('data')

error handling
^^^^^^^^^^^^^^

`SocksError` is a base class for:
    - `NoAcceptableAuthMethods`
    - `LoginAuthenticationFailed`
    - `InvalidServerVersion`
    - `InvalidServerReply`

.. code-block:: python

    try:
      transport, protocol = await aiosocks2.create_connection(
          lambda: Protocol, proxy=socks5_addr, proxy_auth=socks5_auth, dst=dst)
    except aiosocks2.SocksConnectionError:
      # connection error
    except aiosocks2.LoginAuthenticationFailed:
      # auth failed
    except aiosocks2.NoAcceptableAuthMethods:
      # All offered SOCKS5 authentication methods were rejected
    except (aiosocks2.InvalidServerVersion, aiosocks2.InvalidServerReply):
      # something wrong
    except aiosocks2.SocksError:
      # something other

or

.. code-block:: python

    try:
      transport, protocol = await aiosocks2.create_connection(
          lambda: Protocol, proxy=socks5_addr, proxy_auth=socks5_auth, dst=dst)
    except aiosocks2.SocksConnectionError:
        # connection error
    except aiosocks2.SocksError:
        # socks error

aiohttp usage
^^^^^^^^^^^^^

.. code-block:: python

  import asyncio
  import aiohttp
  import aiosocks2
  from aiosocks2.connector import ProxyConnector, ProxyClientRequest


  async def load_github_main():
    auth5 = aiosocks2.Socks5Auth('proxyuser1', password='pwd')
    auth4 = aiosocks2.Socks4Auth('proxyuser1')
    ba = aiohttp.BasicAuth('login')

    # remote resolve
    conn = ProxyConnector(remote_resolve=True)

    # or locale resolve
    conn = ProxyConnector(remote_resolve=False)

    try:
      with aiohttp.ClientSession(connector=conn, request_class=ProxyClientRequest) as session:
        # socks5 proxy
        async with session.get('http://github.com/', proxy='socks5://127.0.0.1:1080',
                               proxy_auth=auth5) as resp:
          if resp.status == 200:
            print(await resp.text())

        # socks4 proxy
        async with session.get('http://github.com/', proxy='socks4://127.0.0.1:1081',
                               proxy_auth=auth4) as resp:
          if resp.status == 200:
            print(await resp.text())

        # http proxy
        async with session.get('http://github.com/', proxy='http://127.0.0.1:8080',
                               proxy_auth=ba) as resp:
          if resp.status == 200:
            print(await resp.text())
    except aiohttp.ClientProxyConnectionError:
      # connection problem
    except aiohttp.ClientConnectorError:
      # ssl error, certificate error, etc
    except aiosocks2.SocksError:
      # communication problem


  if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(load_github_main())
    loop.close()
