import os
from setuptools import setup

from guessenc import __version__

# PyPI:
# $ python setup.py sdist bdist_wheel
# $ twine upload dist/guessenc-x.y

here = os.path.abspath(os.path.dirname(__file__))

if __name__ == "__main__":
    setup(
        name="guessenc",
        version=__version__,
        author="Brad Solomon",
        author_email="brad.solomon.1124@gmail.com",
        description="Infer HTML encoding from response headers & content",
        license="MIT",
        keywords="encoding http html chardet detection",
        url="https://github.com/bsolomon1124/guessenc",
        long_description=open(os.path.join(here, "README.md"), encoding="utf-8").read(),
        long_description_content_type="text/markdown",
        install_requires=["lxml", "chardet"],
        packages=["guessenc"],
        tests_require=["pytest"],
        python_requires=">=3.5",
        classifiers=[
            "Intended Audience :: Developers",
            "Development Status :: 3 - Alpha",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: Implementation :: CPython",
        ],
    )
