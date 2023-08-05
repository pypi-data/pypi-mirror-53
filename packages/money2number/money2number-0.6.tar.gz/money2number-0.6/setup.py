from setuptools import setup, find_packages

with open("README.md", "r") as fh:
      setup(name='money2number',
            version='0.6',
            author='Sarsiz Chauhan',
            author_email='sarsiz97@gmail.com',
            description='Convert a single money related term in a sentence in any format to float.',
            packages=find_packages(exclude=['tests']),
            long_description=open('README.md').read(),
            long_description_content_type="text/markdown",
            url='https://github.com/sarsiz/money_to_number',
            zip_safe=False)