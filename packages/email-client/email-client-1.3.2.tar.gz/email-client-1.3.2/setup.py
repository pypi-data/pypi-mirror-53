import setuptools


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


with open("README.md", "r") as fh:
    long_description = fh.read()

install_reqs = parse_requirements('./requirements')
print(install_reqs)

setuptools.setup(
    name="email-client",
    version="1.3.2",
    author="Egor Urvanov",
    author_email="hedgehogues@bk.ru",
    description="Email clients for grader and other services of fless.pro",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Flesspro/email-client",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    install_requires=install_reqs,
)
