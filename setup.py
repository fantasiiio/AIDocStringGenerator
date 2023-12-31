from setuptools import setup, find_packages

setup(
    name='AIDocStringGenerator',
    version='1.0',
    packages=find_packages(),
    description='AIDocStringGenerator is an automated tool that utilizes AI technologies like Anthropic and OpenAI GPT-3.5 to generate and manage docstrings in Python code. It streamlines documentation by processing both single files and entire directories, offering customizable settings for docstring verbosity and style. This tool is ideal for enhancing code readability and maintainability in Python projects.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Francois Girard',
    author_email='fantasiiio@hotmail.com',
    url='https://github.com/fantasiiio/AIDocStringGenerator',
    install_requires=[
        'AIDocStringGenerator',
        "annotated-types==0.6.0",
        "anyio==4.2.0",
        "cachetools==5.3.2",
        "certifi==2023.11.17",
        "charset-normalizer==3.3.2",
        "colorama==0.4.6",
        "distro==1.9.0",
        "exceptiongroup==1.2.0",
        "google-ai-generativelanguage==0.4.0",
        "google-api-core==2.15.0",
        "google-auth==2.25.2",
        "google-generativeai==0.3.2",
        "googleapis-common-protos==1.62.0",
        "grpcio==1.60.0",
        "grpcio-status==1.60.0",
        "h11==0.14.0",
        "httpcore==1.0.2",
        "httpx==0.26.0",
        "idna==3.6",
        "iniconfig==2.0.0",
        "openai==1.6.1",
        "packaging==23.2",
        "pluggy==1.3.0",
        "proto-plus==1.23.0",
        "protobuf==4.25.1",
        "pyasn1==0.5.1",
        "pyasn1-modules==0.3.0",
        "pydantic==2.5.3",
        "pydantic-core==2.14.6",
        "pytest==7.4.4",
        "python-dotenv==1.0.0",
        "requests==2.31.0",
        "rsa==4.9",
        "sniffio==1.3.0",
        "tomli==2.0.1",
        "tqdm==4.66.1",
        "typing-extensions==4.9.0",
        "urllib3==2.1.0"
    ],    
    entry_points={
        'console_scripts': [
            'AIDocStringGenerator=AIDocStringGenerator.AIDocStringGenerator:main'
        ]
    }   
)