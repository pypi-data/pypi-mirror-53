import setuptools
from MsCoppel import version

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MsCoppel",
    version=version,
    author="Enoi Barrera Guzman",
    author_email="zafiro3000x@gmail.com",
    description="Libreria para microservicios basados en mensajes desdes de una cola de mensajes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    install_requires=['kafka-python==1.4.6', 'Logbook', 'asyncio-nats-client==0.9.2', 'jaeger-client==4.1.0', 'fluent-logger==0.9.3']
)
