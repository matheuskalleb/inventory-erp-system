from setuptools import setup, find_packages

setup(
    name="inventory-erp-system",
    version="0.1.0",
    description="Sistema de gestão de estoque com simulação de processos ERP",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/seu-usuario/inventory-erp-system",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "pydantic>=2.5.0",
        "pandas>=2.1.0",
        "numpy>=1.26.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.12.0",
            "flake8>=6.1.0",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Business",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
