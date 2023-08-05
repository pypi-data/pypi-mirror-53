from setuptools import setup, find_packages

setup(
    name = "scrapy-appleauth",
    version = "0.0.5",
    keywords = ("pip", "datacanvas", "eds", "xiaoh"),
    description = "apple auth downloader middleware for scrapy",
    long_description = "apple auth downloader middleware for scrapy",
    license = "MIT Licence",

    url = "https://github.com/geek-dc/scrapy-appleauth",
    author = "derekchan",
    author_email = "dchan0831@gmail.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['pyjwt']
)