from setuptools import setup, find_packages

setup(
    name="m3wal",
    version="1.0.0",
    packages=find_packages(),
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
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MDiaznf23/m3wal",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
