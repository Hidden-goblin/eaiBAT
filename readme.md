# Eai BAT

## Quick overview

Basic automation tool is mainly a python class which holds various data.

It aims to ease the test's evidence creation by recording steps definition and 
content in an ordered way.

One goal is that class may be subclassed so that your automaton fits your needs.

## What's in?

- EaiBat class with few properties and methods.
- folder_file_name_cleaning package function which cleans a string from spaces and some special characters.

### Properties

- url : yes it's designed to test APIs or Web application. Allow `http`, `https` and `ftp` scheme, ASCII letters, digits and `+`, `.` and `:` characters
- history : your tests records in an ordered dictionary.
- step : your current test step. It's a length two tuple containing `int` or `string`. It might be constructed using a Behave's Step. 
- evidence_location :  where you store the evidence as a `string`.

### Methods

- push_event: takes one event argument
    - a request's Response object,
    - a `string`
    - a `dictionary`
    - a length 2 tuple for file event. First part is the filename (relative to the evidence_folder) and the second part is the file type. Currently, only three types are managed: `img`, `txt` or `sql`.
- clear_history: without argument.
- create_evidence: takes two arguments
    - `filename`: the evidence filename
    -  `evidence_type`: either `markdown` or `word`

## How to use it?

### As a standalone...

Well, I don't use it as a standalone. 

You could create an instance of EaiBat, feed the history and then create the evidence.

It may look like something as below 

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

### Part of `Behave` framework

I prefer using this package as part of `Behave` test automation framework.

Here is my usage:

- In the environment.py file (see [Behave's documentation](https://behave.readthedocs.io/en/stable/api.html#environment-file-functions))

```python
from helpers.model import MyModel
from eaiBat import folder_file_name_cleaning

def before_all(context):
    context.model = MyModel()
    context.model.url = 'http://my.test.environment.com'
    
    
def before_step(context, step):
    context.model.step = step

    
def before_scenario(context, scenario):
    context.model.evidence_location = f'evidence/{folder_file_name_cleaning(scenario.name)}'
    
def after_scenario(context, scenario):
    evidence_name = f"{scenario.name}-{scenario.status}.docx"
    context.model.create_evidence(folder_file_name_cleaning(evidence_name), "word")
    context.model.clear_history()
```

- In the helpers.model package (homemade package for the test automation) assuming I test a GUI application and I have a `take_a_screeshot` function which return the picture's filename 

```python
from eaiBat import EaiBat


class MyModel(EaiBat):
    def some_action(self):
        # Action I want to reuse in my steps
        self.push_event((take_a_screenshot(), 'img'))
```

- In the steps definitions

```python
from behave import Given
from shutil import copy

@Given('I set "{user}" user')
def set_user_in_db(context, user):
    try:
        execute_sql_script(f'resources/script/{user}.sql')  # Assuming you have a function executing sql scripts
        context.model.push_event(f"The {user} is in the database")
        copy(f'resources/script/{user}.sql', f'{context.model.evidence_location}/{user}.sql')
        context.model.push_event((f'{user}.sql', 'sql'))
    except Exception as exception:
        context.model.push_event(f"The step has failed due to {exception.args}")
```