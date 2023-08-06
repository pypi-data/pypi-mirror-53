# Snyp
Snyp is a command line utility that streamlines the process of creating text based documentation and programming tutorials in Markdown.

Snyp extracts specified code snippets from a source file, formats them to enable syntax highlighting in Github Flavored Markdown and prefixes them with a comment exactly specifying where the snippet was extracted from, i.e.:


    ```python
    # snippet from example.py lines 1-2
    print('Hey there!')
    print('This is an example')
    ```
Which would be rendered like this:
```python
# snippet from example.py lines 1-2
print('Hey there!')
print('This is an example')
```
## Installation:
```pip install snyp```

## Usage:  ```snyp --help```

```bash
Usage: snyp.py [OPTIONS] [LINES]...

  Use this tool to extract code snippets from a source file (src) and append
  them to a markdown file (dest)  with proper Github Flavored Markdown
  formatting.

  You can use 0, 1 or 2 'lines' arguments:

  With 0 arguments, the entire source file will be extracted

  With 1 argument, the entire source file starting at lines[0] will be
  extracted

  With 2 arguments, lines lines[0] to lines[1] (inclusively) will be
  extracted from the source file

  Use snip --config to view and update the configuration

Options:
  -s, --src TEXT   The source file from which to extract the code snippet
  -d, --dest TEXT  The destination file to which to append the formatted
                   snippet. "-" for stdout
  -l, --lang TEXT  The language specific formatting to be applied to the code
                   snippet
  -c, --config     Edit the configuration, i.e. to change defaults, add
                   languages, etc.
  --help           Show this message and exit.
```
## Configuration ```snyp --config```
The above command will open Snyp's configuration file in your default editor. It's the easiest way to view and update the configuration.
### Section [default]

```ini
# snippet from snyp.ini lines 1-5 
[default]
default = python
src = snyp.py
dest = README.md


```
+ default: the default language profile to use if -l, --lang is not provided
+ src: relative path to the default source file if -s, --src is not provided
+ dest: relative path to the default destination file if -d, --dest is not provided

### Language sections: [python], etc.

```ini
# snippet from snyp.ini lines 16-19 
[html]
lang = html
commentStart = <!--
commentEnd = -->

```
+ lang: name of the language. Is used for the prefix that determines syntax highlighting
+ commentStart: How a comment starts in *lang*
+ commentEnd (optional): How a comment ends in *lang*
