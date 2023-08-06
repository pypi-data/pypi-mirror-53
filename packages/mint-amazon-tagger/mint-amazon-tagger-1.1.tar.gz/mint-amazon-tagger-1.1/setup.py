import os
import setuptools
from deleteallgooglephotos import VERSION

with open("README.md", "r") as fh:
    long_description = fh.read()


class CleanCommand(setuptools.Command):
    """Custom clean command to tidy up the project root."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')


setuptools.setup(
    name="mint-amazon-tagger",
    version=VERSION,
    author="Jeff Prouty",
    author_email="jeff.prouty@gmail.com",
    description=("Helps you delete all of your Phoros from Google Photos."),
    keywords='google photos delete all',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jprouty/delete-all-google-photos",
    packages=setuptools.find_packages(),
    python_requires='>=3',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'outdated',
        'progress',
        'selenium',
    ],
    entry_points=dict(
        console_scripts=[
            'delete-all-google-photos=deleteallgooglephotos.main:main',
        ],
    ),
    cmdclass={
        'clean': CleanCommand,
    },
)
