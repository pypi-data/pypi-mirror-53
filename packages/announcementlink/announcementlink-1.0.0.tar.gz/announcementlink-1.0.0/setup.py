import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="announcementlink",
    version="1.0.0",
    author="Riley Brown",
    description="A speech system for places like train stations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Chookman5/AnnouncementLink",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
