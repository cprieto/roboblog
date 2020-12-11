---
title: Using Visual Studio Code as your LaTeX environment
date: 2020-11-12
slug: using-visual-studio-code-as-your-latex-environment
tags: misc, til
---

[LaTeX](https://www.latex-project.org/) is one of those things you are sort of forced to learn when preparing technical documents, especially for academia. It is an old (but highly effective) typesetting system, and it is, at its core, complex as hell to use.

In my day to day I jump between plaforms and operating systems so I always dreamed with a LaTeX editor that _rule them all_, sadly I had not found such thing (yet) but the closest has been, so far, [Visual Studio Code](https://code.visualstudio.com/) so I took some time to prepare an environment and ensure I can work in the same document in the same way in any platform and, well, document the experience.

First we need to install the fantastic [LaTeX Workshop](https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop), a Visual Studio Code extension designed to make your life with LaTeX easier (of course you need to have VS Code installed first). Now there is the big question, what about LaTeX? well, we have plenty of options, yes, you need to decide what [LaTeX distribution](https://www.latex-project.org/get/#tex-distributions) to install and run in each of your operating systems and platforms, this is where I have most of my problems in the past, mostly because I got into a point where my installation was corrupted in macOS and I cannot compile Tex documents. Another problem I would like to avoid is to have _global applications_ in my operating system; for example, I use [minted](https://ctan.org/pkg/minted?lang=en) a lot and this requires [Pygments](https://pygments.org/) to be installed in your system, because this is a Python library I would prefer if it is installed in a [virtual environment](https://docs.python.org/3/tutorial/venv.html) and all of that... As you see it could be daunting and I wanted to have a single and unique way to do it.

## Containers to the rescue

If there were a way to isolate (and distribute) a process from all the rest of your processes... Wait a minute, such thing exists! It is called [Docker](https://www.docker.com/)! What if I use a container with all the dependencies I need to do the typesetting of a document in a container and just use it to compile the document and simple reuse the container all over again!

Visual Studio Code has an extension for this, [Remote Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers), I just need to configure it to do what I need and make it work with LaTeX Workshop. This was a lot simpler than I thought but it required a few steps, especially for those that never used the extension before.

First, after installed the mentioned extension, we need to create a folder, `.devcontainer` in the directory where our document project is located, this directory with its content _needs to be version controlled_ if you want to share your experience, it behaves pretty much like your _settings_ for the project. Inside this directory we have to create a [Dockerfile](https://docs.docker.com/engine/reference/builder/) with the instructions to assemble our LaTeX container with our requirements, in my case it is very simple:

```dockerfile
FROM ubuntu

RUN apt update && DEBIAN_FRONTEND=noninteractive apt install --no-install-recommends -y \
        python3 python3-pip texlive texlive-extra-utils texlive-base git \
        latexmk texlive-xetex texlive-pstricks texlive-science texlive-publishers \
    && pip3 install pygments \
    && rm -rf /var/cache/apt/*
```

Feel free to change it to whatever you want to include in your LaTeX distribution, I prefer not to use `texlive-full` because, well, it will require to install 2GB of packages and I don't need them all (yet).

Now that we have the instructions to assemble our container I build it locally _to avoid delay when running the whole process_:

```console
$ docker build -t cprieto/latex .
```

Feel free to use whatever name you want for your image.

Now we create another file, `devcontainer.json` with the instructions of how to use a container for our project root:

```json
{
  "name": "LaTeX",
  "extensions": [
    "james-yu.latex-workshop"
  ],
  "dockerFile": "Dockerfile",
  "image": "cprieto/latex",
  "forwardPorts": [
    36887
  ]
}
```

The `dockerFile` and `image` tell to VSCode to use the image we already built, if this image does not exists it will build it from scratch (and this will probably take some time). We tell it to automatically install the LaTeX Workshop extension in this container (if not, later VSCode will ask us if we want to install it or not) and opening the port 36887 from the container, we need to do this to enable the native preview used by the extension.

And this is all! When we open the directory with our LaTeX project VSCode will just ask us if we want to do this in the container, just follow the prompts and it will be set, our project will be compiled with our container and generate our document, if you need something else installed just do it in the container image instead of your machine.
