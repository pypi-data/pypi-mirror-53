import setuptools

with open("libHREELS/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="libHREELS",
    version="0.2.4",
    author="Wolf Widdra",
    author_email="wolf.widdra@gmx.de",
    description="Handling and ploting vibrational spectroscopy HREELS data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.informatik.uni-halle.de/e3fm8/libhreels",
    packages=setuptools.find_packages(),
	include_package_data = True,
	#packages=['HREELS'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)