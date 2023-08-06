#
# Copyright (c) 2006-2019 Balabit
# All Rights Reserved.
#
"""
.. py:module:: safeguard.sessions.plugin.plugin_base
    :synopsis: Plugin base class.

The following decorators and the
:class:`PluginBase <safeguard.sessions.plugin.plugin_base.PluginBase>` class may be used in any Plugin SDK based plugin
to get some basic functionality.

"""
import os
from . import logging
from .plugin_configuration import PluginConfiguration
from .box_configuration import BoxConfiguration


class LazyProperty:
    def __init__(self, factory):
        self._factory = factory

    def __get__(self, instance, owner):
        return self.__set__(instance, self._factory(instance))

    def __set__(self, instance, value):
        instance.__dict__[self._name] = value
        return value

    __delete__ = None  # disable delete

    def __set_name__(self, owner, name):
        self._name = name


def lazy_property(factory):
    """
    The :meth:`@lazy_property <lazy_property>` decorator is used to mark attributes that should only be evaluated when
    accessed. This is useful when the calculation of the attribute is heavy, but not always necessary.

    **Usage**

    To use ``self.foobar`` as a lazy property, simply define it on the Plugin class, and decorate it with
    :meth:`@lazy_property <lazy_property>` decorator:

    .. code-block:: python

        from safeguard.sessions.plugin import AAPlugin
        from safeguard.sessions.plugin.plugin_base import lazy_property

        class MyPlugin(AAPlugin):
            @lazy_property
            def foobar(self):
                return calculate_answer()

            def do_authenticate(self):
                if need_foobar:
                    print(self.foobar)

    """
    return LazyProperty(factory)


class CookieProperty:
    def __init__(self, key, factory):
        self._key = key
        self._factory = factory

    def __get__(self, instance, owner):
        if self._key not in instance.cookie:
            instance.cookie[self._key] = self._factory(instance)
        return instance.cookie[self._key]

    def __set__(self, instance, value):
        instance.cookie[self._key] = value
        return value

    def __delete__(self, instance):
        del instance.cookie[self._key]


def cookie_property(factory):
    """
    The :meth:`@cookie_property <cookie_property>` decorator is used to mark attributes that should be passed in the
    cookie between invocations of the same plugin. Setting up such property is an easy way to store and retrieve data
    in ``self.cookie``. Similarly to :meth:`@lazy_property <lazy_property>` attributes, the evaulation of a
    :meth:`@cookie_property <cookie_property>` attribute is also delayed until usage.

    **Usage**

    To use ``self.foobar`` as a cookie property, simply define it on the Plugin class, and decorate it with
    :meth:`@cookie_property <cookie_property>` decorator:

    .. code-block:: python

        from safeguard.sessions.plugin import AAPlugin
        from safeguard.sessions.plugin.plugin_base import cookie_property

        class MyPlugin(AAPlugin):
            @cookie_property
            def foobar(self):
                return 42

            def do_authenticate(self):
                assert self.foobar == 42
                self.foobar = 0

            def do_authorize(self):
                assert self.foobar == 0

    The decorator :meth:`@cookie_property <cookie_property>` together with code in
    :class:`AAPlugin <safeguard.sessions.plugin.AAPlugin>` will ensure that ``foobar`` is stored and retrieved from
    the cookie passed to the plugin.

    The initial definition of foobar is 42 in this case, but it can be any function - this function is only called
    if foobar was not accessed before. To be more precise foobar is initialized with its factory function if it is
    being accessed and it is not present in ``self.cookie``.
    """
    return CookieProperty(factory.__name__, factory)


def named_cookie_property(key=None):
    """
    The :meth:`@named_cookie_property <named_cookie_property>` decorator is working similarly to the
    :meth:`@cookie_property <cookie_property>` decorator.
    The only difference is you can specify the key you want to save value in the ``self.cookie``
    It is important that you have to call the decorator with the desired key name, see usage.

    **Usage**

    To use ``self.my_custom_key`` as a cookie property, simply define it on the Plugin class, and decorate it with
    :meth:`@named_cookie_property(key=my_custom_key) <named_cookie_property>` decorator:

    .. code-block:: python

        from safeguard.sessions.plugin import AAPlugin
        from safeguard.sessions.plugin.plugin_base import named_cookie_property

        class MyPlugin(AAPlugin):
            @named_cookie_property(key=my_custom_key)
            def foobar(self):
                return 42

            def do_authenticate(self):
                assert self.cookie.my_custom_key == 42

    """
    return lambda factory: CookieProperty(key or factory.__name__, factory)


class SessionCookieProperty:
    def __init__(self, key, factory):
        self._key = key
        self._factory = factory

    def __get__(self, instance, owner):
        if self._key not in instance.session_cookie:
            instance.session_cookie[self._key] = self._factory(instance)
        return instance.session_cookie[self._key]

    def __set__(self, instance, value):
        instance.session_cookie[self._key] = value
        return value

    def __delete__(self, instance):
        del instance.session_cookie[self._key]


