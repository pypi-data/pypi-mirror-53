import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="viewasuser",
    version="1.0.4",
    author="Tarikul Islam",
    author_email="ti.rasel@gmail.com",
    description="Django View As user is a middleware thats provides login in as any user functionality. It is modification of [django-view-as] package. The django-view-as is not supported on django 2 and newer version, so I have modified the package.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/raselTarikul/ViewASUser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)
