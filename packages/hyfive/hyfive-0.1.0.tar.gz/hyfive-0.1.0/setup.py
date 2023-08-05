import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
  name="hyfive",
  version="0.1.0",
  license="gpl-3.0",
  description="A Hy library that provides a Lispy functional \
               interface by wrapping Python's popular data libraries,  \
               such as Pandas and Matplotlib.",
  long_description=long_description,
  long_description_content_type="text/markdown",
  author="Anthony Khong",
  author_email="anthony@arithmox.ai",
  url="https://gitlab.com/arithmox/hyfive",
  install_requires=[
      "cytoolz>=0.10.0",
      "dask-ml>=1.0.0",
      "dask>=2.3.0",
      "hy>=0.17.0",
      "hypothesis>=4.32.3",
      "ipython>=7.7.0",
      "matplotlib>=3.1.1",
      "pandas>=0.25.0",
      "pdbpp>=0.10.0",
      "pytest-cov>=2.7.1",
      "pytest>=5.0.1",
      "scikit-learn>=0.21.3",
      "scipy>=1.3.1",
      ],
  packages=setuptools.find_packages(),
  classifiers=[
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Operating System :: OS Independent",
    "Topic :: Database",
  ],
)
