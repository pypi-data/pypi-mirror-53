import setuptools

# Read package long description
with open('README.md', 'r') as h:
    long_description = h.read()

# Package setup
setuptools.setup(
    name='nameko_cli',
    version='0.0.6',
    author='li1234yun',
    author_email='li1234yun@163.com',
    description='nameko cli tools',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['nameko_cli'],
    package_dir={'nameko_cli': 'nameko_cli'},
    package_data={'nameko_cli': ['templates/*', 'templates/.gitignore', 'templates/config/*', 'templates/service/*']},
    install_requires=[
        'click'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'nameko-cli = nameko_cli.run:cli'
        ]
    }
)
