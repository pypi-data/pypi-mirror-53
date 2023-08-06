import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sacada-python",
    version="0.0.5",
    author="Pedro Henrique Capp Kopper",
    author_email="pedro.kopper@ufrgs.br",
    description="Python API for the SACADA data acquisition system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.cta.if.ufrgs.br/SACADA/sacada-python",
    packages=['sacada'],
    scripts=['bin/sacada'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: Portuguese (Brazilian)",
        "Topic :: Scientific/Engineering",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pyserial',
        'tqdm',
        'click',
        'thermocouples-reference',
        'scipy'
    ],
    python_requires='>=3.6',
)
