## Overview

The 'longtraceback' module is intended to be used to give more information about the context of exceptions.

Commonly it is necessary to add extra debugging into code which has gone wrong in order to discover what
was happening at the time of the failure. The 'longtraceback' module aims to avoid this situation by
reporting the context of the exceptions in much greater detail than the standard traceback supplied with
Python.

## Features

- Function names are qualified by their path:
    - Functions defined within modules include the module path
    - Methods defined within classes include the module and class path
    - Named functions within methods or functions are given a path through to the function name
    - Function names can indicate the type of symbol that was referenced.

- Functions include information about parameters:
    - The function name can include the parameter names as a prototype (optional)
    - The function name can include all the parameters as a function call (optional)
    - Following the function, we can show the values of the function parameters
    - Parameters which are changed since the function started are inferred (optional)
    - Additional '__traceback_*__' functions as used by _paste_ and _weberror_

- Source lines:
    - Lines have a context lines prior to the frame point (configurable)
    - Source line indentation is not stripped.

- Local variables:
    - Local variables (which have not been listed in the function header) are listed after the source lines
    - Variables are trimmed to avoid instance ids (optional)
    - Properties on objects are included when showing variables (optional)

- Exception information:
    - Exception message are output in the normal way.
    - They are followed by any non-standard properties on the exception object.
    - Syntax error exceptions do not strip the left of the line when highlighting the failure position.

- Filenames within each frame:
    - Filenames are reduced to make it easier to see where the file comes from without having very long paths.
    - <venv> indicates the virtualenv directories.
    - <rootlib> indicates the top level directory (/Library/...) on OS X
    - <syslib> indicates the system libraries (/System/Library/...) on OS X
    - <userlib> indicates the user's python library
    - <main> indicates the directory of the initially invoked script
    - ~ indicates the home directory

- Presentation:
    - Blank lines can be included between each frame (optional)
    - Repetitions of a given frame are detected (optional)
    - Patterns of recursive parameters are reported (optional)

- Error handling:
    - When a problem occurs during frame extraction, backtraces are emitted for the failing case, and the extraction
      falls back to the the old style extraction.
    - When a problem occurs during printing the frames, python will report the exception within the handler, before
      printing the original exception using the normal traceback handler.
    - When a problem occurs during variable evaluation, we can optionally report the variable details (as the
      evaluation invokes at least '__str__' or '__repr__' on the value).

- Interactions with other environments:
    - Aware of virtualenv for path reduction.
    - Replaces the functions in the traceback module to allow other modules to gain from the new behaviour.
    - New classes replace the Frame and Line information, so that users who do not understand them will get the
      string behaviour they expect.
    - When supplied with unaugmented extracted frame information (eg from prior to the import of this module),
      the functions behave sensibly, reporting as much information as they can.
    - When supplied with fake frame information (eg from Jinja2 tracebacks through the template code), the
      presentation provides as much information as possible.

- Colouring of exception output:
    - In terminal, ANSI colouring is used to generate coloured output (optional).
    - Rule-based configuration of colours allows customisation.

- Configurable:
    - User configuration file allows most features to be customised.
    - Environment variable override allows configuration to be fixed in test environments.


## Examples

Taken from one of the tests, the original python traceback would produce the following output:

``` none
Boing
Traceback (most recent call last):
  File "test_expect/function_naming/t09_inheritance_and_super.py", line 29, in <module>
    body.hit()
  File "test_expect/function_naming/t09_inheritance_and_super.py", line 25, in hit
    super(RubberWorld, self).hit()
  File "test_expect/function_naming/t09_inheritance_and_super.py", line 14, in hit
    raise Exception("Body '%s' got hit!" % (self.__class__.__name__,))
Exception: Body 'RubberWorld' got hit!
```

The long traceback produces the following instead:

``` none
Boing

Traceback (most recent call last):
  File '<main>/t09_inheritance_and_super.py', line 29, in __main__
       25 :         super(RubberWorld, self).hit()
       26 :
       27 :
       28 : body = RubberWorld(1,2,-1,+1)
       29-> body.hit()
    Locals:
      body = <__main__.RubberWorld object>
       .vx = -1
       .vy = 1
       .x  = 1
       .y  = 2

  File '<main>/t09_inheritance_and_super.py', line 25, in __main__.RubberWorld.hit
    self = <__main__.RubberWorld object>
     .vx = -1
     .vy = 1
     .x  = 1
     .y  = 2
       23 :     def hit(self):
       24 :         print("Boing")
       25->         super(RubberWorld, self).hit()

  File '<main>/t09_inheritance_and_super.py', line 14, in __main__.Body.hit
    self = <__main__.RubberWorld object>
     .vx = -1
     .vy = 1
     .x  = 1
     .y  = 2
       13 :     def hit(self):
       14->         raise Exception("Body '%s' got hit!" % (self.__class__.__name__,))

Exception: Body 'RubberWorld' got hit!
```

