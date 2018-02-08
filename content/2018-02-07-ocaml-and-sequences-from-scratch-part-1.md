title: OCaml and sequences from scratch, part 1
date: 2018-02-07
slug: ocaml-and-sequences-from-scratch-part-1
tags: ocaml, sequences, samples, learning, functional programming
twitter_image: camel_seq_01.jpg
---

I really like [ML languages](https://en.wikipedia.org/wiki/Category:ML_programming_language_family) ([OCaml](https://ocaml.org/), [Elm](http://elm-lang.org/), [F#](http://fsharp.org/)). Recently I was doing the problems in [99 problems in OCaml](https://ocaml.org/learn/tutorials/99problems.html) and found my lack of understanding in some basic patterns with lists.

I decided to reimplement some basic functions and structures in OCaml from scratch as an exercise. I usually do this in a [Jupyter notebook](http://jupyter.org/) but I took my notes and I will be publishing them in my blog from now on (as a way to remember _where I put that bloody notebook_). You can practice and redo this samples with the Jupyter kernel for OCaml, in fact, I already have a small docker image with it ready for you to try if you want to, go and pull it from [Docker Hub](https://hub.docker.com/r/cprieto/jupyter-ocaml/).

# The definition of sequences

Let's start defining a sequence, we will call it `seq`:

```ocaml
type 'a seq =
  | End
  | Next of 'a * 'a seq
```
[]>
type 'a seq = Nil | Next of 'a * 'a seq
<[]

As you can see we use a generic parameter `'a` for the value of the sequence. We can create a sequence with numbers from 0 to 3 and an empty sequence:

```ocaml
let sample = Next(1, Next(2, Next(3, End))) ;;
let empty = End
```
[]>
val sample : int seq = Next (1, Next (2, Next (3, End)))
val empty : 'a seq = End
<[]

# Basic operations

Let's create the simplest operations in town: `length`, `head`, `tail`, `cons` and `nth`

```ocaml
let seq_length x =
  let rec length' acc = function
    | End -> acc
    | Next (_, t) -> length' (acc + 1) t
  in
  length' 0 x
;;

seq_length sample ;;
seq_length empty
```
[]>
val seq_length : 'a seq -> int = <fun>
- : int = 3
- : int = 0
<[]

This pattern is very common in OCaml, I call it _inner accumulator loop_. There is a variation of this pattern and we will see later.

The standard library in OCaml and Caml has the function `length` in the [List module](https://caml.inria.fr/pub/docs/manual-ocaml/libref/List.html)


Now it is time for the `head` operator, or well, it is named `hd` in the `List` module in Caml, it will return only the first element of a sequence or throw an invalid argument if the sequence is empty.

```ocaml
let seq_head = function
  | End -> raise (Invalid_argument "seq_head")
  | Next (x, _) -> x
;;

seq_head sample
```
[]>
val seq_head : 'a seq -> 'a = <fun>
- : int = 1
<[]>

The contrapart of this operator is its brother `tail`, or `tl` in the List module.

```ocaml
let seq_tail = function
  | End -> raise (Invalid_argument "seq_tail")
  | Next (_, t) -> t
;;

seq_tail sample
```
[]>
val seq_tail : 'a seq -> 'a seq = <fun>
- : int seq = Next(2, Next(3, End))
<[]

Easy!

It is time for the `cons` operator, this is basically adding an element to the head of the sequence, in OCaml and Standard ML is denoted as well with the operator `::`

```ocaml
let seq_cons x al = Next(x, l) ;;

seq_cons 0 sample
```
[]>
val seq_cons : 'a -> 'a seq -> 'a seq = <fun>
- : int seq = Next(0, Next(1, Next(2, Next(3, End))))
<[]

Last but not least, it is time to implement the `nth` operator, it will return the element at the index `n` starting from 0.

```ocaml
let seq_nth n l =
  if n < 0 then raise (Invalid_argument "nth") else
  match l with
    | End -> raise (Failure "nth")
    | Next (x, tl) -> if n = 0 then x else nth_seq (n - 1) tl
;;

seq_nth 0 sample ;;
seq_nth 2 sample
```
[]>
val seq_nth : int -> 'a seq -> 'a
- : int = 1
- : int = 3
<[]

Interestinly, this function had the potential to use the _inner accumulator loop_ but if we see clearly it is not needed, remember, if we discard the value of a function when it returns in a recursive call it is basically tail recursive, and here we do nothing with the return value of the function until we need it.

An easy way to check if a function call is [_tail recursive_](http://wiki.c2.com/?TailRecursion) is asking the compiler to tell us so (available since OCaml 4.04)

```ocaml
let seq_nth n l =
  if n < 0 then raise (Invalid_argument "nth") else
  match l with
    | End -> raise (Failure "nth")
    | Next (x, tl) -> if n = 0 then x else ((nth_seq [@tailcall]) (n - 1) tl)
```

In this case, if that marked call is not tail recursive (the place where we suspect is not), the compiler will throw a warning.

That is all for today, we will continue another day!.

**NOTE:** If somebody is interested in the Jupyter notebook for this blog post (and the whole series), it is located in my [GitHub repository](https://github.com/cprieto/notebooks/blob/master/ocaml/OCaml_lists.ipynb).