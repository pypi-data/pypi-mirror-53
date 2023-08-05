import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="example_pkg_PANDASTEST_01",
	version="0.0.1",
	author="Ameer Bajwa",
	author_email="ameer@gluon.com",
	description="A small example package using pandas",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
	install_requires=[
		"pandas"
	]
)
