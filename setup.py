from distutils.core import setup
import relativedeltafield


setup(name = "relativedeltafield",
      author = "Samuel Andersson",
      url = "http://github.com/trew/relativedeltafield",
      version = relativedeltafield.__version__,
      packages = [
          'relativedeltafield',
      ],
      install_requires = [
          'Django==1.4',
          'python-dateutil>=1.5',
      ]
)

