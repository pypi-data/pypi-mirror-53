from setuptools import setup


setup(name='nhl_scraper',
      version='0.0.1',
      description='Scrape hockey data from websites such as NHL.com',
      url='http://github.com/spilchen/nhl_scraper',
      author='Matt Spilchen',
      author_email='matt.spilchen@gmail.com',
      license='MIT',
      packages=['nhl_scraper'],
      setup_requires=["pytest-runner"],
      tests_require=["pytest"],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.7',
      ],
      install_requires=['pandas', 'objectpath', 'requests'],
      python_requires='>=3',
      include_package_data=True,
      zip_safe=True)
