from setuptools import setup, find_packages

setup(
    name="m3wal",
    version="1.1.3",
    packages=find_packages(),
    package_data={
        'm3wal': ['templates/*.template'],  # Include templates
    },
    install_requires=[
        "material-color-utilities",
        "Pillow",
    ],
    entry_points={
        'console_scripts': [
            'm3wal=m3wal.m3wal:main',
        ],
    },
    author="Diaz",
    description="Material 3 wallpaper color scheme generator",
    url="https://github.com/MDiaznf23/m3wal",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
