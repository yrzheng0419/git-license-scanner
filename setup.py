from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="git-license-scanner",
    version="0.5.0",
    author="YOU-RONG, ZHENG",  # 改成你的名字
    author_email="ghhab852@gmail.com",  # 改成你的 email
    description="A CLI tool to scan and identify software licenses in Git repositories",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/git-license-scanner",  # 改成你的 GitHub
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=[
        "click>=8.1.0",
        "GitPython>=3.1.0",
        "colorama>=0.4.6",
        "rich>=13.0.0",
        "PyYAML>=6.0",
        "requests>=2.31.0",
    ],
    entry_points={
        "console_scripts": [
            "license-scan=license_scanner.cli:scan",
        ],
    },
)