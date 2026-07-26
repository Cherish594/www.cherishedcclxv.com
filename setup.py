from setuptools import setup, find_packages

setup(
    name="android-repair-cli",
    version="1.0.0",
    description="Python CLI tool for Android device recovery and repair",
    author="Cherish594",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "android-repair=main:cli",
        ],
    },
    install_requires=[
        "adb-shell==0.3.3",
        "click==8.1.7",
        "colorama==0.4.6",
        "requests==2.31.0",
        "pyyaml==6.0.1",
        "psutil==5.9.6",
    ],
    python_requires=">=3.7",
)
