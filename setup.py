from setuptools import setup, find_packages

setup(
    name="payment-gateway",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "sqlalchemy>=1.4.0",
        "psycopg2-binary>=2.9.0",
        "pydantic>=1.8.0",
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.4",
        "python-multipart>=0.0.5",
        "python-dotenv>=0.19.0",
        "httpx>=0.19.0",
        "celery>=5.1.0",
        "alembic>=1.7.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-asyncio>=0.15.0",
            "black>=21.0",
            "isort>=5.0.0",
            "mypy>=0.910",
        ],
    },
    python_requires=">=3.8",
    author="Your Name",
    author_email="your.email@example.com",
    description="A secure payment gateway system with SSLCommerz and PayPal integration",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/payment-gateway",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
