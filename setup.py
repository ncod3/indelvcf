import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="indelvcf",
    version="0.0.1",
    author="satoshi-natsume",
    author_email="s-natsume@ibrc.or.jp",
    description="Indelvcf",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ncod3/indelvcf",
    packages=setuptools.find_packages(),
    license='GPL',
    entry_points = {
        'console_scripts': ['indelvcf = indelvcf.main:main']
    },
    python_requires='>=3.7',
)
