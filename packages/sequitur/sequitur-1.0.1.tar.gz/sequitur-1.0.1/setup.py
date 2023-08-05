try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
# from codecs import open

setup(
    name="sequitur",
    description="Recurrent Autoencoder for sequence data that works out-of-the-box ",
    version="v1.0.1",
    packages=["sequitur"],
    python_requires=">=3",
    url="https://github.com/shobrook/sequitur",
    author="shobrook",
    author_email="shobrookj@gmail.com",
    # classifiers=[],
    install_requires=['torch'],
    keywords=["sequitur", "autoencoder", "lstm", "sequence", "sequence-data", "seq2seq"],
    license="MIT"
)
