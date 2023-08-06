from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='agung96tm_funniest',
      version='0.1.4',
      description='The agung96tm_funniest jokes',
      long_description=readme(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          # 'Licence :: OSI Approved :: MIT Licence',
          'Programming Language :: Python :: 2.7',
          'Topic :: Text Processing :: Linguistic',
      ],
      keywords='funniest joke comedy flying circus',
      url='http://localhost:8000',
      author='king',
      author_email='king@example.com',
      license='MIT',
      packages=['agung96tm_funniest'],
      install_requires=[
          'markdown',
      ],
      zip_safe=False)
