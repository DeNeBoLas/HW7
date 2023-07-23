from setuptools import setup, find_namespace_packages

setup(
    name="clean_folder",
    version="0.0.1",
    description="Very useful code",
    # url="http://github.com/dummy_user/useful",
    author="Svitlana Ilchenko",
    author_email="svitlana-ilchenko@ukr.net",
    packages=find_namespace_packages(),
    entry_points={"console_scripts": ["clean-folder = clean_folder.clean:clean"]},
)
