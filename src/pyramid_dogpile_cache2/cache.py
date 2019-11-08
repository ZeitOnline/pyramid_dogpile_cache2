import dogpile.util.compat
import hashlib
import inspect


def key_generator(ns, fn, to_str=dogpile.util.compat.text_type):
    """Extension of dogpile.util.function_key_generator that handles
    non-ascii function arguments, and supports not just plain functions, but
    methods as well.
    """
    if dogpile.util.compat.py2k:
        args = inspect.getargspec(fn)
    else:
        args = inspect.getfullargspec(fn)
    has_self = args[0] and args[0][0] in ('self', 'cls')

    def generate_key(*args, **kw):
        if kw:
            raise ValueError(
                "dogpile.cache's default key creation "
                "function does not accept keyword arguments.")
        if has_self and args:
            cls = args[0].__class__
            args = args[1:]
        else:
            cls = None

        if cls:
            namespace = u'.'.join([cls.__module__, cls.__name__, fn.__name__])
        else:
            namespace = u'.'.join([fn.__module__, fn.__name__])
        if ns is not None:
            namespace = u'%s|%s' % (namespace, ns)

        return namespace + u'|' + u' '.join(map(to_str, args))
    return generate_key


def sha1_mangle_key(key):
    """Extension of dogpile.util.sha1_mangle_key that handles unicode.

    The upstream version was fixed in dogpile.cache-0.9.0, so this is only
    left here for bw-compat.
    """
    return hashlib.sha1(key.encode('utf-8')).hexdigest()
