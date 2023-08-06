import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.core
__jsii_assembly__ = jsii.JSIIAssembly.load("@stormreply/cdk-openapi", "0.0.3", __name__, "cdk-openapi@0.0.3.jsii.tgz")
class OpenAPI(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@stormreply/cdk-openapi.OpenAPI"):
    """Installs an endpoint in your stack that allows users to view the contents of a DynamoDB table through their browser."""
    def __init__(self, parent: aws_cdk.core.Construct, id: str, *, api: str) -> None:
        """
        :param parent: -
        :param id: -
        :param props: -
        :param api: The api yaml file to parse.
        """
        props = OpenAPIProps(api=api)

        jsii.create(OpenAPI, self, [parent, id, props])


@jsii.data_type(jsii_type="@stormreply/cdk-openapi.OpenAPIProps", jsii_struct_bases=[], name_mapping={'api': 'api'})
class OpenAPIProps():
    def __init__(self, *, api: str):
        """
        :param api: The api yaml file to parse.
        """
        self._values = {
            'api': api,
        }

    @property
    def api(self) -> str:
        """The api yaml file to parse."""
        return self._values.get('api')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'OpenAPIProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = ["OpenAPI", "OpenAPIProps", "__jsii_assembly__"]

publication.publish()
