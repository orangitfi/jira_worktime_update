from setuptools import setup, find_packages

setup(
    name="jira_work_update",  # Package name
    version="0.1.0",
    description="A CLI tool to log work time to Jira issues.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/agileday",  # Replace with your project URL
    packages=find_packages(),  # Automatically find and include all packages in the project
    entry_points={
        "console_scripts": [
            "jira_work_update=jira_wowk_update.__main__:main",  # CLI command, entry point to main function
        ]
    },
    install_requires=[
        "jira",  # Dependency for interacting with the Jira API
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-mock",
            "coverage",  # Optional dependencies for development/testing
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
