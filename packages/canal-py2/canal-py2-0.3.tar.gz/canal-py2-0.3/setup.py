import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='canal-py2',
    version='0.3',
    packages=['canal', 'canal.protocol'],
    author='pxguan',
    author_email='guanpeixiang@foxmail.com',
    license='MIT',
    description="test",
    url='https://github.com/Guanpx/canal-python',
)
