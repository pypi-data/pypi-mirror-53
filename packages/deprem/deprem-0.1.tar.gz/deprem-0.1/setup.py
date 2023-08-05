from distutils.core import setup
setup(
  name = 'deprem',
  packages = ['/Users/Mehmet/Desktop/deprem'],
  version = '0.1',
  license='MIT',
  description = 'pydeprem lets you programmatically access Kandilli Earthquake Observatory data',
  author = 'Mehmet Altuntaş',
  author_email = 'mehmetccm@gmail.com',
  url = 'https://github.com/mehmetcc/pydeprem',
  download_url = 'https://github.com/mehmetcc/deprem/archive/v_01.tar.gz',
  keywords = ['turkish', 'earthquake'],
  install_requires=[
          'lxml',
          'requests'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
