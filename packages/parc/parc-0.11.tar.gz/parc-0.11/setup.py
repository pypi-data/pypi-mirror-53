import setuptools



#with open("requirements.txt", "r") as fh:
#    requirements = fh.read()

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='parc',
    version='0.11',
    packages=['parc',],
    license='MIT',
    author_email = 'shobana.venkat88@gmail.com',
    url = 'https://github.com/ShobiStassen/PARC',
    setup_requires = ['pybind11'],
    install_requires=['numpy','scipy','pandas','hnswlib','python-igraph','leidenalg'],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
