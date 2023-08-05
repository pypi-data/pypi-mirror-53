from setuptools import setup, find_packages

with open("README.md", "r") as f1:
    long_description = f1.read()

setup(
    name='GSimPy',
    version='0.0.2',
    description='A Python Package for calculating similarity between groups',
    long_description=open('README.md', 'r').read(),
    long_description_content_type="text/plain",
    author='YifeiZhang',
    author_email='curlyar1995@163.com',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/curlyae1995/GSimPy',
    install_requires=[
        'numpy',
        'pyecharts',
        'matplotlib',
    ]

)
