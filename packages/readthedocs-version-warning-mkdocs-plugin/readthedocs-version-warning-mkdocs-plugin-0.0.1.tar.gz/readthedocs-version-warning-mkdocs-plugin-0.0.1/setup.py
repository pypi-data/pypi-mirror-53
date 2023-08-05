from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='readthedocs-version-warning-mkdocs-plugin',
    version='0.0.1',
    packages=['mkdocs_version_warning'],
    url='https://github.com/grossmannmartin/readthedocs-version-warning-mkdocs-plugin',
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Martin Grossmann',
    author_email='martin@vyvoj.net',
    description='ReadTheDocs version warning MkDocs plugin replace placeholder text with warning banner '
                'for specific versions if deployed on Readthedocs',
    install_requires=['mkdocs', 'requests'],

    # The following rows are important to register your plugin.
    # The format is "(plugin name) = (plugin folder):(class name)"
    # Without them, mkdocs will not be able to recognize it.
    entry_points={
        'mkdocs.plugins': [
            'readthedocs-version-warning = mkdocs_version_warning:VersionWarning',
        ]
    },
)
