# Eai BAT

## Quick overview

Basic automation tool is mainly a python class which holds various data.

It aims to ease the test's evidence creation by recording steps definition and 
content in an ordered way.

One goal is that class may be subclassed so that your automaton fits your needs.

## What's in?

EaiBat class contains few properties and methods. 

### Properties

- url : yes it's designed to test APIs or Web application
- history : your tests records
- step : your current test step
- evidence_location :  where you store the evidence

### Methods

- push_event
- clear_history
- create_evidence

## How to use it?

### As a standalone...

Well, I don't use it as a standalone. 

You could create an instance of EaiBat, feed the history and then create the evidence.



```python
from eaiBat import EaiBat

my_reporter = EaiBat()

# Set first where evidence should be stored
my_reporter.evidence_location = 'path_to_evidence_location'
# Set the step. Mind that Behave's step do the job
my_reporter.step = ('First step', 'my action')
# Set the history content for the step
my_reporter.push_event("I describe what I do")
# Another step
my_reporter.step = ('Second step', 'another action')
# Another content. Mind the file will be search in the 'evidence_location'
my_reporter.push_event(('screenshot.png', 'img'))
my_reporter.push_event(('sql_file_i_processed.sql', 'sql'))
# Create the evidence
my_reporter.create_evidence("my_evidence.docx", "word")
# Clear the history for a new run
my_reporter.clear_history()
```

### Part of a model