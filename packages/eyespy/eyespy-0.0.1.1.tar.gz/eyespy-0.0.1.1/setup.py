import setuptools

setuptools.setup(
    name="eyespy",
    version="0.0.1.1",
    author="Josh Hunt",
    author_email="hunt.brian.joshua@gmail.com",
    description="",
    long_description="",
    url="https://github.com/jbhunt/eyepy",
    packages=setuptools.find_packages(exclude=['*.display']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)