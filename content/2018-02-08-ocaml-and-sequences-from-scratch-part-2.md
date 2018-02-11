title: OCaml and sequences from scratch, part 2
date: 2018-02-08
slug: ocaml-and-sequences-from-scratch-part-2
tags: ocaml, sequences, samples, learning, functional programming
twitter_image: camel.jpg
---

This is the second part of my series about simple sequences in OCaml from scratch, the first part is [here]({filename}2018-02-07-ocaml-and-sequences-from-scratch-part-1.md).

We are going to explore a few more complex but not difficult list (or our own definition, `seq`) functions, they will be our building blocks for (_hopefully_) future blog posts. This is a very common pattern in functional programming algorithms, base in smaller functions doing a simple operation. Isn't it beautiful?!

Now it is time for a little more complicated functions, we will start with one of the jewels of the OCaml standard library, `rev`:

```ocaml
let sample = Next(1, Next(2, Next(3, End))) ;;

let seq_rev l =
  let rec rev' acc = function
    | End -> acc
    | Next (x, tl) -> rev' (seq_cons x acc) tl
  in
  rev' End l
;;

seq_rev sample
```
[]>
val seq_rev : 'a seq -> 'a seq = <fun>
- : int seq = Next (3, Next (2, Next (1, End)))
<[]

I said before this is one of the jewels of OCaml, while implementing sequence operations you will use it _many times_.

Now let's try something a little more complex, the `init` function, the idea is that you provide a function `f` and a number `n` and it will return a sequence with _`n` number of elements when applying the function `f` `n`  number of times_. The signature of the function is `int -> 'a`

```ocaml
let seq_init n f =
  let rec init' n' acc = 
    if n' = 0 then acc else init' (n' - 1) (cons_seq (f n') acc)
  in
  init' n End
;;

seq_init 3 (fun x -> x)
```
[]>
val seq_init : int -> (int -> 'a) -> 'a seq = <fun>
- : int seq = Next (1, Next (2, Next (3, End)))
<[]

As you see, the _inner accumulator_ pattern is used here as well, get used to it because it is _very common_ in OCaml, oh, and the function is _tail recursive_!.

## Concatenate lists

We already saw an operation to _append_ an element to the beginning of the list. As you may remember, `cons` (expressed as well in OCaml as the operator `::`) is a _time constant operation_, it doesn't matter how big is the list we are appending the element to, it will _always_ take the same constant time.

This is not the case with appending an element at the end, which is the same case as appending two lists (after all, appending another list is just adding its first element as the last element of the first list).

Let's give our first try:

```ocaml
let rec seq_append a b =
  match a with
   | End -> b
   | Next (x, tl) -> Next(x, ((append_seq [@tailcall]) tl b))
;;
seq_append sample (Next(4, End))
```
[]>
val seq_append : 'a seq -> 'a seq -> 'a seq
- : int seq = Next (1, Next (2, Next (3, Next (4, End))))
<[]

But wait, the OCaml compiler emits a warning! (yeah, that is why I actually added the `[@tailcall]` notation there)

!!! warning ""
    Warning 51: expected tailcall

Yes, that is because our implementation is not tail recursive!, it means it cannot work in _very long sequences_, I did that on purpose because the standard implementation of `append` in the OCaml List module _it is not tail recursive neither!_.

We can do better than this, we can write a tail recursive function!. It is not as efficient though, the operation will roughly be $O(n^2)$

```ocaml
let seq_append a b =
  let rec append' acc = function
    | End -> acc
    | Next (x, t) -> append' (Next(x, acc)) t
  in
  append' End (seq_rev a)
;;

seq_append sample (Next(4, End))
```
[]>
val seq_append : 'a seq -> 'a seq -> 'a seq
- : int seq = Next (1, Next (2, Next (3, Next (4, End))))
<[]

Did you notice the usage of `rev` here? this is another patter I like to call _reverse inner accumulator loop_ (again, I made up that name, I am pretty sure it is known with another sexier name). That pattern is another of the things you will see _very often_ in OCaml list functions, it looks _weird_ but you will see it _everywhere_ with list functions. In the standard [Caml list module](https://caml.inria.fr/pub/docs/manual-ocaml/libref/List.html) we have the function `rev_append` and that does exactly the same.

That is all for today, as usual you can find the original Jupyter Notebook in my [GitHub repository](https://github.com/cprieto/notebooks/blob/master/ocaml/OCaml_lists.ipynb).
