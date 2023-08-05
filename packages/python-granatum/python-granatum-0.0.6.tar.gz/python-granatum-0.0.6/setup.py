import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-granatum",
    version="0.0.6",
    author="dustintheglass",
    author_email="dustin.glass@gmail.com",
    description="A Python wrapper for Granatum Financeiro",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dustinglass/python-granatum",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Office/Business :: Financial :: Accounting",
    ],
    python_requires='>=3.6',
    install_requires=[
        'lxml',
        'pandas',
        'python-dateutil',
        'requests',
    ]
)
