import setuptools

with open("README.md", 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='cli42ndLock',
    version='0.0.2',
    scripts=['cli42ndlock'],
    author="Ansgar Schmidt",
    author_email='ansgar@symlink.de',
    maintainer="Symlink GmbH",
    maintainer_email="info@symlink.de",
    description='Client library and command line interface for 2ndLock',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/symlinkgmbh/client-python/',
    packages=['Secondlock'],
    py_modules=['Secondlock'],
    python_requires='>=3.0',
    install_requires=["click", "pysha3", "requests", "dnspython", "pycryptodome", "python-dateutil"],
    classifiers=[
                "Programming Language :: Python :: 3",
                "Development Status :: 4 - Beta",
                "License :: OSI Approved :: Apache Software License",
                "Environment :: Console",
                "Natural Language :: English",
                "Topic :: Communications"
    ]
)
