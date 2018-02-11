title: OCaml and sequences from scratch, comment of part 1
date: 2018-02-11
slug: ocaml-and-sequences-from-scratch-comment-part-1
tags: ocaml, sequences, samples, learning, functional programming
twitter_image: camel_seq_03.jpg
---

My good friend Daniel Chambers ([@danielchmbrs](https://twitter.com/danielchmbrs)) pointed out an error in my code for `seq_append`, and he was totally right! so I fixed it thanks to him, go and check it out, thanks buddy :)

Now, he mentioned something very important:

 >You should try to not make your functions partial (ie throw exceptions). Instead, use the Option type. So head is `'a list -> 'a option` instead of `'a list -> 'a`

In the standard [Caml list module](https://caml.inria.fr/pub/docs/manual-ocaml/libref/List.html) `hd`, `tl` and `nth` throw `failure` if the list is empty, but in the same module we have `nth_opt` returning the _optional_ type instead.

Let's talk a little more about `option`, it is defined like this:

```ocaml
type option 'a =
  | None
  | Some of 'a
```

Using this, implementing our `seq_nth_opt` is an easy job:

```ocaml
let rec seq_nth_opt n l =
  if n < 0 then raise (Invalid_argument "nth") else
  match l with
    | End -> None
    | Next (x, tl) -> if n = 0 then (Some x) else seq_nth_opt (n - 1) tl
;;

seq_nth_opt 0 sample ;;
seq_nth_opt 10 sample
```
[]>
val seq_nth_opt : int -> 'a seq -> 'a option = <fun>
- : int option = Some 1
- : int option = None 
<[]

So, our friend Daniel is right, and I let you as an exercise to implement your own `seq_hd_opt` and `seq_tl_opt`.