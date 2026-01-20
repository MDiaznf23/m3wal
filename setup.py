from pathlib import Path
from setuptools import setup, find_packages

# Read README.md for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="m3wal",
    version="1.1.8",
    packages=find_packages(),
    package_data={
        'm3wal': ['templates/*.template'],
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
    description="Material 3 wallpaper-based color scheme generator for Linux desktop theming",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MDiaznf23/m3wal",
    project_urls={
        "Bug Tracker": "https://github.com/MDiaznf23/m3wal/issues",
        "Documentation": "https://github.com/MDiaznf23/m3wal#readme",
        "Source Code": "https://github.com/MDiaznf23/m3wal",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Desktop Environment",
        "Topic :: System :: Installation/Setup",
        "Topic :: Utilities",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Environment :: Console",
    ],
    keywords=[
        "material-design",
        "material3",
        "color-scheme",
        "wallpaper",
        "theming",
        "rice",
        "ricing",
        "linux",
        "desktop",
        "gtk",
        "customization",
    ],
    python_requires=">=3.7",
    license="MIT",
)
