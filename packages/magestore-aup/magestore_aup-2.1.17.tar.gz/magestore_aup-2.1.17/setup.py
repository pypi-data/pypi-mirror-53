import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

package_name = 'magestore_aup'
packages = setuptools.find_packages(
    include=[package_name, "{}.*".format(package_name)]
)

setuptools.setup(
    name=package_name,
    version="2.1.17",
    author="Mars",
    author_email="mars@trueplus.vn",
    description="Get package info when latest package building process not done yet",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://magestore.com",
    packages=packages,
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3',
    install_requires=[
        'cryptography>=2.5',
        'fabric',
        'requests',
        'packaging'
    ],
    include_package_data=True
)
