import json
import setuptools

kwargs = json.loads("""
{
    "name": "stormreply.cdk-openapi",
    "version": "0.0.2",
    "description": "@stormreply/cdk-openapi",
    "url": "https://github.com/stormreply/cdk-openapi.git",
    "long_description_content_type": "text/markdown",
    "author": "Henning Teek<h.teek@reply.com>",
    "project_urls": {
        "Source": "https://github.com/stormreply/cdk-openapi.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "stormreply.cdk_openapi",
        "stormreply.cdk_openapi._jsii"
    ],
    "package_data": {
        "stormreply.cdk_openapi._jsii": [
            "cdk-openapi@0.0.2.jsii.tgz"
        ],
        "stormreply.cdk_openapi": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii~=0.17.0",
        "publication>=0.0.3",
        "aws-cdk.core~=1.9,>=1.9.0"
    ]
}
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
