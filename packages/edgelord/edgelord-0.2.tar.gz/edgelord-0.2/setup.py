from distutils.core import setup

setup(
    name = 'edgelord',
    packages = ['edgelord'],
    version = '0.2',  # Ideally should be same as your GitHub release tag varsion
    description = 'A module for non-voodo equity analysis',
    author = 'Dylan E. Holland',
    author_email = 'salinson1138@gmail.com',
    url = 'https://github.com/edgyquant/edgelord/',
    download_url = 'https://github.com/edgyquant/edgelord/archive/0.2.tar.gz',
    keywords = ['stock', 'equity', 'analysis'],
    classifiers = [],
    install_requires=[
        'pandas',
        'scipy'
    ]
)