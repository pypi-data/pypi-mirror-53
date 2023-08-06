from setuptools import setup

setup(
    name="ioc_strings",
    version="0.1.4",
    author="CinCan",
    author_email="cincan@cincan.io",
    description="Extract IOC strings from files, just like Linux strings command, but only IOCs.",
    license="MIT",
    url="https://gitlab.com/CinCan/ioc_strings",
    packages=["ioc_strings"],
    install_requires=["iocextract", "validators"],
    entry_points = {
        "console_scripts": [
            "iocstrings = ioc_strings.ioc_strings:main"
        ]
    }
)
