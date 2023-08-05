from setuptools import setup, find_packages

setup(
    name="petersPythonLogger",
    version="0.1.0",
    py_modules=["petersPythonLogger"],
    packages=find_packages(),
    include_package_data=True,
    entry_points="""
        [console_scripts]
        petersPythonLogger=petersPythonLogger.petersPythonLogger:main
    """,
)
