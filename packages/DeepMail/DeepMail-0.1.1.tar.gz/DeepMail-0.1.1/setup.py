import setuptools
from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
  name = 'DeepMail',         # How you named your package folder (MyLib)
  packages = ['DeepMail'],   # Chose the same as "name"
  version = '0.1.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'For mail Deep learning',   # Give a short description about your library
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'SaiReddy',                   # Type in your name
  author_email = 'vsaichandrareddy@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/saichandrareddy1/MailSender',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/saichandrareddy1/MailSender/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['Mail', 'DeepLearning', 'Sending'],   # Keywords that define your package best
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7'
	
  ],
)
