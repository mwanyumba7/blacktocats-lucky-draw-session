from setuptools import setup, find_packages

setup(
    name='github-commenter-raffle',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A raffle system that selects a winner from GitHub issue commenters.',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'Flask',
        'requests',
        'PyGithub'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)