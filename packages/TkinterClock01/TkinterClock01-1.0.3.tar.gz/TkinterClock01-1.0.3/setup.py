import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TkinterClock01",
    version="1.0.3",
    author="Quantum_Wizard",
    author_email="minecraftcrusher100@gmail.com",
    description="""A tkinter based window clock, dipslays time, date, and clock name.""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GrandMoff100/TkinterClock01",
    packages=setuptools.find_packages(include=["tkinterclock01"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.7',
    install_requires=['omegamath01'],
)
