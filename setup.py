from setuptools import setup

setup(name='pykhipu',
      version='0.1.0',
      description='Wrapper for the Khipu payment service API v2.0',
      url='http://github.com/fixmycode/pykhipu',
      author='Pablo Albornoz',
      author_email='pablo.albornoz.n@gmail.com',
      license='MIT',
      packages=['pykhipu'],
      install_requires=['requests'],
      zip_safe=False)
