from distutils.core import setup
setup(
  name='wxparser',
  packages=['wxparser'],
  version='0.5',
  license='MIT',
  description ='parser for wx article ',
  author='Mario',                   # Type in your name
  author_email ='laohan.msa@gmail.com',      # Type in your E-Mail
  url ='https://github.com/laohanmsa/wxparser.git',
  download_url = 'https://github.com/laohanmsa/wxparser/archive/v0.5.tar.gz',    # I explain this later on
  keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 2',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 2.7',
  ],
)