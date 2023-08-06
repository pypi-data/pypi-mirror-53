# Recognizers

Parglare uses scannerless parsing. Actually, scanner is integrated in the
parser. Each token is created/recognized in the input during parsing using so
called _recognizer_ which is connected to the grammar terminal symbol.

This gives us greater flexibility.

First, recognizing tokens during parsing eliminate lexical ambiguities that
arise in separate scanning due to the lack of parsing context.

Second, having a separate recognizers for grammar terminal symbols allows us to
parse not only text but a stream of anything as parsing is nothing more but
constructing a tree (or some other form) out of a flat list of objects. Those
objects are characters if text is parsed, but don't have to be.

Parglare has two built-in recognizers for textual parsing that can be specified
in [the grammar directly](./grammar_language.md#string-recognizer). Those are
usually enough if text is parsed, but if a non-textual content is parsed you
will have to supply your own recognizers that are able to recognize tokens in
the input stream of objects.

Recognizers are Python callables of the following form:

```python
def some_recognizer(context, input, pos):
    ...
    ...
    return part of input starting at pos
```

where `context` is the [parsing context object](./common.md#the-context-object)
and is optional (e.g. you don't have to accept it in your recognizers), `input`
is the input string or list of objects and `position` is the position in the
input where match should be performed. The recognizer should return the part of
the input that is recognized or `None` if it can't recognized at the current
position. For example, if we have an input stream of objects that are comparable
(e.g. numbers) and we want to recognize ascending elements starting at the given
position but such that the recognized token must have at least two object from
the input, we could write the following:

```python
def ascending_nosingle(input, pos):
    "Match sublist of ascending elements. Matches at least two."
    last = pos + 1
    while last < len(input) and input[last] > input[last-1]:
        last += 1
    if last - pos >= 2:
        return input[pos:last]
```

We register our recognizers during grammar construction. All terminal rules in
the grammar that don't define string or regex match (i.e. they have empty
bodies) must be augmented with custom recognizers for the parser to be complete.

In order to do that, create a Python dict where the key will be a rule name used
in the grammar references and the value will be recognizer callable. Pass the
dictionary as a `recognizers` parameter to the parser.

```python
recognizers = {
    'ascending': ascending_nosingle
}

grammar = Grammar.from_file('mygrammar.pg', recognizers=recognizers)
```

In the file `mygrammar.pg` you have to provide a terminal rule with empty body:

```nohighlight
ascending: ;
```


!!! tip

    You can also define recognizers in a separate Python file that
    accompanies your grammar file. In that case, recognizers will be
    automatically registered on the parser. For more information see [grammar
    file recognizers](./grammar_modularization.md#grammar-file-recognizers).


!!! tip

    If you want more information you can investigate
    [test_recognizers.py](https://github.com/igordejanovic/parglare/blob/master/tests/func/test_recognizers.py) test.
