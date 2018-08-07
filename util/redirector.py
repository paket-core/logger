'Link redirector.'
import urllib.parse
import util.countly

HTML_HEAD = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>PAKET Linker</title></head><body>'
HTML_FORM = '<form><input name=link placeholder=link><input name=source placeholder=source><input type=submit></form>'
HTML_TAIL = '</body></html>'


def application(env, start_response):
    'Handle request.'
    kwargs = urllib.parse.parse_qs(env['QUERY_STRING'])
    if 'target' in kwargs:
        target = kwargs['target'][0]
        util.countly.send_countly_event('redirect', 1, **kwargs)
        start_response('302 Found', [('Location', target)])
        return b''
    start_response('200 OK', [('Content-Type', 'text/html')])
    if not {'link', 'source'} - set(kwargs.keys()):
        query_string = urllib.parse.urlencode({'target': kwargs['link'][0], 'source': kwargs['source'][0]})
        return "{}<a href='/linker?{}'>https://c.paket.global/linker?{}</a>{}".format(
            HTML_HEAD, query_string, query_string, HTML_TAIL).encode()
    return "{}{}{}".format(HTML_HEAD, HTML_FORM, HTML_TAIL).encode()

# Sample uwsgi command:
# uwsgi --wsgi-file linker.py --socket 127.0.0.1:9090
# Sample nginx config:
# location ^~ /linker/ {
#     include uwsgi_params;
#     uwsgi_pass 127.0.0.1:9090;
# }
