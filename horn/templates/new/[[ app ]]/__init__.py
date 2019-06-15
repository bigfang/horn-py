from .run import create_app


__version__ = '0.1.0'

app = create_app()


__all__ = ['__version__', 'app']
