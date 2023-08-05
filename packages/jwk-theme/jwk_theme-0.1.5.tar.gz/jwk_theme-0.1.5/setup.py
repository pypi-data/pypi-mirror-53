"""Setup file
"""

import setuptools
import jwk_theme

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='jwk_theme',
                 version=jwk_theme.__version__,
                 description='Pelican theme',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url=jwk_theme.__github_url__,
                 author='James W. Kennington',
                 author_email='jameswkennington@gmail.com',
                 license='MIT',
                 packages=setuptools.find_packages(),
                 zip_safe=False,
                 include_package_data=True)
