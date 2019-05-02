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
