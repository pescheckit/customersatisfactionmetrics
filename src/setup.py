"""
Setup configuration for the customersatisfactionmetrics package.

This script is used to handle the packaging and distribution of the
'customersatisfactionmetrics' package, including metadata, dependencies,
and other necessary package information.
"""

from pathlib import Path

from setuptools import find_packages, setup

# Resolve the README relative to this file rather than the working directory.
# Tools that build the package from somewhere else (editable installs, GitHub's
# dependency submission) otherwise fail here before they can read the metadata.
README = Path(__file__).resolve().parent / 'README.md'
long_description = README.read_text(encoding='utf-8') if README.is_file() else ''

setup(
    name='customersatisfactionmetrics',
    version="1.1.1",
    author='Bram Mittendorff',
    author_email='bram@pescheck.io',
    description='Django app for in-product surveys: CSAT, NPS and CES with touchpoints and impression tracking',
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
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
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
