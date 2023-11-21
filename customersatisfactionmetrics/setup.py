from setuptools import find_packages, setup

setup(
    name='customersatisfactionmetrics',
    version='0.1',
    author='Bram Mittendorff',  # Your name or your organization's name
    author_email='bram@pescheck.io',  # Your email or your organization's email
    description='A short description of your package',  # A brief description of your package
    long_description=open('README.md').read(),  # A long description from README.md
    long_description_content_type='text/markdown',  # Content type of the long description
    url='http://github.com/pescheckit/customersatisfactionmetrics',  # URL to your package's repository
    packages=find_packages(),  # Automatically find packages in your project
    include_package_data=True,  # Include non-code files specified in MANIFEST.in
    install_requires=[
        'Django>=3.0',  # Replace or add dependencies as needed
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',  # Choose the appropriate status
        # 'Intended Audience :: Developers', 
        # 'License :: OSI Approved :: MIT License', 
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.6',
        # 'Programming Language :: Python :: 3.7',
        # 'Programming Language :: Python :: 3.8',
        # 'Programming Language :: Python :: 3.9',
        # 'Programming Language :: Python :: 3.10',
        # 'Framework :: Django',
        # 'Framework :: Django :: 3.0',
        # ... Add other classifiers as needed
    ],
    # Optional settings
    # keywords='keyword1 keyword2 keyword3',
    # license='MIT',
    # python_requires='>=3.6',
)
