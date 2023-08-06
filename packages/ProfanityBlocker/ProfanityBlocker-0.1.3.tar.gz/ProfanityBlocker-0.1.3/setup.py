from distutils.core import setup

try:
  with open("README.md", "r") as fh:
    long_description = fh.read()
except:
  long_description = ""

setup(
  name = 'ProfanityBlocker',
  packages = ['ProfanityBlocker'],
  version = '0.1.3',
  license='MIT',
  description = 'A Python Intergration For The Profanity Blocker API',
  author = 'David Crompton',
  author_email = 'davidallancrompton@outlook.com',
  long_description=long_description,
  long_description_content_type="text/markdown",
  url = 'https://github.com/voarsh/ProfanityBlocker-Python-Implementation',
  download_url = 'https://github.com/voarsh/ProfanityBlocker-Python-Implementation/archive/master.tar.gz',
  keywords = ['Profanity Blocker', 'Profanity', 'Word Filter', 'Filter'],
  install_requires=[ 
          'requests',
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