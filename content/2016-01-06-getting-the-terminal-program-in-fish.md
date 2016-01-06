title: Getting the terminal name in Fish shell
date: 2016-01-06
slug: getting-the-terminal-program-in-fish
tags: fish, shell, programming
---

I don't know you but I love the [Fish shell](http://fishshell.com/). Yeah yeah I know, it is not [POSIX](https://en.wikipedia.org/wiki/POSIX) standard and all those things, but seriously, it is awesome, go, give it a try.

Well, one of the problems you find when you move to Fish is finding good shell scripts, because for most cases Fish syntax is incompatible with [ZSH](https://en.wikipedia.org/wiki/Z_shell) or [Bash](https://en.wikipedia.org/wiki/Bash_(Unix_shell)). Today was one of those days. I wanted to write a simple script to give me the name of the current terminal I was working on, and I find this nice line of code in
[StackExchange](http://askubuntu.com/questions/476641/how-can-i-get-the-name-of-the-current-terminal-from-command-line) but, well, it is not going to work in Fish:

```bash
ps -p $(ps -p $$ -o ppid=) -o args=
```

First, we need to understand what the script does: `$$`, which is pretty awesome, returns the PID of the current process (in this case, the terminal process) and well, `ps` is the standard [process status command](http://www.linfo.org/ps.html) with arguments to return the process id of its parent. Easy, right?

Well, Fish has no notion of `$$`, but the equivalent is our friend `%self`. Another big difference is how to group operations. In Bash you use `$()`, but in Fish you just use a simple parenthesis. So at the end the equivalent command is just:

```fish
ps -p (ps -p %self -o ppid=) -o args=
```

Nice! Wait... If you run this command in Linux using something like [Gnome terminal](https://en.wikipedia.org/wiki/GNOME_Terminal) or [Konsole](https://www.kde.org/applications/system/konsole/) it will work, and it is awesome but guess what, in MacOSX it doesn't work, it will just return `login -fp blah` instead of the terminal name... bummer! Well, that is a _feature_ in MacOSX, but luckily you can just query an environment variable, `TERM_PROGRAM`, and that will give you the answer you are looking for!

Now, we just add a few other things, like removing the application path and extension if present, and voila! there you have the full script! (You can get the script from my [Github gist](https://gist.github.com/cprieto/88d239a50ec345e95f0f))

```fish
function which_term
  switch (ps -p (ps -p %self -o ppid=) -o args=)
  case 'login*'
    echo (basename $TERM_PROGRAM .app)
  case '*'
    echo (basename (ps -p (ps -p %self -o ppid=) -o args=))
  end
end
```

See? Fish is awesome!
