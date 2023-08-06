import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sequdas-client",
    version="1.0.0",
    author="Jun Duan",
    author_email="jun.duan@bccdc.ca",
    description="SeqUDAS: Sequence Upload and Data Archiving System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/duanjunhyq/sequdas",
    packages=setuptools.find_packages(include=['sequdas_client','sequdas_client.Lib']),
    install_requires=['configparser','mysql-connector-python','pytz','ntplib','validate_email'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data = True,
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'sequdas_client=sequdas_client.sequdas_client:main',
        ],
    },
)