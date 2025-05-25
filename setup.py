from setuptools import setup, find_packages


setup(
    name="rest_course",
    version="0.1",
    author="Yurii Bakai",
    description="Laboratory works for the course REST API Programming",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi==0.115.12",
        "uvicorn==0.34.2",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.13",
        "Framework :: FastAPI",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.13"
)
