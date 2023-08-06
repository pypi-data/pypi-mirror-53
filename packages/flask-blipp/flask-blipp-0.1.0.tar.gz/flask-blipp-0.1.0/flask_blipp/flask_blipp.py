import sys

from .basic_formatter import basic_formatter


def flask_blipp(app, stdout=sys.stdout, formatter=None, ignored_http_methods=None):
    """
    Prints out the routes for a flask app on start up

    app - a flask app
    stdout - where to print the routes to
    """
    if not ignored_http_methods:
        ignored_http_methods = ["OPTIONS", "HEAD"]
    ignored_methods = set(ignored_http_methods)

    if not formatter:
        formatter = basic_formatter

    rules = [
        (rule, filter_methods(rule.methods, ignored_methods))
        for rule in app.url_map.iter_rules()
    ]

    stdout.write(formatter(rules))


def filter_methods(methods, ignored_methods):
    return [method for method in methods if method not in ignored_methods]
