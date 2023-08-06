from setuptools import setup, find_packages
import versioneer

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='mantid_total_scattering',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      author='Marshall, Elliot, Pete',
      author_email='mcondonnellmd@ornl.gov',
      url='https://github.com/marshallmcdonnell/mantid_total_scattering',
      description='Mantid Total Scattering Reduction',
      long_description_content_type="text/markdown",
      license='GPL License (version 3)',
      entry_points={
        'console_scripts': [
            "mantidtotalscattering = total_scattering.cli:main"
        ]
      },
      install_requires=['six>=1.9'],
      packages=find_packages(),
      # package_data={'': ['*.ui', '*.png', '*.qrc', '*.json']},
      include_package_data=True,
      test_suite='tests',
      tests_require=['pytest']
      )
