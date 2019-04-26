import toml


class Naming(object):

    @classmethod
    def camelize(cls, value, lower=False):
        return value

    @classmethod
    def humanize(cls, value):
        return value

    @classmethod
    def underscore(cls, value):
        return value

    @classmethod
    def unsuffix(cls, value):
        return value


def get_proj_meta():
    data = toml.load('./proj.toml')
    return data.get('meta')
