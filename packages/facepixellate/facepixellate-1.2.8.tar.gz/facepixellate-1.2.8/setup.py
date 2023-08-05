import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="facepixellate",
    version="1.2.8",
    author="Tom Tillo",
    author_email="tomtillo@gmail.com",
    description="Detect and pixellate faces in the picture",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tomtillo/facepixellate",
    packages=["facepixellate"],
    include_package_data=True,
    install_requires=["opencv-python"],    
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)