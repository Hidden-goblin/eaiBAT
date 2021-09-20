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

## How to I use it?

### As a standalone...

Create an EaiBat object. 
Set the url if you work with web or apis.
Set the folder where you store your tests' evidences.
For each step you are conducting, set the step as a size 2 tuple or a Behave step.
Push your events to the history.
Create the evidence base on the current history.

### As a mother class for your (page/api) model

Create your model class as a EaiBat subclass.
Each action done in your model, push an event.
Your test executor provide the step data.

It's designed to work with Behave.


