from setuptools import setup

version = '0.3.0'

setup(
    name='musical',
    version=version,
    url='https://github.com/jollyhrothgar/banjo_liberation/python-musical',
    author='Davy Wybiral, Mike Beaumier',
    author_email='davy.wybiral@gmail.com, michael.beaumier@gmail.com',
    description='A python library for dealing with sounds and music',
    keywords = 'audio music theory synthesis',
    packages=['musical', 'musical.audio', 'musical.theory'],
    platforms='any',
    install_requires=[
        'numpy',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Artistic Software',
        'Topic :: Multimedia :: Sound/Audio :: Sound Synthesis',
    ],
)
