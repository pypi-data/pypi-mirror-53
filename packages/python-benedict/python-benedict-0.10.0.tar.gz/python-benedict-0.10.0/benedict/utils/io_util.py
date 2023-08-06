# -*- coding: utf-8 -*-

from six import StringIO

import base64
import csv
import errno
import json
import os
import requests
import xmltodict
import toml
import yaml

try:
    # python 3
    # from urllib.parse import parse_qs as url_parse
    # from urllib.parse import quote_plus as url_quote
    # from urllib.parse import unquote_plus as url_unquote
    # from urllib.parse import parse_qs, urlparse
    # from urllib.parse import parse_qs
    from urllib.parse import urlencode
except ImportError:
    # python 2
    # from urllib.parse import parse_qs, urlparse
    # from urllib import quote_plus as url_quote
    # from urllib import unquote_plus as url_unquote
    # from urlparse import parse_qs, urlparse
    from urllib import urlencode


def decode_base64(s, **kwargs):
    decode_func = kwargs.pop('through', decode_json)
    b = base64.b64decode(s)
    s = b.decode('utf-8')
    return decode_func(s, **kwargs)


def decode_csv(s, **kwargs):
    kwargs.setdefault('delimiter', ';')
    kwargs.setdefault('quoting', csv.QUOTE_ALL)
    f = StringIO(s)
    data = csv.DictReader(f, **kwargs)
    return data


def decode_json(s, **kwargs):
    data = json.loads(s, **kwargs)
    return data


def decode_query_string(s, **kwargs):
    d = {}
    # if s.startswith('https://') or s.startswith('http://'):
    #     # parsed_url = urlparse(s)
    #     # print(parsed_url.query)
    #     return {}
    #     query_string = parsed_url.query
    # else:
    #     query_string = s
    # d = parse_qs(query_string)
    # # flat dict single dict values
    # keys = d.keys()
    # for key in keys:
    #     value = d.get(key);
    #     if isinstance(value, list) and len(value) == 1:
    #         value = value[0]
    #         d[key] = value
    # return d
    # # d = {}
    # # pairs = s.split('&')
    # # for pair in pairs:
    # #     kv = pair.split('=')
    # #     key = kv[0]
    # #     val = url_unquote(kv[1])
    # #     d[key] = val
    return d


def decode_xml(s, **kwargs):
    kwargs.setdefault('dict_constructor', dict)
    data = xmltodict.parse(s, **kwargs)
    return data


def decode_toml(s, **kwargs):
    data = toml.loads(s, **kwargs)
    return data


def decode_yaml(s, **kwargs):
    kwargs.setdefault('Loader', yaml.Loader)
    data = yaml.load(s, **kwargs)
    return data


def encode_base64(d, **kwargs):
    encode_func = kwargs.pop('through', encode_json)
    data = base64.b64encode(
        encode_func(d, **kwargs).encode('utf-8')).decode('utf-8')
    return data


# def encode_csv(d, **kwargs):
#     kwargs.setdefault('delimiter', ';')
#     kwargs.setdefault('quoting', csv.QUOTE_ALL)
#     return data


def encode_json(d, **kwargs):
    data = json.dumps(d, **kwargs)
    return data


def encode_query_string(d, **kwargs):
    data = urlencode(d, **kwargs)
    return data
    # pairs = []
    # for key, val in d.items():
    #     pair = '='.join(slugify(key), url_quote(key))
    #     pairs.append(pair)
    # s = '&'.join(pairs)
    # return s


def encode_toml(d, **kwargs):
    data = toml.dumps(d, **kwargs)
    return data


def encode_xml(d, **kwargs):
    data = xmltodict.unparse(d, **kwargs)
    return data


def encode_yaml(d, **kwargs):
    data = yaml.dump(d, **kwargs)
    return data


def read_content(s):
    # s -> filepath or url or data
    if s.startswith('http://') or s.startswith('https://'):
        content = read_url(s)
    elif os.path.isfile(s):
        content = read_file(s)
    else:
        content = s
    return content


def read_file(filepath):
    handler = open(filepath, 'r')
    content = handler.read()
    handler.close()
    return content


def read_url(url, *args, **kwargs):
    response = requests.get(url, *args, **kwargs)
    content = response.text
    return content


def write_file(filepath, content):
    # https://stackoverflow.com/questions/12517451/automatically-creating-directories-with-file-output
    if not os.path.exists(os.path.dirname(filepath)):
        try:
            os.makedirs(os.path.dirname(filepath))
        except OSError as e:
            # Guard against race condition
            if e.errno != errno.EEXIST:
                raise e
    handler = open(filepath, 'w+')
    handler.write(content)
    handler.close()
    return True
