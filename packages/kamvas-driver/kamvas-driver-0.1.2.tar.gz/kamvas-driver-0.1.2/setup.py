import setuptools
import os.path

long_description = ''
if os.path.isfile("README.md"):
    with open("README.md", "r") as fh:
        long_description = fh.read()

setuptools.setup(
    name="kamvas-driver", version="0.1.2",
    author="Mantaseus",
    description = 'A Linux userland driver for Huion Kamvas Pro devices',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url = 'https://github.com/Mantaseus/Huion_Kamvas_linux.git',
    license = 'MIT',

    packages = ['driver'],
    package_data={'driver': ['config.yaml']},
    entry_points = {
        'console_scripts': [
            'kamvas = driver.cli:run_main',
        ]
    },

    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires = [
        'docopt',
        'tabulate',
        'pyusb',
        'evdev',
        'pyyaml',
        'psutil',
        'elevate',
        'pyudev',
    ],
)
