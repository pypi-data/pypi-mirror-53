from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="project-deap",
    version="0.0.3",
    author="joseroberts87",
    author_email="jose.roberts@intracitygeeks.org",
    description="Data Engineering Analytics Platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JoseRoberts87/project-deap",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
    ],
    python_requires='>=3.6',
)
