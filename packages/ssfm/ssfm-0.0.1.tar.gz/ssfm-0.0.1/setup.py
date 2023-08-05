import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ssfm",
    version="0.0.1",
    author="Lykos94",
    scripts=['ssfm',],
    author_email="lukaszmoskwa94@gmail.com",
    description="Curses based File Manager application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Lykos94/ssfm",
    packages=[
        'ssfm_modules',
        'ssfm_modules.core',
        'ssfm_modules.draw',
        'ssfm_modules.extensions',
        'ssfm_modules.extensions.window_extension',
        'ssfm_modules.extensions.git_extension',
        'ssfm_modules.extensions.file_extension',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Unix"
    ],
    python_requires='>=3.6',
)
