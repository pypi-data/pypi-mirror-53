from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ccm_java8',
    version='0.1',
    packages=find_packages(),

    author="Adam Zegelin",
    author_email="adam@instaclustr.com",

    description="CCM extension that starts nodes under Java 1.8",
    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://github.com/instaclustr/ccm-java8",

    install_requires=['ccm'],

    entry_points={
        'ccm_extension': ['java_home = ccm_java8.java_home:register_extensions']
    },

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: MacOS X',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Database',
    ]
)