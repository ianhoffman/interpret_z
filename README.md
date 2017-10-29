KNOWN ISSUES:
* Python and Zephyr treat the following expressions differently:

```python
3 && 4 && 0
# Zephyr => false
# Python => 0

3 && 4 && 2
# Zephyr => true
# Python => 2
```

If you are going to use this interpreter, just avoid these sorts of statements.
Given the limited nature of the sort of programming people tend to do in 
Zephyr, it shouldn't be hard.

