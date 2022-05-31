---
title: Gradle, Kotlin and ANTLR
date: 2022-05-24
slug: gradle-kotlin-and-antlr
tags: programming, building, antlr, gradle
---

This is one of those things I always do and somehow I forget about it next day, how to properly have a [Gradle](https://gradle.org/) build definition file with [Kotlin](https://kotlinlang.org/) and [ANTLR](https://www.antlr.org/)? Yes, ANTLR generates your parser and lexer skeleton and you want to write your specialized classes using them in Kotlin, all of that with a Gradle build file.

You will assume is easy, after all, there is a [Gradle plugin for ANTLR](https://docs.gradle.org/current/userguide/antlr_plugin.html), but for some reason is not _that_ transparent. Let's start with a simple grammar file (taken from the amazing [The Definitive ANTLR4 Reference](https://pragprog.com/titles/tpantlr2/the-definitive-antlr-4-reference/) book):

```antlr
grammar ArrayInit;

init: '{' value (',' value)* '}';
value: init | INT;
INT: [0-9]+;
WS: [ \t\r\n]+ -> skip;
```

Remember to save this file in the proper place, including potential `package` directory, in my case it will be `src/main/antlr/com/cprieto/samples/ArrayInit.g4`. This is important because if not your generated classes will be placed in the default package!

Now let's write our simple consumer for our parser in Kotlin:

```kotlin
package com.cprieto.sample

import org.antlr.v4.runtime.CharStreams
import org.antlr.v4.runtime.CommonTokenStream

fun main() {
    val input = CharStreams.fromStream(System.`in`)
    val lexer = ArrayInitLexer(input)
    val tokens = CommonTokenStream(lexer)
    val parser = ArrayInitParser(tokens)

    val tree = parser.init()
    println(tree.toStringTree(parser))
}
```

Nice, you know where to put this (`src/main/kotlin/com/cprieto/samples/App.kt`). Our `build.gradle` file should be pretty simple using the right plugins:

```groovy
plugins {
    id 'antlr'
    id 'org.jetbrains.kotlin.jvm' version '1.6.21'
}

repositories() {
    mavenCentral()
}

dependencies {
    antlr 'org.antlr:antlr4:4.10.1'
    implementation 'org.antlr:antlr4-runtime:4.10.1'
}
```

But if we try to build this application will find two nasty surprises!

## There is no `package` declaration

Our Lexers would be generated in the correct directory (in default case, `generated-src/antlr/main/com/cprieto/samples`) but if you check the generated `.java` files, no `package` headers is included! There are a few ways to solve this issue, including the [`@header`]() option in `.g4` files, but I like my grammars to be a little independent, so I prefer to include that as part of the build definition. The ANTLR tool can do this for you with the parameter `-package`, it will be matter of adding this as part of the grammar generation process (controlled by the `generateGrammarSource` task)

```groovy
generateGrammarSource {
    arguments += ["-package", "com.cprieto.sample"]
}
```

## When building, Kotlin compiler cannot find generated Java sources

This is a little more tricky to do, the sources are `.java` files and we need to tell Gradle about this dependency. An easy way to do this is telling the Kotlin compilation task (named `compileKotlin` in Gradle) to wait for the ANTLR generation task to finish before kicking on:

```groovy
compileKotlin {
    dependsOn generateGrammarSource
}
```

With this two things a simple build file can be done and expanded!

```groovy
plugins {
    id 'antlr'
    id 'application'
    id 'org.jetbrains.kotlin.jvm' version '1.6.21'
}

repositories() {
    mavenCentral()
}

dependencies {
    antlr 'org.antlr:antlr4:4.10.1'
    implementation 'org.antlr:antlr4-runtime:4.10.1'
}

generateGrammarSource {
    arguments += ["-package", "com.cprieto.sample"]
}

compileKotlin {
    dependsOn generateGrammarSource
}
```