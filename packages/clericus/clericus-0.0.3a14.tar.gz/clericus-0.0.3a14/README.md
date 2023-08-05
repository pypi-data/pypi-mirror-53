# Clericus

Clericus is an asynchronous webserver (wrapping aiohttp) which tries to abstract away the boring parts of writing a webserver by making parsing request, serializing data, and generating documentation build in.

## Getting Started

### Prerequisites

Clericus requires Python 3.7.

### Installing

Clericus is on pypi, but is still in alpha, so your mileage may vary.  Install the latest alpha release (which is probably a different version by now) like so:

```
$ pip install clericus==0.0.3a4
```

## Running the tests

Tests are built with unittest and can be run via:

```
$ python -m unittest 
```

Add the `-v` flag if you want more verbosity.


## Usage

The following code sets up and runs a simple webserver:

```python
from clericus import Clericus, Endpoint, newMethod
from clericus.parsing.fields import StringField, IntegerField


class ExampleEchoEndpoint(Endpoint):
    """
    String Echoing
    """

    async def echo(self, phrase, times):
        return {"echo": phrase * times}

    Get = newMethod(
        httpMethod="GET",
        description="Echo the string given in the query",
        process=echo,
        queryParameters={
            "phrase": StringField(
                description="A string to echo some number of times"
            ),
            "times": IntegerField(
                description="The number of times to repeat the given string",
                optional=True,
                default=1,
            )
        },
        responseFields={
            "echo": StringField(),
        }
    )


server = Clericus()
server.addEndpoint("/echo/", ExampleEchoEndpoint, name="Echo Example")

server.runApp()
```

With the webserver running, in another tab do:

```
$ curl 'localhost:8080/echo/?phrase=hello-world&times=3'
{"echo": "hello-worldhello-worldhello-world"}
```

Because the `times` parameter is optional, it can be omitted and the configured default will be used.

```
$ curl 'localhost:8080/echo/?phrase=hello-world'
{"echo": "hello-world"}
```

Leaving out the required `phrase` parameter will cause the server to respond with an automatically generated error:

```
$ curl 'localhost:8080/echo/'
{"errors": [{"message": "Missing required field: phrase"}]}
```

Clericus also handles documentation based on your configuration, so any endpoint you add also adds another `documentation` endpoint like so (JSON expanded for clarity):

```
$ curl 'localhost:8080/documentation/echo/'
{
    "description": "String Echoing",
    "name": "Echo Example",
    "path": "/echo/",
    "methods": {
        "get": {
            "description": "Echo the string given in the query",
            "request": {
                "query": {
                    "phrase": {
                        "allowedTypes": [
                            "string"
                        ],
                        "optional": false,
                        "default": null,
                        "description": "A string to echo some number of times"
                    },
                    "times": {
                        "allowedTypes": [
                            "int"
                        ],
                        "optional": true,
                        "default": 1,
                        "description": "The number of times to repeat the given string"
                    }
                }
            },
            "response": {
                "body": {
                    "echo": {
                        "allowedTypes": [
                            "string"
                        ],
                        "optional": false,
                        "default": null,
                        "description": ""
                    }
                }
            }
        },
        "options": {
            "description": null,
            "request": {},
            "response": {
                "body": {}
            }
        }
    }
}
```


Clericus also assumes the root path should be the documentation for your API, so you can do the following to see all endpoints (currently some authentication methods are always included, I plan to factor these out later...)

```
$ curl 'localhost:8080/'
{
    "endpoints": [
        {
            "description": "String Echoing",
            "name": "Echo Example",
            "path": "/echo/",
            "methods": {
                "get": {
                    "description": "Echo the string given in the query",
                    "request": {
                        "query": {
                            "phrase": {
                                "allowedTypes": [
                                    "string"
                                ],
                                "optional": false,
                                "default": null,
                                "description": "A string to echo some number of times"
                            },
                            "times": {
                                "allowedTypes": [
                                    "int"
                                ],
                                "optional": true,
                                "default": 1,
                                "description": "The number of times to repeat the given string"
                            }
                        }
                    },
                    "response": {
                        "body": {
                            "echo": {
                                "allowedTypes": [
                                    "string"
                                ],
                                "optional": false,
                                "default": null,
                                "description": ""
                            }
                        }
                    }
                },
                "options": {
                    "description": null,
                    "request": {},
                    "response": {
                        "body": {}
                    }
                }
            }
        },
        {
            "description": "Return the status of the server",
            "path": "/healthy/",
            "methods": {
                "get": {
                    "description": "Return the status of the server",
                    "request": {},
                    "response": {
                        "body": {
                            "healthy": {
                                "allowedTypes": [],
                                "optional": false,
                                "default": true,
                                "description": "A boolean of whether the server is healthy"
                            }
                        }
                    }
                },
                "options": {
                    "description": null,
                    "request": {},
                    "response": {
                        "body": {}
                    }
                }
            }
        },
        ...
    ]
}
```

Clericus also handles `OPTIONS` requests based on your definitions, so:

```
$ curl -X OPTIONS localhost:8080/echo/ -v
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 8080 (#0)
> OPTIONS /echo/ HTTP/1.1
> Host: localhost:8080
> User-Agent: curl/7.58.0
> Accept: */*
> 
< HTTP/1.1 200 OK
< Allow: GET, OPTIONS
< Access-Control-Request-Method: GET, OPTIONS
< Content-Type: application/json; charset=utf-8
< Access-Control-Allow-Credentials: true
< Access-Control-Allow-Origin: http://localhost:3000
< Content-Length: 2
< Date: Tue, 18 Jun 2019 01:23:23 GMT
< Server: Python/3.7 aiohttp/3.5.4
< 
* Connection #0 to host localhost left intact
```

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/MrIncredibuell/clerius/tags). 

## Authors

* **Joseph Buell** - *Initial work* - [MrIncredibuell](https://github.com/MrIncredibuell)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


