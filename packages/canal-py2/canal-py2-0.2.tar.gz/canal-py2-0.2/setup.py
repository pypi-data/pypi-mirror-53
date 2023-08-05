from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='canal-py2',
    version='0.2',
    packages=['canal', 'canal.protocol'],
    author='pxguan',
    author_email='guanpeixiang@foxmail.com',
    license='MIT',
    # long_description=open('README.md', 'r').read(),
    url='https://github.com/Guanpx/canal-python',
    # long_description_content_type="text/markdown"
)
