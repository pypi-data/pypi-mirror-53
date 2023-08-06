import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='generic-struct',
    version='1.0.2',
    author='Ori Pardo',
    author_email='pardooori@gmail.com',
    description='A simple package to simplify conversion between binary data and python objects',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers'
    ],
    python_requires='>=3.6',
)
