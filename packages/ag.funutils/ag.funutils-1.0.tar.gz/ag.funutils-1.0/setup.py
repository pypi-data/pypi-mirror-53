import setuptools

with open('README.md', 'r') as readme:
    long_description = readme.read()

setuptools.setup(
    name='ag.funutils',
    version='1.0',
    author='Austin Garrard',
    author_email='austin.w.garrard@gmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/austin-garrard/ag.funutils',
    packages=['ag.funutils']
)
