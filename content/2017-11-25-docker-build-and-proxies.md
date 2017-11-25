---
title: Docker build and proxies
date: 2017-11-25
slug: docker-build-and-proxies
tags: docker, build, python, alpine
---
I remember the first time I saw a presentation about [Docker](http://docker.com/), it was probably in 2014 and it was love at first sigh. My day to day workflow has changed drastically since then, instead of installing servers on my laptop (for example, a database server for testing) or dealing with a virtual machine I just spin up a new container image and it is done. Instead of testing my application in my machine I put it in an image container and test it there.

Recently I had a not very common problem with images, it was taking a lot of time to build the image from scratch because the shared internet connection was too slow, why not use a proxy to cache the dependencies locally and just reuse them in next images? This sounds easy, but I found it was trickier than expected.

The first step is caching the docker image. Every time you use an image in a `pull` or `build` the docker daemon will keep the image locally. We can check this easily:

```
docker pull alpine:latest
docker images
```

The first command will check if you already have the image locally, if not it will download the image and keep it. Because almost all my custom docker images use Alpine Linux this part of the "cache" is already done, thanks docker daemon!

Now, lets see how my [Dockerfile'(https://docs.docker.com/engine/reference/builder/) looks like:

```docker
FROM alpine:latest
LABEL mantainer "me@cprieto.com"

RUN apk update && apk upgrade \
    && apk --no-cache add python3 python3-dev build-base freetype-dev \
    && apk --no-cache add libxml2 libxml2-dev libxslt libxslt-dev \
    && apk --no-cache add jpeg jpeg-dev zlib zlib-dev \
    && apk --no-cache add lapack lapack-dev gfortran \
    && pip3 install jupyter
```

This will download over 300MB that will be downloaded again if you build a similar image. Let's put a proxy in front of it, you can use any proxy or in my case, I wrote my own simple proxy in Python:

```py
import BaseHTTPServer
import hashlib
import os
import urllib2
import socket

CACHE_DIR = os.path.abspath('./cache')

class CacheHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        m = hashlib.md5()
        m.update(self.path)
        cache_filename = os.path.join(CACHE_DIR, m.hexdigest() + ".cached")

        if os.path.exists(cache_filename):
          print "Cache hit"
          data = open(cache_filename).readlines()
        else:
          print "Cache miss"
          data = urllib2.urlopen(self.path).readlines()
          open(cache_filename, 'wb').writelines(data)
        self.send_response(200)
        self.end_headers()
        self.wfile.writelines(data)

def run():
    server_address = ('0.0.0.0', 8899)
    httpd = BaseHTTPServer.HTTPServer(server_address, CacheHandler)
    httpd.serve_forever()

if __name__ == '__main__':
    if not os.path.isdir(CACHE_DIR):
      os.makedirs(CACHE_DIR)

    run()
```

Now we just run this proxy with:

```
python proxy.py
```

How do we tell to our docker image to use this proxy for `apk `, the easy way is using the environment variable `HTTP_PROXY`, I know your first instinct is to put that variable in the `ENV` statement, but let's do something different, let's use the `ARG` parameter, now your Dockerfile will look like this:

```docker
FROM alpine:latest
LABEL mantainer "me@cprieto.com"

ARG HTTP_PROXY

RUN apk update && apk upgrade \
    && apk --no-cache add python3 python3-dev build-base freetype-dev \
    && apk --no-cache add libxml2 libxml2-dev libxslt libxslt-dev \
    && apk --no-cache add jpeg jpeg-dev zlib zlib-dev \
    && apk --no-cache add lapack lapack-dev gfortran \
    && pip3 install jupyter
```

Let's build the image with the following command:

```
docker build --build-args HTTP_PROXY=http://192.168.0.1:8899 -t cprieto/jupyter-python3
```

Notice we use _our machine IP_ and not _localhost_, this is because inside the docker container localhost is its own localhost!

You will see your new image will use the cache, and the next time you build the image with the same parameters (for example, `apk add python3`) it will serve the package from your local disk and not from the internet ;)

Now we have a new problem, `pip`. [Pip](https://pip.pypa.io/en/stable/) is the package manager for Python (in fact, it is just one package manager, the other famous one is [Pipenv](https://docs.pipenv.org/)) and it will go direct to pypa to grab the packages. There is an easy way to cache pip packages, using a pip proxy.

Let's install and run a pip proxy:

```
pip install devpip-server
devpip-server --start --init --host 0.0.0.0
```
This will install [devpip-server](https://devpi.net/docs/devpi/devpi/stable/%2Bd/index.html), initialize it and store its data in a cache directory (usually in ~/.devpip). It is important to pass the option `--host 0.0.0.0` because by default it listen to localhost only.

By default the index server for the pip proxy is `http://localhost:3141/root/pypi/+simple/`

We have to tell our pip inside the container to use that pip proxy, we have to set up _two environment variables_:

```docker
FROM alpine:latest
LABEL mantainer "me@cprieto.com"

ARG HTTP_PROXY
ARG PIP_TRUSTED_HOST
ARG PIP_INDEX_URL

RUN apk update && apk upgrade \
    && apk --no-cache add python3 python3-dev build-base freetype-dev \
    && apk --no-cache add libxml2 libxml2-dev libxslt libxslt-dev \
    && apk --no-cache add jpeg jpeg-dev zlib zlib-dev \
    && apk --no-cache add lapack lapack-dev gfortran \
    && pip3 install jupyter
```

We can run the build command now:

```
docker build \
  --build-args HTTP_PROXY=http://192.168.0.1:8899 \
  --build-args PIP_TRUSTED_HOST=192.168.0.1 \
  --build-args PIP_INDEX_URL=http://192.168.0.1:3141/root/pypi/+simple/ \
  -t cprieto/jupyter-python3
```

If you try to build the image it will kind of work, but you will get this error message:

```
Could not find a version that satisfies the requirement jupyter (from versions: )
No matching distribution found for jupyter
```

This happens because pip is trying to look at our proxy (the custom made proxy) and it cannot find it. Maybe if you use another proxy (like TinyProxy) you won't have such issue, but well...

The easy way to solve this is using another environment variable. Internally pip uses the [requests]() library, and this library can skip the use of a proxy (already set up using the `HTTP_PROXY` environment variable) if we set the environment variable `no_proxy` with a list of ips or domains to skip proxy resolution. Let's do that (notice it is in lowecase `no_proxy`):

```docker
FROM alpine:latest
LABEL mantainer "me@cprieto.com"

ARG HTTP_PROXY
ARG PIP_TRUSTED_HOST
ARG PIP_INDEX_URL
ARG no_proxy

RUN apk update && apk upgrade \
    && apk --no-cache add python3 python3-dev build-base freetype-dev \
    && apk --no-cache add libxml2 libxml2-dev libxslt libxslt-dev \
    && apk --no-cache add jpeg jpeg-dev zlib zlib-dev \
    && apk --no-cache add lapack lapack-dev gfortran \
    && pip3 install jupyter
```

Now the complete command to build the image is:

```
docker build \
  --build-args HTTP_PROXY=http://192.168.0.1:8899 \
  --build-args PIP_TRUSTED_HOST=192.168.0.1 \
  --build-args PIP_INDEX_URL=http://192.168.0.1:3141/root/pypi/+simple/ \
  --build-args no_proxy=192.168.0.1 \
  -t cprieto/jupyter-python3
```

Done! now I can keep a local cache with pip packages, docker images (from pull) and [Alpine Linux](https://alpinelinux.org/) packages :) [well, or get a faster connection that is]
