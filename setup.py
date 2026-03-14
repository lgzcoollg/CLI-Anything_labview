from setuptools import setup, find_namespace_packages

setup(
    name="cli-anything-labview",
    version="0.1.0",
    description="CLI Anything harness for LabVIEW",
    packages=find_namespace_packages(include=["cli_anything.*"]),
    install_requires=[
        "click",
    ],
    entry_points={
        "console_scripts": [
            "cli-anything-labview=cli_anything.labview.labview_cli:cli",
        ],
    },
    python_requires=">=3.10",
)
