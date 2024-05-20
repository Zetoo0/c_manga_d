from setuptools import setup, find_packages

setup(
    name="c_manga_d",
    version="0.0.1",
    packages=find_packages(),
    install_requires=["argparse","tkinter","PIL","requests","python-dotenv"],
    py_modules=['manga','nmain','reader'],
)