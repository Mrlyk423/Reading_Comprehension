# Reading_Comprehension
## Data processing
In root file run:
```bash
$ python process_data.py
```
default is for dev data. Use `--train True` to process train data.

Processed data stored in `pro_data` file in following form:
```
{'D':['super', ...], # tokenized document
 'Q':['which', ...], # tokenized question
 'A':[(33, 34), 'denver ...'] # answer offset and answer texts
}
```

dev file: all examples processed.
train file: exact-match answer cannot be found in 35/87599 examples.

