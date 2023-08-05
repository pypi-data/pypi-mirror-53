from setuptools import setup
import setuptools

setup(
        name='gxdltk',
        version='0.1-alpha-3',
        description="DeepLearning Toolkit",
        author='gawainx',
        author_email='liangyixp@live.cn',
        # packages=['gx-toml'],
        install_requires=['numpy','torch'],
        classifiers=[
            "Programming Language :: Python :: 3.7",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        packages=setuptools.find_packages(),
)
