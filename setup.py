from setuptools import find_packages, setup

PACKAGE = "ddemblem"
NAME = "ddemblem"
DESCRIPTION = "一个用于Bilibili粉丝勋章经验爬取的简单工具"
AUTHOR = "BYOUINZAKA"
AUTHOR_EMAIL = "2606675531@qq.com"
URL = "https://github.com/BYOUINZAKA/DD-Emblem"
VERSION = __import__(PACKAGE).__version__

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="MIT",
    url=URL,
    packages=find_packages(),
    include_package_data=False,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
    ],
    zip_safe=False,
)
