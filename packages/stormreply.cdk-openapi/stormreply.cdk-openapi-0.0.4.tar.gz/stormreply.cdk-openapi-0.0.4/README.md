# cdk-openapi

An AWS CDK construct which generates API Gateway exposed Lambda functions
from an OpenAPI specification in your stack.

## Usage

### JavaScript

Install via npm:

```shell
$ npm i @stormreply/cdk-openapi
```

Add to your CDK stack:

```ts
import { OpenAPI, OpenAPIProps } from '@stormreply/cdk-openapi'

const api = new OpenAPI(this, 'SampleAPI', {
  api: 'api.yaml'
});
```

### Python

Install via pip:

```shell
$ pip install stormreply.cdk-openapi
```

Add to your CDK stack:

```python
from stormreply.cdk_openapi import (
    OpenAPI,
    OpenAPIProps,
)

api = OpenAPI(
    self, "SampleAPI", {
      api='api.yaml'
    }
)
```

## License

Apache 2.0
