from distutils.core import setup
setup(
  name = 'FuckingSunday',         # How you named your package folder (MyLib)
  packages = ['FuckingSunday','FuckingSunday.fuck.that.shit','FuckingSunday.fuck.that.dick','FuckingSunday.sundays.a.fun.day'],   # Chose the same as "name"
  version = '0.4',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Fucking Sunday, guys! It\'s fucking sunday (again!)',   # Give a short description about your library
  author = 'That Dude You Don\'t Want In Your Home',                   # Type in your name
  author_email = 'vidner123@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/spookyahell/FuckingSunday',   # Provide either the link to your github or to your website
  download_url = 'https://codeload.github.com/spookyahell/FuckingSunday/tar.gz/master',    # I explain this later on
  keywords = ['FUN','TEST','STUPID','DICK','SUNDAY'],   # Keywords that define your package best
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)