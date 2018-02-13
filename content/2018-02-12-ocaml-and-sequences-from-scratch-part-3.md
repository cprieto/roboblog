title: OCaml and sequences from scratch, part 3
date: 2018-02-13
slug: ocaml-and-sequences-from-scratch-part-3
tags: ocaml, sequences, samples, learning, functional programming, algorithms
twitter_image: camel0_seq_04.jpg
---

Now it is the turn for three favourites in the [Caml standard List module](https://caml.inria.fr/pub/docs/manual-ocaml/libref/List.html), `map`, `fold_right`, `fold_left`.

Let's start _with the non-tail recursive version_ of `map` (the List module version is not tail recursive neither), the idea is to return a list `'b` which is the result of applying the function `'a -> 'b` to all the members of a list `'a`, or well in our case `('a -> 'b) -> 'a seq -> 'b seq`

```ocaml
let seq_map ~f l =
  | Next (x, t) -> Next ((f x), ((seq_map [@tailcall]) f t))
  | _ -> End
;;

seq_map ~f:(fun x -> x * 2) sample
```
[]>
val seq_map : f:('a -> 'b) -> 'a seq -> 'b seq = <fun>
- : int seq = Next(2, Next(4, Next(6, End)))
<[]

As expected we will get the tailcall error:

!!! warning ""
    Warning 51: expected tailcall

Again, the original `map` function in the Caml standard list module is not tail recursive (the version in [Core](https://ocaml.janestreet.com/ocaml-core/111.28.00/doc/core/#Core_list) is), notice as well the use of the named arguments, when working with the mix of list and functions is a good idea to use them.

Let's work in our tail recursive version, it will become easy if we use the now familiar `reverse inner loop accumulator` style

```ocaml
let seq_map f l =
  let rec map' acc = function
    | End -> acc
    | Next (x, t) -> map' (Next((f x), acc)) t
  in
  rev_seq (map' End l)
;;
```

# The power of fold

The `fold` operations are called reducers and aggregators by others, the idea is `calculating` a running value through a sequence. We agregate values from a sequence with a function who takes the current value and previous value of the applied function. In some parlance it is called _reducers_.

There are two versions of `fold`, the common `left` version _folding_ from left to right (moving the apply function from the left to the right)

Let's start with probably the most powerful function in the List module, `fold_left`

```ocaml
let rec seq_fold_left ~f ~init = function
  | End -> init
  | Next (x, tl) -> (seq_fold_left [@tailcall]) ~f ~init:(f x init) tl
;;

seq_fold_left ~f:(fun a b -> a + b) ~init:0 sample
```
[]>
val seq_fold_left : ~f:('a -> 'b -> 'b) -> ~init:'b -> 'a seq -> 'b = <fun>
- : int = 6
<[]

Here I put the `@tailcall` here so I can demostrate _the function is already tail recursive_, the compiler throws no warning! Nice!

The `fold_right` expression (fold from the right to the left) can be easily expressed now simply reversing the sequence and applying `fold_left`:

```ocaml
let seq_fold_right ~f ~init l = 
  seq_fold_left ~f ~init (seq_rev l)
;;
```
[]>
val fold_right_seq : f:('a -> 'b -> 'b) -> 'a seq -> init:'b -> 'b = <fun>
<[]

We can even express functions like `rev` as a `fold` function:

```ocaml
let rev_seq' = 
  fold_left_seq ~f:(fun l' x -> cons_seq x l') ~init:End 
;;

rev_seq' sample
```
[]>
val rev_seq' : '_weak8 seq -> '_weak8 seq = <fun>
- : int seq = Next (3, Next (2, Next (1, End)))
<[]

Notice how we _curry_ the function, this is a very common style in FP

Another function easy to implement now with fold is the familiar `map`

```ocaml
let map_seq' ~f =
  fold_right_seq ~f:(fun elem l -> cons_seq (f elem) l) ~init:End
;;
map_seq' ~f:(fun x -> x * 2) sample
```
[]>
val map_seq' : f:('a -> 'b) -> 'a seq -> 'b seq = <fun>
- : int seq = Next (2, Next (4, Next (6, End)))
<[]

See? I told you `fold` is a very powerful function ;)

Next time (I hope) we will talk more about _tail recursion_ and why some functions in the Caml standard library are not tail recursive (and core offers both versions). As usual the Jupyter notebook with more of my notes (and the origin of this series) is in [my GitHub repo](https://github.com/cprieto/notebooks/blob/master/ocaml/OCaml_lists.ipynb).