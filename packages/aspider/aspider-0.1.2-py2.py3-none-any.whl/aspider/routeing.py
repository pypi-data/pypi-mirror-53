'''
routing logic and some tools
'''
from functools import wraps
import asyncio
import re
import inspect
from urllib.parse import urlparse, urljoin
from .util import logger
# from bottle import route
# key-value map for url pattern -> process func mapping
default_router = None


def check_signature(func, arg_name):
    args_list = inspect.getfullargspec(func)[0]
    if arg_name in args_list:
        return True
    else:
        return False


def get_router():
    global default_router

    if default_router is None:
        default_router = Router()
    return default_router


class Router:
    '''
    collections of routes and help match to Route object

    Args:
        root_path -> str : root path to start
    '''

    def __init__(self):
        self.routes = {}

    def stop(self):
        self.quit_event.set()

    def resume(self, loop):
        self.quit_event = asyncio.Event(loop=loop)

    def is_running(self):
        return not self.quit_event.is_set()

    def add_root_path(self, root_path):
        url_parts = urlparse(root_path)
        if url_parts.path:
            pos = root_path.index(url_parts.path)
            root_path = root_path[:pos]
        self.root_path = root_path

    def _replace_tokens(self, rule):
        '''
        turn /hello/<name> to r'/hello/?P<name>[^/]+'
        '''
        repl = '[^/]+'
        pattern = ''
        for prefix, key, config in self._iter_tokens(rule):
            #repl = r'(?P\g<0>[^/]+)'
            pattern += prefix
            if key:
                pattern += f'(?P<{key}>{config or repl})'

        return pattern

    def _iter_tokens(self, rule):
        '''
        return iter of (prefix, key, config) item
        '''
        offset, prefix = 0, ''
        pattern = re.compile(r'<(.+)>')
        key = None
        conf = None
        for match in pattern.finditer(rule):
            prefix = rule[offset:match.start()]
            offset = match.end()
            g = match.groups()
            if len(g) > 0:
                key = g[0]
                if ':' in key:
                    key, conf = key.split(':', 1)
            yield prefix, key, conf
        if offset < len(rule):
            yield rule[offset:], None, None

    def match(self, url):
        '''
        find mated pattern return key, value pairs
        match /hello/jun to {'name', 'jun'}

        Returns:
            tuple -> (route, args_dict)
        '''
        path = self.get_url_path(url)
        route = None
        args_dict = {}
        for pattern in self.routes:
            match = re.match(pattern, path)
            if match:
                route = self.routes[pattern]
                args_dict = match.groupdict()
                args_dict.update(path=path)
                break

        return route, args_dict

    def get_url_path(self, url):
        '''
        Args:
            url -> str: full url

        Return:
            path -> str: path part of url
        '''
        path = None
        if self.root_path in url:
            path = url[len(self.root_path):]
        return path

    def get_full_url(self, path):
        root_path = self.root_path
        full_url = urljoin(root_path, path)
        return full_url

    def verify_url(self, url, out_url):
        '''
        check if link is allowed in router

        Args:
            url: str -> url to verify
            out_url: str -> page include url
        '''
        out_path = self.get_url_path(out_url)
        out_match = self.find_route(out_path)
        if out_match:
            out_route, _ = out_match
            if out_route.no_parse_links:
                logger.debug(
                    f'out path {out_url} disable parse link:{url}')
                return False
        path = self.get_url_path(url)
        match = self.find_route(path)
        # check if any verify_func defined
        if match:
            route, args_dict = match
            if route.verify(path, **args_dict):
                logger.debug(f'verify_url:{path} with route:{route}')
                return True
        logger.debug(f'not verify_url:{path}')
        return False

    def find_route(self, path):
        for pattern in self.routes:
            match = re.match(pattern, path)
            if match:
                route = self.routes[pattern]
                args_dict = match.groupdict()
                return route, args_dict
        return None

    def route(self, rule, verify_func=None, no_parse_links=False):
        def decorator(callback):
            # add rule to router
            replaced = self._replace_tokens(rule)
            route = Route(self, rule, callback,
                          verify_func=verify_func, no_parse_links=no_parse_links)
            self.routes[replaced] = route
            return callback
        return decorator


class Route:
    '''
    wrapper for callback and url verify func
    '''

    def __init__(self, router, rule, callback, verify_func=None, no_parse_links=False):
        self.router = router
        self.rule = rule
        self.callback = callback
        self.verify_func = verify_func
        self.no_parse_links = no_parse_links

    def __repr__(self):
        s = f'<Route {self.rule}>'
        return s

    def call(self, text, **kwargs):
        callback = self.callback
        has_path = check_signature(callback, 'path')
        if not has_path:
            kwargs.pop('path')
        return callback(text, **kwargs)

    def verify(self, path, **kwargs):
        '''
        Args:
            path -> url remove root part
        '''
        verify_func = self.verify_func
        if verify_func:
            has_path = check_signature(verify_func, 'path')
            if has_path:
                return verify_func(path, **kwargs)
            else:
                return verify_func(**kwargs)
        return True
