import setuptools

with open("PCAViz/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pcaviz-durrantlab",
    version="1.2",  # Version for test pip not necessarily the same for production
    author="Jacob Durrant",
    author_email="durrantj@pitt.edu",
    description="A script to compress molecular dynamics simulations so they can be visualized with PCAViz in a web browser.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://git.durrantlab.com/jdurrant/pcaviz",
    packages=setuptools.find_packages(),
    requires=['scikit_learn (>=0.19.1)', 'numpy (>=1.15.2)', 'MDAnalysis (>=0.17.0)'],
    install_requires=['scikit_learn>=0.19.1', 'numpy>=1.15.2', 'MDAnalysis>=0.17.0'],
    package_data={'PCAViz': ['*.md', 'examples/*']},
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
    scripts=['bin/pcaviz']
)
