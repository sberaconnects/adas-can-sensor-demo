from setuptools import setup, find_packages

setup(
    name="adas_can_demo",
    version="0.1.0",
    description="ADAS CAN Sensor Simulator and Visualizer",
    author="Sudhir Kumar Bera",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "python-can",
        "pytest",
        "matplotlib",
        "dash",
        "pyyaml",
    ],
    entry_points={
        "console_scripts": [
            "adas-demo=main:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
