"""
Configuration d'installation du package de détection d'anomalies.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="gestionlogs-anomaly-detector",
    version="2.0.0",
    author="Louis COLLAS Erwan NICOLAS Nathan Brunet",
    description="Système de détection d'anomalies dans les logs HDFS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Louloucoco2l/gestion_logs",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "gestionlogs=main:main",
        ],
    },
)
