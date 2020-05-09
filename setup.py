import pathlib

from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="django-rest-api-logger",
    version="0.4",
    description="Log everything from your drf view",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/navidagz/django-rest-api-logger",
    author="Navid Agz",
    author_email="navidagz76@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=["django_rest_api_logger"],
    install_requires=[
        "pymongo",
        "django",
        "wheel",
        "djangorestframework",
    ]
)
