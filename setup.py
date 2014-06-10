from setuptools import setup

setup(
    name='pytsdb',
    version='0.2.1',
    author='Nikhil Benesch',
    author_email='nikhil.benesch@gmail.com',
    py_modules=['pytsdb'],
    url='https://github.com/whoopinc/pytsdb',
    description='Featureless Python adapter for OpenTSDB',
    install_requires=[
        "requests >= 2.2.1",
    ],
)
