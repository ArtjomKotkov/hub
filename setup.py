from setuptools import setup, find_packages


setup(
    name='akohub_backend',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'anyio==3.6.2',
        'certifi==2022.12.7',
        'charset-normalizer==3.1.0',
        'click==8.1.3',
        'colorama==0.4.6',
        'dependency-injector==4.41.0',
        'dnspython==2.3.0',
        'email-validator==1.3.1',
        'fastapi==0.94.1',
        'greenlet==2.0.2',
        'h11==0.14.0',
        'httpcore==0.16.3',
        'httptools==0.5.0',
        'httpx==0.23.3',
        'idna==3.4',
        'itsdangerous==2.1.2',
        'Jinja2==3.1.2',
        'MarkupSafe==2.1.2',
        'orjson==3.8.7',
        'pydantic==1.10.6',
        'PyJWT==2.6.0',
        'python-configuration==0.8.2',
        'python-dotenv==1.0.0',
        'python-multipart==0.0.6',
        'PyYAML==5.4.1',
        'requests==2.28.2',
        'rfc3986==1.5.0',
        'six==1.16.0',
        'sniffio==1.3.0',
        'SQLAlchemy==2.0.5.post1',
        'starlette==0.26.1',
        'toml==0.10.2',
        'typing_extensions==4.5.0',
        'ujson==5.7.0',
        'urllib3==1.26.15',
        'uvicorn==0.21.1',
        "watchfiles==0.18.1",
        "websockets==10.4",

        #local-dependencies
        'modeller==1.0.0',
        'errors==0.0.1',
        'pbac==1.0.1',
    ],
    python_requires='>=3.11',
    entry_points={
        'console_scripts': [
            'run-akotaru-backend = backend.server:main',
        ]
    }
)
