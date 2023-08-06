"""
test package
"""

import setuptools

REQUIRED = [
    "numpy",
    "pandas"
]

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()
    setuptools.setup(
        name="lambdata-coopwilliams",
        version="0.0.1",
        author="coop",
        description="test package",
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        url="https://lambdaschool.com/courses/data-science",
        packages=setuptools.find_packages(),
        python_requires=">=3.5",
        install_required=REQUIRED,
        classifiers=["Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent"
        ]
    )
