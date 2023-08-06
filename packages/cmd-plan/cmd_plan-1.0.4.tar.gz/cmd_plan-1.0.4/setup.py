from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='cmd_plan',
    version='1.0.4',
    packages=find_packages(),
    author='BorisPlus',
    author_email='cmd_plan@borisplus.ru',
    description="Python3 OS commands run dependency planner",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
)
