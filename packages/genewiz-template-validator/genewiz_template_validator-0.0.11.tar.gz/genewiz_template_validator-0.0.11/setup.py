from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='genewiz_template_validator',
      version='0.0.11',
      description='G001 data entry validation for Genewiz templates.',
      author='Greg Finak',
      author_email='gfinak@fredhutch.org',
      license='MIT',
      packages=['genewiz_template_validator'],
      scripts=['bin/validate_genewiz_templates'],
      install_requires=['xlrd'],
      long_description=readme(),
      long_description_content_type='text/x-rst',
      include_package_data=True,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
          'Topic :: Utilities',
      ],
      keywords='validation genewiz templates',
      zip_safe=False)
