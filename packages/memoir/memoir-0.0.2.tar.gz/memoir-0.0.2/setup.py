from pathlib import Path

from setuptools import (find_packages,
                        setup)

import memoir

project_base_url = 'https://github.com/lycantropos/memoir/'

tests_require = Path('requirements-tests.txt').read_text()

setup(name='memoir',
      packages=find_packages(exclude=('tests', 'tests.*')),
      version=memoir.__version__,
      description=memoir.__doc__,
      long_description=Path('README.md').read_text(encoding='utf-8'),
      long_description_content_type='text/markdown',
      license='MIT License',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Operating System :: POSIX',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
      ],
      author='Azat Ibrakov',
      author_email='azatibrakov@gmail.com',
      url=project_base_url,
      download_url=project_base_url + 'archive/master.zip',
      python_requires='>=3.5.3',
      tests_require=tests_require)
