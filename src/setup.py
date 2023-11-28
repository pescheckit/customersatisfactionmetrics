"""
Setup configuration for the customersatisfactionmetrics package.

This script is used to handle the packaging and distribution of the
'customersatisfactionmetrics' package, including metadata, dependencies,
and other necessary package information.
"""

from setuptools import find_packages, setup

# Using 'with' statement for safe file handling
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='customersatisfactionmetrics',
    version="0.0.3",
    author='Bram Mittendorff',
    author_email='bram@pescheck.io',
    description='A short description of your package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://github.com/pescheckit/customersatisfactionmetrics',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=3.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Other classifiers...
    ],
    # Optional settings
    # keywords='...',
    # license='MIT',
    # python_requires='>=3.6',
)
