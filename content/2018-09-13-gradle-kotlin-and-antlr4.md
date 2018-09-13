title: Gradle, Kotlin and ANTLR4
date: 2018-09-13
tags: programming, compilers, kotlin
---
I remember read and learning ANTLR4 with the excelent book [The definitive ANTLR4 reference](https://pragprog.com/book/tpantlr2/the-definitive-antlr-4-reference) by Terence Parr, it is a good book, I highly recommend it. Well, I recently wanted to read the book again and decided to do the examples with Gradle and Kotlin and while searching in the web I found a lot of different answers and tips for writing the build file, so I was like "what is the smallest gradle build I can make for this"? so I decided to write this in case somebody ask the same question or future Cristian forgets how to do it.

Well, Gradle requires a specific project layout, so let's do that:

```
.
├── build.gradle
└── src
    └── main
	    ├── antlr
        └── kotlin

4 directories, 1 file
```

Easy, in `src/main/antlr` will be our ANTLR grammars and in `src/main/kotlin` _our_ implementation for ANTLR listeners or visitors. Let's create the smallest `build.gradle` possible for this layout:

```groovy
plugins {
  id 'antlr'
  id 'org.jetbrains.kotlin.jvm' version '1.2.61'
}

repositories {
  mavenCentral()
}

dependencies {
  antlr 'org.antlr:antlr4:4.7.1'
}
```

We are using Gradle plugin DSL notation and the [Kotlin Gradle plugin](https://kotlinlang.org/docs/reference/using-gradle.html) with the included [ANTLR plugin](https://docs.gradle.org/current/userguide/antlr_plugin.html), see? nothing fancy.

When building, Gradle will generate java sources with the Lexers/Parsers and place them in a generated sources directory, I had seen a lot of post out there with scripts moving the generated sources or putting them in fancy directories, nah, we don't want that, we want something super simple, so let's go with the defaults.

Let's generate a simple grammar and tell to use a specific package for it as well:

```antlr
grammar Hello;

@header {
package com.cprieto.sample;
}

hello: 'hello' ID ;
ID   : [a-zA-Z]+ ;
WS   : [ \r\n\t]+ -> skip ;
```

Remember to save it in `src/main/antlr/com/cprieto/sample/Hello.g4`, We are using a package and we need to place the grammar file in the same layout we will put our source code.

Ok, as a simple matter of test, let's create a simple Listener for our parser:

```kotlin
package com.cprieto.sample

class SampleListener: HelloBaseListener() {
}
```
It is so simple it does nothing! but hey, it is a start! This needs to be saved in the expected Kotlin source set: `src/main/kotlin/com/cprieto/sample/SampleListener.kt`

If we try to compile, guess what, it will fail! This is because our Kotlin source cannot find the generated source files from the grammar by ANTLR, remember, the ANTLR plugin _knows_ about the Java plugin but not about any other plugin, so we have to manually solve that, just add a line to your Gradle file:

```groovy hl_lines="14"
plugins {
  id 'antlr'
  id 'org.jetbrains.kotlin.jvm' version '1.2.61'
}

repositories {
  mavenCentral()
}

dependencies {
  antlr 'org.antlr:antlr4:4.7.1'
}

compileKotlin.dependsOn generateGrammarSource
```

Done! this is the simples gradle build file for Kotlin, it is short and concise, of course if you have more dependencies or need you can grow from there.


