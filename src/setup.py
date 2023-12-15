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
    version="1.0.2",
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
        "Development Status :: 5 - Production/Stable",
        "Natural Language :: English",
        "Topic :: Utilities",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Framework :: Django",
    ],
    keywords=[
        'django',
        'survey',
        'customer satisfaction',
        'feedback',
        'CSAT',
        'NPS',
        'CES',
        'survey management',
        'user responses',
        'analytics',
        'data collection',
        'web surveys',
        'survey application',
        'docker',
        'docker compose',
        'web app',
        'user experience',
        'user feedback',
        'questionnaire',
        'user engagement',
        'metadata tracking',
        'response analysis',
        'Django application',
    ],
    license='MIT',
)
