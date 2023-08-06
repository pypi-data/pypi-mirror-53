from django.db import connection


def escape_sql_identifier(identifier):
    if connection.vendor == 'mysql':
        return '`{}`'.format(identifier)
    else:
        return '"{}"'.format(identifier)
