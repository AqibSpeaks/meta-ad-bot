from setuptools import setup, find_packages

setup(
    name="meta-ad-bot",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'streamlit==1.28.0',
        'sqlalchemy==2.0.0',
        'pandas==2.0.0',
    ],
)
