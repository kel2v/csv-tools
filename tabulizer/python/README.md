Name
---
tabulizer - extract position value of every datapoint of a CSV file into a *outputfile*

syntax
---
```
python3 tabulizer.py [-o] [-p] [-cr | -lf | -crlf] [-lb | -nlb] [-d directory] sourceCSVfile
```

Description
---

This python code can extract the **position value** and **string length** (position w.r.t the file beginning) of every datapoint from a RFC 4180 compliant CSV source file and output these paired values on a textfile as a table of ordered pairs of the format **(position value,string length)** (enclosed within the curly-brackets). All the ordered pairs, seperated by a single space, on a single line corresponds to the datapoints of the corresponding record on the CSV file.

This *outputfile* is intended to serve as the metadata for quick access of any random datapoint of a CSV file without traversing over the entire file scanning for it. The -o option is required to output this *outputfile*.

For example, if the 3rd ordered pair in the 5th line of the *outputfile* is (20,8), this means that the datapoint in the 3rd column of the 5th row in the source CSV file starts at the position 20 (from the file beginning), and to extract it, **seek** to the position 20 and **read** 8 characters from there.

It can also print the CSV data in a neatly formatted tabular form using -p option to the *stdout*.

If no optional options are used, the program assumes \n (ascii code 0x0A) as the `line break` sequence and expects the source CSV file to end with a `line break` character (if it doesn't end with a `line break` character, it virtually adds a `line break` at the end of the source CSV file, but does not affect the actual source CSV file), and informs whether the input CSV file is valid (according to RFC 4180 standard) or else displays the reason it is invalid (doesn't generate *outputfile* or print source CSV data in a tabular form to *stdout*).

Options
---

-o :
generates the *outputfile* containing the curly-bracket enclosed ordered pairs containing the **position value** and **string length** of all the data units

-p :
prints the content of the CSV file in a neatly formatted tabular form

-cr :
sets the `line break` sequence as \r (ascii code 0x0D), and interpretes any occurance of such sequence in the source CSV file as a `line break` character

-lf :
sets the `line break` sequence as \n (ascii code 0x0A), and interpretes any occurance of such sequence in the source CSV file as a `line break` character

-crlf :
sets the `line break` sequence as \r\n (ascii code 0x0D 0x0A), and interpretes any occurance of such sequence in the source CSV file as a `line break` character

-lb :
inform the program that the last record (row) of your source CSV file has a following `line break` character, i.e., the last character of your source CSV file is the `line break` character.

-nlb :
inform the program that the last record (row) of your source CSV file does not have a following `line break` character.

-d :
inform the program to save the *outputfile* in the directory mentioned in the immediate next argument to this option. The directory path could be either a relative path or an absolute path. Note that, to use this option, you must use -o option aswell.

Note
---
It is advised to inform the program whether the last record of the source CSV file is followed/not-followed by a `line break` character using -lb or -nlb option to avoid any misinterpretation of the source CSV file.
