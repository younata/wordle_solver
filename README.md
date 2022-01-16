# Wordle Solver

Python CLI script to solve [wordles](https://www.powerlanguage.co.uk/wordle/).

You need at least python 3.8 installed to run this. No dependencies.

## Sample Usage

Let's say the wordle is "blank".

```text
$ python3 main.py
Provide feedback in terms of initial of color of feedback. Use 'x' for when the letter is marked as black. This script does recognize the high-contrast colors. e.g. xxygx if the result was 'black', 'black', 'yellow', 'green', black'. Hit ^D (control+D) if you've solved it.
Try the word "arose"
How was it?
```

You then type `yxxxx` into the prompt.

```txt
How was it? yxxxx
Try the word "caama"
How was it?
```

Which, as it turns out, is in your computer's word list, but not in wordle's word list. So you type "invalid".

```txt
How was it? invalid
Try the word "liana"
How was it?
```

Which has 3 correct letters. Two of which are in the right spot. So, you type `yxggx`.

```txt
How was it? yxggx
Try the word "plant"
How was it?
```

Which is close, but not quite right. You type `xgggx` at the prompt.

```txt
How was it? xgggx
Try the word "blanc"
How was it?
```

Which, again, for me, is another word that's not in wordle's word list. But, it comes around and suggests "clang".

```txt
How was it? invalid
Try the word "clang"
How was it?
```

Which has the same issue as before, `xgggx`.

```txt
How was it? xgggx
Try the word "bland"
How was it? 
```

Almost there! You type `ggggx`, and then it comes back and suggests "blank". Which is the correct word. You can either type `ggggg` or just enter control+d to exit. It'll congratulate you, then exit.
