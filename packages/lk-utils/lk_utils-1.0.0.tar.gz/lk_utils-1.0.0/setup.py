from setuptools import setup, find_packages

# with open('readme/readme.md', 'r') as f:
#     desc = f.read()

# REF: https://packaging.python.org/tutorials/packaging-projects/

setup(
    name='lk_utils',
    version='1.0.0',
    packages=find_packages(),
    url='https://github.com/likianta',
    license='MIT License',
    author='Likianta',
    author_email='likianta@foxmail.com',
    description='Easy used for data processing.',
    python_requires='>=3.6'
)
