---
title: Compilers and the modern art of Web Development
date: 2016-05-04
tags: web development, javascript, compilers
slug: compilers-and-the-modern-art-of-web-development
---

With the only exception of people living in a cave, we already know everything is JavaScript now, fluid web ui, server side applications, native mobile applications and even desktop applications, everything is JavaScript... Now we talk about _components_ when developing user interfaces for the web, now we talk about ES2015 and beyond, people mention on the streets about [Babel](http://babeljs.io) to compile your [EcmaScript](https://babeljs.io/docs/learn-es2015/) (this may be an exaggeration, but I wish people talk about that on the streets), some other scholars are debating about different loaders and no doubt [Webpack](https://webpack.github.io/) is the default linker for the web... Wait a minute? compilers? loaders? linkers? we are talking about JavaScript, right? That thing that runs in the browser? right? why are you mentioning compilers? and even more obscure things like linkers and loaders? man, you have been drinking again...

A few years ago I gave a few talks about linkers and loaders, later I talked about symbols and compilers (maybe one day I will try to talk about lexers and parser, dreams...) and most of the people in the room asked me what all of this have to do with web development, well, I will try to do a comparison of those _low level things_ from the point of view of modern web development.

As a few of you already may know, there are a few languages out there which 'compile' code into JavaScript ([TypeScript](http://www.typescriptlang.org), [Dart](http://www.dartlang.org), [Elm](http://elm-lang.org), [PureScript](http://www.purescript.org) to name a few) in fact, that type of compiler is usually named [transpilers](https://en.wikipedia.org/wiki/Source-to-source_compiler) and are not different from the native compilers we already know, basically
converting JavaScript 5 into our assembly language. Do you want to know how this works? well, the [Babel documentation](https://github.com/thejameskyle/babel-handbook/blob/master/translations/en/README.md) has a lot of information about that.

The point is, our browsers only know about JavaScript 5, so, if you want to debug your code, you need a way to navigate from the generated compacted code to your original code, this is where our friend [Source Maps](http://www.html5rocks.com/en/tutorials/developertools/sourcemaps/) help, they are not different from Symbol files (the famous [PDB files](http://www.wintellect.com/devcenter/jrobbins/pdb-files-what-every-developer-must-know) in Windows development) and we should care in the same way for source map files. Generate them, keep them in a safe place, version them, give them some love. Source maps are your friends.

I really love the subject of linkers and loaders, if you want to know more I can highly recommend John R. Levine's book [Linkers and Loaders](http://linker.iecc.com/) (great book by the way, go buy it and read it). I prefer to think that Webpack is our _linker_ and the code it injects to load the dependencies is our _loader_ (using AMD or CommonJS, or whatever is the new kid on the block). This is where I see that [Browserify](http://browserify.org/) is more of a loader and Webpack more of a linker...

In conclusion: yes, it is true, JavaScript 5 is our new assembler language and the browser our new virtual machine. Maybe soon our university  professors will start using them to teach compilers theory...

**PS:** I am pretty sure my grammar in this blog post is awful, sorry, I wrote it in a rush.
