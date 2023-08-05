from setuptools import setup, find_packages

setup(
    name="stephen",
    version="0.1.0",
    py_modules=["stephen"],
    packages=find_packages(),
    include_package_data=True,
    entry_points="""
        [console_scripts]
        stephen=stephen.stephen:main
    """,
)
