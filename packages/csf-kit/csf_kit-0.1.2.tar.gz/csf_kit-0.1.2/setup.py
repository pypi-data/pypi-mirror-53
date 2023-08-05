from setuptools import setup, find_packages

setup(name='csf_kit',
      version='0.1.2',
      description='StartKit for ChinaScope data',
      author='ChinaScope',
      packages=find_packages(),
      include_package_data = True,
      platform='any',
      install_requires=['pandas', 'numpy', 'alphalens', 'zipfile37', 'python-dateutil']

      )


