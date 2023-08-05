import setuptools

with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    author="Rafael Izidoro",
    author_email="izidoro.rafa@gmail.com",
    url="https://github.com/rizidoro/sqload",
    name="sqload",
    version="0.1.0",
    py_modules = ['sqload'],
    package_data={'': ['LICENSE']},
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="A simple utility tool that scan SQL files with queries separated by comments into python dicts.",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
    ],
)
