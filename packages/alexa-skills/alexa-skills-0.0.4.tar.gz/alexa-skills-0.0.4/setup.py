import setuptools

with open("README.md", "r") as file:
    long_description = file.read()

requires = [
]

packages = [
    "alexa_skills",
    "alexa_skills.requests",
    "alexa_skills.responses",
    "alexa_skills.session",
    "alexa_skills.helpers"
]

setuptools.setup(
    name="alexa-skills",
    version="0.0.4",
    author="Alistair O'Brien",
    author_email="alistair@duneroot.co.uk",
    description="A Python Alexa Skills Package.",
    long_description=long_description,
    include_package_data=True,
    long_description_content_type="text/markdown",
    url="https://github.com/johnyob/alexa-skills",
    packages=packages,
    install_requires=requires,
)
