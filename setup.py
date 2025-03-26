from setuptools import setup, find_packages

setup(
    name="tb-to-csv",
    version="1.0.0",
    description="Extract metrics from TensorBoard event files and export to CSV.",
    author="Anton Zamyatin",
    author_email="anton.zamyatin14@gmail.com",
    url="https://github.com/tonyzamyatin/tb-to-csv",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scipy",
        "tensorboard",
    ],
    entry_points={
        "console_scripts": [
            "tensorboard_to_csv=cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)