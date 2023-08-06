import setuptools
with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name='screenwriter',
	version='1.0.3',
	author="S Satapathy",
	author_email="shubhakant.satapathy@gmail.com",
	description="python library for writing progress texts, echo messages, warnings and errors to standard output",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/satapathy/pypi-screenwriter",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
 )
