"""
Adapted from https://github.com/moriyoshi/pyramid_dogpile_cache/blob/0.0.4/pyramid_dogpile_cache/__init__.py

Copyright (c) 2014 Moriyoshi Koizumi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""


def build_dogpile_region_settings(settings):
    region_settings_dict = {}
    prefix = 'dogpile_cache.'

    # pass 1: retrieve settings and put them into the dictionary
    for key, value in settings.items():
        if key.startswith(prefix):
            region_name, dot, param_name = key[len(prefix) :].partition('.')
            if not dot:
                if region_name == 'regions':
                    # dogpile_cache.regions = foo, bar ...
                    for region_name in value.split(','):
                        region_name = region_name.strip()
                        if region_name in ('regions', 'arguments'):
                            raise ValueError('region name %s is not allowed' % region_name)
                        if region_name and region_name not in region_settings_dict:
                            region_settings_dict[region_name] = {}
                    continue
                else:
                    # dogpile_cache.backend = ...
                    # dogpile_cache.expiration_time = ...
                    param_name = region_name
                    region_name = ''
                    if param_name == 'name':
                        raise ValueError(
                            'parameter %s is not allowed for the default cache settings' % key
                        )
            elif region_name == 'arguments':
                # dogpile_cache.arguments.host = localhost ...
                param_name = region_name + '.' + param_name
                region_name = ''

            region_settings = region_settings_dict.get(region_name)
            if not region_settings:
                region_settings = region_settings_dict[region_name] = {}
            region_settings[param_name] = value

    # pass 2: combine region-specific settings with defaults
    default_settings = region_settings_dict.get('', {})
    for region_name, region_settings in region_settings_dict.items():
        if region_name == '':
            # skip the default
            continue

        # merge the default into region-specific settings
        for key, value in default_settings.items():
            if key not in region_settings:
                region_settings[key] = value

    try:
        del region_settings_dict['']
    except KeyError:
        pass

    return default_settings, region_settings_dict
