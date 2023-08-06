import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cartograph",
    version="0.0.1",
    author="Alastair Flynn",
    author_email="contact@alastairflynn.com",
    description="A package for drawing map tiles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://alastairflynn.com/cartograph",
    project_urls = {'Documentation':'https://alastairflynn.com/cartograph',
                    'Source code':'https://github.com/alastairflynn/cartograph'},
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    install_requires=['numpy>=1.3.0', 'scipy>=0.9.0', 'matplotlib>=3.0.0']
)
