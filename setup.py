from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='pykhipu',
    version='0.1.4',
    description='Wrapper for the Khipu payment service API v2.0',
    long_description=readme(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Environment :: Console',
    ],
    url='http://github.com/fixmycode/pykhipu',
    author='Pablo Albornoz',
    author_email='pablo.albornoz.n@gmail.com',
    license='MIT',
    packages=['pykhipu'],
    install_requires=['six', 'python-dateutil', 'requests'],
    zip_safe=False)
