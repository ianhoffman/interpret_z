# Interpret Z
This is an interpreter for Sailthru's Zephyr scripting language. I'd gotten fed
up about posting every template to Sailthru in order to check if my code
rendered a context correctly, so I build this. A heavy debt of gratitude and 
inspiration is owed to Ruslan Spivak, whose article series 'Let's build a
simple interpreter' provided the basis for this program. You can read the 
series [here](https://ruslanspivak.com/lsbasi-part1/), if interested.

## Usage
Interpret Z exposes one function, `render`, which takes `.txt` or `.html`
content and a context dict, and renders that dict into the given content, as
follows: 

```python
html_content = interpret_z.render(some_html_template_content, context_dict)
```

where `some_html_template_context` is an (unrendered) string containing
sailthru vars, and `context_dict` is a dictionary of vars to be rendered into
the given HTML.

## Improvements
I've only implemented the bare minimum of Sailthru functions necessary to get
this project up and running. For the rest, we raise a `NotImplemented`
exception (for now). Long term, if you want access to these functions in 
Interpret Z, make a pull request.

## Known Issues
1. Python and Zephyr treat the following expressions differently:

```python
# 3 && 4 && 0
# Zephyr => false
# Python => 0

# 3 && 4 && 2
# Zephyr => true
# Python => 2
```

If you are going to use this interpreter, just avoid these sorts of statements.
Given the limited nature of the programming people tend to do in 
Zephyr, it shouldn't be hard.

For more examples of this bug, see `test_boolean_statements` in 
`tests/test_interpreter.py`.

2. Limited support for Zephyr functions. 

Mostly because of the time involved, I've only supported the Zephyr functions
needed to render the templates I need to test for work. Feel free to make a PR
to add support for more functions (though I imagine supporting something like
`Personalize` is nearly impossible).

3. No support for binary operators

I haven't needed this, so I didn't implement it yet. Again, feel free to make a
PR to add it.

4. No support for making your own dicts.

You can pass in dicts through context, obviously. But you can't initialize them
in Zephyr code. I've never needed to do that, and I honestly don't even know
if Zephyr supports it, but if they do this is something I should add at some
point.

5. No support for keying into a dict.

Interpret Z support dot notation only. Again, I've never attempted to use
`dict['key']` in Zephyr, and I'm not sure why anyone would when you can just do
`dict.key`. Still, it should be included for completeness' sake.

