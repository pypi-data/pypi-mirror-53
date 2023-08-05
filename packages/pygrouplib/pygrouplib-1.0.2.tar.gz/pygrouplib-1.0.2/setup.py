import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="pygrouplib",
	version="1.0.2",
	author="Nenad Popovic",
	author_email="popovic0706@gmail.com",
	description="Library for dividing entities into groups based on numeric or text value.",
	keywords="group fuzzy approximate levenshtein text numeric",
	long_description=long_description,
	long_description_content_type='text/markdown',
	url="https://github.com/popovicn/pygrouplib",
	packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
	)
