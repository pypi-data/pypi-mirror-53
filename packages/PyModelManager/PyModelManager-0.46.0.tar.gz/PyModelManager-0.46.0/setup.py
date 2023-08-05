from setuptools import setup
import io, os

version = "0.46.0"

here = os.path.abspath(os.path.dirname(__file__))


def get_long_description():
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        return '\n' + f.read()


setup(
    name='PyModelManager',
    version=version,
    packages=['modelmanager'],
    url='',
    license='',
    author='Alexander Litvinov',
    author_email='alektron@yandex.ru',
    description='ModelManager API',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    python_requires='>=3.6'
)
