from setuptools import setup, find_packages

setup(name='holiday_jp',
      version='19.09.28',
      url='https://github.com/LUXEYS/holiday_jp-python',
      license='MIT',
      author='Luxeys',
      author_email='tessier@luxeys.com',
      description='Japanese holiday for Python',
      long_description_content_type="text/markdown",
      packages=find_packages(),
      long_description=open('README.md').read(),
      zip_safe=False,
      install_requires=[
        "python-dateutil==2.7.5",
      ],
      classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
])
