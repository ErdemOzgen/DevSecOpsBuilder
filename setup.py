import subprocess
from setuptools import setup, find_packages
from setuptools.command.install import install as InstallCommand

# Define a custom installation command to execute Makefile commands
class CustomInstallCommand(InstallCommand):
    def run(self):
        targets = ['setup', 'lab', 'outputs']  # Replace with the targets from your Makefile
        for target in targets:
            subprocess.check_call(['sudo', 'make', target])
        InstallCommand.run(self)

setup(
    name='devsecopsbuilder',  # Replace with your package name
    version='1.0.0',  # Replace with your package version
    packages=find_packages(),  # Automatically discover packages and sub-packages
    install_requires=[
        'pyYAML==6.0.1',
        'networkx==3.2.1',
        'matplotlib==3.8.2',
    ],
    # Other metadata like author, description, license, etc.
    # ...
    # Specify the custom install command
    cmdclass={
        'install': CustomInstallCommand,
    }
)
