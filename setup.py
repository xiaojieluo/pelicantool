from setuptools import setup
from pelicantool import __version__

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

packages = ['pelicantool']
test_requirements = ['pytest>=3.1.2', 'pytest-cov']

entry_points = {
    'console_scripts': [
        'pelicantool = pelicantool.__main__:main',
    ]
}

requires = ['toml>=0.9.4', 'requests>=2.18.4', 'six>=1.10.0']

setup(
    name='pelicantool',
    keywords='pelican auto tool',
    version = __version__,
    description='pelican auto tool',
    long_description=readme,
    author='Luo Xiaojie',
    author_email='xiaojieluoff@gmail.com',
    url='https://github.com/xiaojieluo/pelicantool',
    license=license,
    packages=packages,
    tests_require=test_requirements,
    install_requires=requires,
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ),
    test_suite='tests',
    entry_points=entry_points,

    python_requires='>=3',
)
