import setuptools
from distutils.core import setup

setup(
  name = 'PqrUploadModule',         # How you named your package folder (MyLib)
  packages = ['PqrUploadModule'],   # Chose the same as "name"
  version = '0.0.12',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Connection AT-TD',   # Give a short description about your library
  author = 'ppp',                   # Type in your name
  author_email = 'petronije2002@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/petronije2002/PqrUpload/',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/petronije2002/PqrUpload/archive/0.0.10.tar.gz',    # I explain this later on
  keywords = ['Autotask', 'Topdesk', 'Connection'],   # Keywords that define your package best
  install_requires = [ 'atws<=0.5.3','azure-functions<=1.0.4','backcall<=0.1.0','bleach<=3.1.0','cached-property<=1.5.1',
  'certifi<=2019.6.16','chardet<=3.0.4','decorator<=4.4.0','docutils<=0.15.2','future<=0.17.1','idna<=2.8','imageio<=2.5.0',
  'ipykernel<=5.1.2','ipython<=7.8.0','ipython-genutils<=0.2.0','jedi<=0.15.1','jupyter-client<=5.3.1','jupyter-core<=4.5.0',
  'numpy<=1.17.2','pandas<=0.25.1','parso<=0.5.1','pexpect<=4.7.0','pickleshare<=0.7.5','Pillow<=6.1.0','pkginfo<=1.5.0.1',
  'prompt-toolkit<=2.0.9','ptyprocess<=0.6.0','Pygments<=2.4.2','python-dateutil<=2.8.0','pytz<=2019.2',
  'pyzmq<=18.1.0','readme-renderer<=24.0','requests<=2.22.0','requests-toolbelt<=0.9.1','six<=1.12.0','suds-jurko<=0.6','tornado<=6.0.3',
  'tqdm<=4.36.1','traitlets<=4.3.2','twine<=2.0.0','urllib3<=1.25.3','wcwidth<=0.1.7','webencodings<=0.5.1','xmltodict<=0.12.0'] , 
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)