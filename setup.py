from setuptools import setup, find_packages

setup(
    name="digital-life-primordium",
    version="0.0.1",
    description="Digital Life Primordium — A conceptual research framework for next-generation autonomous agents",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="suoyinjv",
    author_email="1782550525@qq.com",
    url="https://github.com/suoyinjv/digital-life-primordium",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.10",
    install_requires=[],
)
