import setuptools

INSTALL_REQUIRES = [
    'pynwb',
    'hdmf',
    'nwb-docutils'
    'sphinx'
]
TESTS_REQUIRE = ['pytest >= 2.7.1']
DESCRIPTION = "Frank lab nwb specific extensions"

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="franklab_nwb_extensions",
    version="0.1.0.dev0",
    author="Frank Lab members",
    author_email="loren@phy.ucsf.edu",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LorenFrankLab/franklab_nwb_extensions",
    packages=setuptools.find_packages(),
    package_data={'franklab_nwb_extensions': ["*.yaml"]},
    install_requires=INSTALL_REQUIRES,
    python_requires='>=3.6',
    tests_require=TESTS_REQUIRE,
    entry_points='''
        [console_scripts]
        create_franklab_spec=franklab_nwb_extensions.create_franklab_spec:main
    ''',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
