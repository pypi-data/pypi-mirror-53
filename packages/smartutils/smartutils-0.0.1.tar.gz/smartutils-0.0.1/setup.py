import setuptools

setuptools.setup(
    name="smartutils",
    version="0.0.1",
    author="Arockia Arulnathan",
    author_email="arockia@scriptinghub.com",
    description="A lightweight package to measure the execution time of function",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)