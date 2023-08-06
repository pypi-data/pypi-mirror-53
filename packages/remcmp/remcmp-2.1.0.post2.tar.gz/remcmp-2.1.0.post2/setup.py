from setuptools import setup


with open("README.md") as rf:
    readme = rf.read()

setup(
        name = "remcmp",
        version = "2.1.0.post2",
        author = "DimiDimit",
        author_email = "dmtrdmtrov@gmail.com",
        description = "Extensible program to compare local and remote directories.",
        long_description = readme,
        long_description_content_type = "text/markdown",
        url = "https://github.com/DimiDimit/remcmp",
        packages = ["remcmp"],
        classifiers = [
            "Environment :: Console",
            "License :: OSI Approved :: MIT License",
            "Natural Language :: English",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3 :: Only",
            "Topic :: System :: Filesystems",
            "Topic :: Utilities"
        ],
        python_requires = ">=3.7",
        install_requires = ["colorama", "fs"],
        entry_points = {
            "console_scripts": [
                "remcmp = remcmp:main"
            ]
        }
)
