from setuptools import setup, find_packages

setup(
    name="pizza_review_system",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "fastapi",
        "uvicorn",
        "streamlit",
        "plotly",
        "langchain",
        "chromadb",
        "beautifulsoup4",
        "requests",
        "python-dotenv",
        "pydantic>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest",
            "black",
            "flake8",
            "jupyter",
            "ipykernel",
        ],
    },
    author="Amittai lerer",
    description="A comprehensive pizza review analysis system",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
) 