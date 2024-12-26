from setuptools import setup, find_packages

setup(
    name="round-robin",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.104.1",
        "uvicorn==0.24.0",
        "httpx==0.25.1",
    ],
    extras_require={
        "test": [
            "pytest==7.4.3"
        ],
    },
)