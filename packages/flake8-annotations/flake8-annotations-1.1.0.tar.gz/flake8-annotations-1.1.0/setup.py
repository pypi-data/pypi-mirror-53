from setuptools import setup


setup(
    name="flake8-annotations",
    license="MIT",
    version="1.1.0",
    description="Flake8 Type Annotation Checks",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Python Discord",
    author_email="staff@pythondiscord.com",
    url="https://github.com/python-discord/flake8-annotations",
    packages=['flake8_annotations'],
    entry_points={
        "flake8.extension": [
            'TYP = flake8_annotations.checker:TypeHintChecker',
        ],
    },
    python_requires=">=3.6",
    zip_safe=True,
    classifiers=[
        "Framework :: Flake8",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
    project_urls={
        'Issue tracker': 'https://github.com/python-discord/flake8-annotations/issues',
        'Discord server': 'https://discord.gg/python',
    },
    install_requires=[
        "flake8~=3.7.8",
        "typed-ast~=1.4"
    ],
    extras_require={
        "dev": [
            "flake8-bugbear~=19.8",
            "flake8-docstrings~=1.4",
            "flake8-formatter-junit-xml~=0.0",
            "flake8-import-order~=0.18",
            "flake8-string-format~=0.2",
            "flake8-tidy-imports~=2.0",
            "flake8-todo~=0.7",
            "pre-commit~=1.18",
            "pytest~=5.1",
            "pytest-check~=0.3",
            "pytest-cov~=2.7",
        ]
    }
)
