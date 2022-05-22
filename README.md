# cmpsc-154-harnesses

## How do I use this?

Plop your lab file in the corresponding directory `lab-0n` and change directory to it. Then

```
pytest --disable-warnings --verbose harness.py
```

The `--disable-warnings` flag is due to a `pyrtl` deprecated import than I don't understand.
