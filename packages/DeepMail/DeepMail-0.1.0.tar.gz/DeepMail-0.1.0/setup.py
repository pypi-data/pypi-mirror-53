import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="DeepMail",
    version="0.1.0",
    author="SaiReddy",
    author_email="vsaichandrareddy@gmail.com",
    description="Sending mails in Deep Learning projects to know how it is working",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/saichandrareddy1/MailSender",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
