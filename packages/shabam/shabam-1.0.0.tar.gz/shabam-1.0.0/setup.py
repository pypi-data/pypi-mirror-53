
import io
from setuptools import setup

setup(
    name = "shabam",
    version = "1.0.0",
    author = "Daniel Rice",
    author_email = "daniel.rice@sanger.ac.uk",
    description = ("Easy sequence alignment plots"),
    long_description=io.open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    license = "GPL",
    packages=["shabam"],
    install_requires=['pysam >= 0.9.0',
                      'pycairo >= 1.11.0',
    ],
    entry_points={'console_scripts': ['shabam = shabam.__main__:main']},
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    python_requires=">=3.6",
    test_suite="tests",
    tests_require=['Pillow >= 4.0',
    ]
)
