import setuptools

VERSION = "0.0.34"

setuptools.setup(
  name='techlabreactor',
  packages=['techlabreactor'],
  version=VERSION,
  description='Utility for performing replay analysis of SC2 replays',
  author='Hugo Wainwright',
  author_email='wainwrighthugo@gmail.com',
  url='https://github.com/frugs/techlab-reactor',
  keywords=['sc2', 'replay', 'sc2reader'],
  classifiers=[],
  install_requires=['sc2reader'],
)
