import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="django-rest-api-logger",
    version="0.1",
    description="Log everything from you drf view",
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
        "django",
        "wheel",
        "djangorestframework"
    ],
    # entry_points={
    #     "console_scripts": [
    #         "django_rest_api_logger=django_rest_api_logger.__main__:main",
    #     ]
    # },
)
