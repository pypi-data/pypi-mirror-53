from setuptools import setup, find_packages

setup(
    name="j2db",
    version="0.1.0",
    description="standard and safe way to upload your json to db",
    author="williamfzc",
    author_email="fengzc@vip.qq.com",
    url="https://github.com/williamfzc/j2db",
    packages=find_packages(),
    include_package_data=True,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
        "fastapi",
        "uvicorn",
        "pydantic",
        "python-multipart",
        "loguru",
        "sqlalchemy",
        "PyMySQL",
    ],
)