Same output, but using the colouring system:

![Coloured traceback](images/coloured.png "Simple coloured traceback")


## How to use

How you use the longtraceback module depends on what type of usage you intend for it.

* At the command line it can be used very simply by referencing the module and using a Python REPL shell.
* Embedded within an application, it is only necessary to import the longtraceback module to override the default traceback system.

### Using the module from the command line

1. Obtain a copy of the sources.
2. Run the script to diagnose with: `PYTHONPATH=(path-to-module) python -mlongtraceback.shell (your-script)`

For simplicity, I have a small bash script in my path called `lpython` which does the equivalent for me:

``` bash
#!/bin/bash
##
# Activate python with the longtraceback extensions
#

export PYTHONPATH=$HOME/projects/longtraceback/

python -mlongtraceback.shell "$@"
```


## Configuration

The longtraceback module is configurable through a configuration file. This will be loaded on module
initialisation from the file referenced by the environment variable `PYTHONLONGTRACEBACKCONFIG`, or
if it is unset, from the file `~/.python.longtraceback`.

The configuration file is a file parseable by ConfigParser (ie an .ini-like format), which contains
two sections:

1. `options` - contains the main options for the traceback system
2. `colours` - contains rules for colouring the output

An example file can be found in [examples/python.traceback](examples/python.traceback).

To display the current configuration in a form suitable for putting into the configuration file,
the following commands can be used:

  python -mlongtraceback.Options
    - display the configuration with the defaults commented out
  python -mlongtraceback.Options --defaults
    - display the configuration with the defaults present


### Options

The options take the form of settings which control whether settings are enabled or not, or the
limits to which they apply. The options are described in Options.py file, and the configuration
file example. See `examples/python.longtraceback` for an example configuration file containing
the descriptions of the options.


### Colours

When enabled, the colours used by the module are defined within the `colours` section of the
configuration file. These take the form of keys which describe the rule to match areas of
the traceback output, and a value that is a comma-separated list of the properties to use.

The rules take the form of a .-separated list of the tokens used to describe the area of
the traceback output. For example, headers within the file are always described with the
`header` token. To see what tokens are used for a given traceback, the styling format option
in the main `options` section can be given the value `tokens`. When output as tokens,
each token will be listed in the output within `<>` markers.

If a rule starts with a `.` character, the rule may match anywhere within a list of tokens.
Without the leading `.`, the rule matches from the start of the list.

The rule values take the form of property assignments. Properties describe how the rule should be
presented. Some properties have values (like colours), and others do not (like bold). Values
are given after an `=` sign in the list. The following properties are supported:

- `fg` - foreground colour. Takes a named colour as a value.
- `bg` - background colour. Takes a named colour as a value.
- `bold` - bold enable. No value.
- `underline` - underline enable. No value.

Colours supported are the 8 standard ANSI colours:

- black
- red
- green
- yellow
- blue
- magenta
- cyan
- white

The supplied colour scheme is suitable for a black-background terminal. It may not be ideal for
white-background terminals.

For example, to change the colour of the filenames in the header, the rule used could be:

```
.header.file: fg=blue
```

A non-exhaustive list of the tokens used:

- `context` - part of the source context lines around the failure
- `context-caret` - the caret indicating the failure in a syntax error
- `exception-name` - the exception name at the end of the output
- `filename` - a filename
- `function-name` - a function name
- `function-type` - the inferred type of the function
- `frame-repeated` - the message indicating the repetitions of the function frame
- `header` - part of the header lines
- `header.cause` - the messsage saying that this exception caused another one (Python 3 only)
- `header.context` - the messsage saying that this exception was in a context (Python 3 only)
- `header.exception` - the exception message
- `header.file` - a header describing the function frame
- `header.locals` - the local variables header
- `header.traceback` - the initial message for traceback (not used in Python 2)
- `internal-exception` - any internal errors which occurred whilst processing traceback
- `line-divider` - the divider mark in the source context
- `line-exception` - the marker for the line the exception was on
- `lineno` - a line number within file description
- `line-number` - the number of the source context line
- `local` - a second of the local variables
- `parameter` - the parameter to a function
- `parameters` - a section of the function parameters
- `property` - a property of an object
- `sequence-values` - the values used within the repeated frames
- `source` - source code
- `varname` - a variable name
- `varvalue` - a variable value
