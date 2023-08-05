import setuptools

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setuptools.setup(
    name='scuttlepy',
    version='0.1.0',
    description='SCUTTLE Python Library',
    license='GNU General Public License v3.0',
    packages=setuptools.find_packages(),
    author='Daniyal Ansari',
    author_email='daniyal.s.ansari+pypi@gmail.com',
    keywords=['scuttle'],
    url='https://github.com/ansarid/SCUTTLE',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