def session_cookie_property(factory):
    """
    The :meth:`@session_cookie_property <session_cookie_property>` decorator is used to mark attributes that should be
    passed in the session cookie between invocations of all plugins relevant to the session.
    Setting up such property is an easy way to store and retrieve data in ``self.session_cookie``.
    Similarly to :meth:`@lazy_property <lazy_property>` attributes, the evaulation of a
    :meth:`@session_cookie_property <session_cookie_property>` attribute is also delayed until usage.

    **Usage**

    To use ``self.foobar`` as a session cookie property, simply define it on the Plugin class, and decorate it with
    :meth:`@session_cookie_property <session_cookie_property>` decorator:

    .. code-block:: python

        from safeguard.sessions.plugin import AAPlugin
        from safeguard.sessions.plugin.plugin_base import session_cookie_property

        class MyPlugin(AAPlugin):
            @session_cookie_property
            def foobar(self):
                return 42

            def do_authenticate(self):
                assert self.foobar == 42
                self.foobar = 0

            def do_authorize(self):
                assert self.foobar == 0

    The decorator :meth:`@session_cookie_property <session_cookie_property>` together with code in
    :class:`AAPlugin <safeguard.sessions.plugin.AAPlugin>` will ensure that ``foobar`` is stored and retrieved from
    the session cookie passed to the plugin.

    The initial definition of foobar is 42 in this case, but it can be any function - this function is only called
    if foobar was not accessed before. To be more precise foobar is initialized with its factory function if it is
    being accessed and it is not present in ``self.session_cookie``.
    """
    return SessionCookieProperty(factory.__name__, factory)


class PluginBase:
    """
    The :class:`PluginBase` implements:

    * parsing the textual plugin configuration
    * setting the log level
    * setting HTTPS proxy environment variables https_proxy and HTTPS_PROXY
    * basic cookie handling methods

    """
    def __init__(self, configuration, defaults=None, logger=None):
        self.cookie = None
        self.connection = None
        self.session_cookie = None
        self.proxy_settings = None
        self.logger = logger or logging.get_logger(__name__)
        self.plugin_configuration = PluginConfiguration(configuration, defaults=defaults)
        self.box_configuration = BoxConfiguration.open()
        self.set_https_proxy()
        logging.configure(self.plugin_configuration)

    @property
    def https_proxy_server(self):
        return self.proxy_settings.get('server')

    @property
    def https_proxy_port(self):
        return self.proxy_settings.get('port')

    @property
    def https_proxy_username(self):
        return self.proxy_settings.get('username')

    @property
    def https_proxy_password(self):
        return self.proxy_settings.get('password')

    def set_https_proxy(self):
        self.proxy_settings = self._override_proxy_from_config(
                self._get_proxy_settings_from_box_config())
        https_proxy = self._calculate_http_proxy(self.proxy_settings)

        if https_proxy:
            self.logger.info('Setting proxy to: {}'.format(https_proxy))
            os.environ['https_proxy'] = os.environ['HTTPS_PROXY'] = https_proxy
            self.logger.debug('Proxy set to {}'.format(os.environ['HTTPS_PROXY']))
        else:
            self.unset_https_proxy()

    def unset_https_proxy(self):
        os.environ.pop('https_proxy', None)
        os.environ.pop('HTTPS_PROXY', None)

    def _get_proxy_settings_from_box_config(self):
        proxy_settings = self.box_configuration.get_http_proxy()
        return dict(server=proxy_settings.server,
                    port=proxy_settings.port,
                    username=proxy_settings.username,
                    password=proxy_settings.password)

    def _override_proxy_from_config(self, proxy_from_box_config):
        if self.plugin_configuration.get('https_proxy', 'server'):
            return dict(server=self.plugin_configuration.get('https_proxy', 'server'),
                        port=self.plugin_configuration.getint('https_proxy', 'port', default=3128),
                        username=self.plugin_configuration.get('https_proxy', 'username'),
                        password=self.plugin_configuration.get('https_proxy', 'password'))
        elif self.plugin_configuration.get('https_proxy', 'server') == '':
            return dict()
        else:
            return proxy_from_box_config

    @staticmethod
    def _calculate_http_proxy(proxy_settings):
        if proxy_settings.get('server') and proxy_settings.get('port'):
            if proxy_settings.get('username') and proxy_settings.get('password'):
                auth_string = '{username}:{password}@'.format(username=proxy_settings['username'],
                                                              password=proxy_settings['password'])
            else:
                auth_string = ''
            return "https://{auth}{server}:{port}".format(auth=auth_string,
                                                          server=proxy_settings['server'],
                                                          port=proxy_settings['port'])
        else:
            return None

    def _add_cookies(self, result):
        if not isinstance(result, dict):
            return result

        if "cookie" in result:
            self.cookie.update(result["cookie"])
        result["cookie"] = self.cookie

        if "session_cookie" in result:
            self.session_cookie.update(result["session_cookie"])
        result["session_cookie"] = self.session_cookie

        return result

    @cookie_property
    def __plugin_sdk_private(self):
        return {}

    def _get_private(self, key, default=None):
        return self.__plugin_sdk_private.get(key, default)

    def _set_private(self, key, value):
        self.__plugin_sdk_private[key] = value

    def _pop_private(self, key):
        value = self.__plugin_sdk_private[key]
        del self.__plugin_sdk_private[key]
        return value
