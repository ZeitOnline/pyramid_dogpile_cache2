"""
Copied from https://github.com/bbangert/beaker/blob/1.13.0/beaker/util.py

Copyright (c) 2006, 2007 Ben Bangert, Mike Bayer, Philip Jenvey
                         and contributors.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.
3. The name of the author or contributors may not be used to endorse or
   promote products derived from this software without specific prior
   written permission.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
SUCH DAMAGE.
"""

from datetime import datetime, timedelta
import re


def convert(behaviors):
    rules = [
        ('cas', (bool, int), 'cas must be a boolean or an integer'),
        ('no_block', (bool, int), 'no_block must be a boolean or an integer'),
        ('receive_timeout', (int,), 'receive_timeout must be an integer'),
        ('send_timeout', (int,), 'send_timeout must be an integer'),
        (
            'ketama_hash',
            (str,),
            'ketama_hash must be a string designating a valid hashing strategy option',
        ),
        ('_poll_timeout', (int,), '_poll_timeout must be an integer'),
        ('auto_eject', (bool, int), 'auto_eject must be an integer'),
        ('retry_timeout', (int,), 'retry_timeout must be an integer'),
        ('_sort_hosts', (bool, int), '_sort_hosts must be an integer'),
        ('_io_msg_watermark', (int,), '_io_msg_watermark must be an integer'),
        ('ketama', (bool, int), 'ketama must be a boolean or an integer'),
        ('ketama_weighted', (bool, int), 'ketama_weighted must be a boolean or an integer'),
        ('_io_key_prefetch', (int, bool), '_io_key_prefetch must be a boolean or an integer'),
        (
            '_hash_with_prefix_key',
            (bool, int),
            '_hash_with_prefix_key must be a boolean or an integer',
        ),
        ('tcp_nodelay', (bool, int), 'tcp_nodelay must be a boolean or an integer'),
        ('failure_limit', (int,), 'failure_limit must be an integer'),
        ('buffer_requests', (bool, int), 'buffer_requests must be a boolean or an integer'),
        ('_socket_send_size', (int,), '_socket_send_size must be an integer'),
        ('num_replicas', (int,), 'num_replicas must be an integer'),
        ('remove_failed', (int,), 'remove_failed must be an integer'),
        ('_noreply', (bool, int), '_noreply must be a boolean or an integer'),
        ('_io_bytes_watermark', (int,), '_io_bytes_watermark must be an integer'),
        ('_socket_recv_size', (int,), '_socket_recv_size must be an integer'),
        (
            'distribution',
            (str,),
            'distribution must be a string designating a valid distribution option',
        ),
        ('connect_timeout', (int,), 'connect_timeout must be an integer'),
        ('hash', (str,), 'hash must be a string designating a valid hashing option'),
        ('verify_keys', (bool, int), 'verify_keys must be a boolean or an integer'),
        ('dead_timeout', (int,), 'dead_timeout must be an integer'),
    ]

    return verify_rules(behaviors, rules)


def verify_rules(params, ruleset):
    for key, types, message in ruleset:
        if key in params:
            params[key] = verify_options(params[key], types, message)
    return params


def verify_options(opt, types, error):
    if not isinstance(opt, types):
        if not isinstance(types, tuple):
            types = (types,)
        coerced = False
        for typ in types:
            try:
                if typ in (list, tuple):
                    opt = [x.strip() for x in opt.split(',')]
                else:
                    if typ is bool:
                        typ = asbool
                    elif typ is int:
                        typ = asint
                    elif typ in (timedelta, datetime):
                        if not isinstance(opt, typ):
                            raise Exception('%s requires a timedelta type', typ)
                    opt = typ(opt)
                coerced = True
            except Exception:
                pass
            if coerced:
                break
        if not coerced:
            raise Exception(error)
    elif isinstance(opt, str) and not opt.strip():
        raise Exception('Empty strings are invalid for: %s' % error)
    return opt


def asbool(obj):
    if isinstance(obj, str):
        obj = obj.strip().lower()
        if obj in ['true', 'yes', 'on', 'y', 't', '1']:
            return True
        elif obj in ['false', 'no', 'off', 'n', 'f', '0']:
            return False
        else:
            raise ValueError('String is not true/false: %r' % obj)
    return bool(obj)


def asint(obj):
    if isinstance(obj, int):
        return obj
    elif isinstance(obj, str) and re.match(r'^\d+$', obj):
        return int(obj)
    else:
        raise Exception('This is not a proper int')
