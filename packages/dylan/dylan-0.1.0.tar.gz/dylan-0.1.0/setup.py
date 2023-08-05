from setuptools import setup, find_packages

setup(
    name="dylan",
    version="0.1.0",
    py_modules=["dylan"],
    packages=find_packages(),
    include_package_data=True,
    entry_points="""
        [console_scripts]
        dylan=dylan.dylan:main
    """,
)
