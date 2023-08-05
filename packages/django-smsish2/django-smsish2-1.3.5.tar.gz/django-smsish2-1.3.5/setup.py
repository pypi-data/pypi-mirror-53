import os
from setuptools import setup, find_packages

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="django-smsish2",
    version="1.3.5",
    packages=find_packages(),
    include_package_data=True,
    license="MIT",
    description="A simple Django app to send SMS messages using an API similar to that of django.core.mail.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/o3o3o/django-smsish",
    author="Ryan Balfanz",
    author_email="ryan@ryanbalfanz.net",
    classifiers=[
        "Development Status :: 4 - Beta",
        # 'Development Status :: 5 - Production/Stable',
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 1.8",
        "Framework :: Django :: 1.9",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Topic :: Communications",
        "Topic :: Communications :: Telephony",
    ],
)
