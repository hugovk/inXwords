# @inXwords

Find a trending topic along the lines of #YinXwords and tweet a random X-word sentence from Project Gutenberg.

See it in action at **[![](https://abs.twimg.com/favicons/favicon.ico)@inXwords](https://twitter.com/inXwords)** and some of the best at [![](http://favstar.fm/favicon.ico)http://favstar.fm/users/inXwords](http://favstar.fm/users/inXwords).

Inspired by Darius Kazemi's [#FiveWordsToRuinADate](http://tinysubversions.com/stuff/fivewords/), and [GenGen](http://tinysubversions.com/gengen/), with which I made this [prototype](http://tinysubversions.com/gengen/gen.html?key=1Fe83835N-GoCl_g6iGGVWpSoJIgRvm-StuFhnt54kWk). I like that Darius's generators are powered by his [gutencorpus](https://github.com/dariusk/gutencorpus), which was inspired by my [gutengrep](https://github.com/hugovk/gutengrep), and gutengrep is used here. Full circle!

## Set up

First we need some lists of sentences from Project Gutenberg. For this I used a tool called [gutengrep](https://github.com/hugovk/gutengrep) on the [August 2003 CD](http://www.gutenberg.org/wiki/Gutenberg:The_CD_and_DVD_Project) ("contains 600 of our best Ebooks").

1. Put all Gutenberg text files in the same directory and `cd` to it.
2. `gutengrep.py "^\w+\s\w+\s\w+[\.?\!]$" --cache > /tmp/3.txt`
3. `edit /tmp/3.txt`
4. Edit out guff at start and end
5. `sort /tmp/3.txt | uniq > /tmp/3-word-sentences.txt`
6. Repeat for four, five and six-word sentences.
7. `wc -l /tmp/*.txt`
```bash
   23949 /tmp/3-word-sentences.txt
   91551 /tmp/3.txt
   31396 /tmp/4-word-sentences.txt
  107418 /tmp/4.txt
   29835 /tmp/5-word-sentences.txt
   94720 /tmp/5.txt
```

8\. Then create a [new Twitter application](https://apps.twitter.com/app/new), a [new Twitter account](https://twitter.com/signup), authorise them using [this](http://i.puthtml.com/boodooperson/twurl) or [that](
https://gist.github.com/moonmilk/035917e668872013c1bd#comment-1333900), fill in the keys in inxwords.yaml, and run something like:

```bash
python inxwords.py  --no-web --loop --yamp /path/to/inxwords.yaml --sendir /path/to/dir/of/gutenberg/sentences
```
