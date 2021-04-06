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

