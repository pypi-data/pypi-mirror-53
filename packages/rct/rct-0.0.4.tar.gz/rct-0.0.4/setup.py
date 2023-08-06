import setuptools

with open("rct/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rct",
    version="0.0.4",
    author="Sylvain Chassang",
    author_email="sylvain.chassang@gmail.com",
    description="design robust balanced randomized experiments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sylvaingchassang/rct",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={'rct': ['tests/test_data/*', 'notebooks/*']},
    install_requires=[
        'pandas>=0.25.1',
        'numpy>=1.17.2',
        'statsmodels>=0.10.1',
        'parameterized>=0.7.0',
        'lazy-property>=0.0.1',
    ],
    keywords='experiment-design RCTs A/B-testing',
    python_requires='>=3.6',
)
