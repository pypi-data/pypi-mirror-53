from setuptools import setup, find_packages

setup(
    name = "scrapy-googleauth",
    version = "0.1.0",
    keywords = ("pip", "datacanvas", "eds", "xiaoh"),
    description = "google auth downloader middleware for scrapy",
    long_description = "google auth downloader middleware for scrapy",
    license = "MIT Licence",

    url = "https://github.com/geek-dc/scrapy-googleauth",
    author = "derekchan",
    author_email = "dchan0831@gmail.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['oauth2client']
)