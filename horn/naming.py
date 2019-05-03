class Naming(object):

    @classmethod
    def camelize(cls, value, lower=False):
        return value.capitalize()

    @classmethod
    def humanize(cls, value):
        return value.lower()

    @classmethod
    def underscore(cls, value):
        return value.lower()

    @classmethod
    def unsuffix(cls, value):
        return value.upper()

    @classmethod
    def singular(cls, value):
        rv = value
        if value.endswith('ies'):
            rv = f'{value[:-3]}y'
        elif value.endswith('s'):
            rv = value[:-1]
        return rv
