![Beads Logo](https://gitlab.com/a.wuillemet/beads/raw/master/documentation/media/logo.png)

# Beads - A tool to generate code from state machines

_**2019** <sup>©</sup> Jakob Baatz, Rico Possienka, Pavel Nepke, Marco Wenning, Adrian Wuillemet_<br>
<br>
<br>

## Introduction

As a software developer you can encouter state machines as part of a logic that
can parse content, as a description of AI behaviour or while modelling some
buisness processes.<br>
In whatever form, state machines are cumbersome to code, as the written code is
very repetitive and it is quite easy to loose oversight as the machine gets bigger.<br>
<br>
For this purpose **Beads<sup>©</sup>** can aid you in consistently generating that
code from textfiles or drawings that you provide. Simply write a **.json**
 representation of your machine or use our simplified _**.bead**_ format to write
down the logic.<br>
<br>
**Beads<sup>©</sup>** is an open source python and webtech tool that can be used
from the command line and is easy to incorporate into scripts for project builds.
Additionally the Graphical User Interface (GUI) provides means to draw visual
representations of your machines and will persist them as _**.svg**_, _**.png**_
 and _**.json**_ files.<br>
**Beads<sup>©</sup>** comes with a validaten logic for simple state machines,
that can be turned off if needed.<br>
<br>
All further informations and details on writing state machines and using **Beads<sup>©</sup>**
can be found below!<br>
<br>
[Project Screenshots](https://docs.google.com/presentation/d/1R3tYoSjhtAN2ghXU36P8B2fT_jkr9z0OJo2ymSYXALM/edit?usp=sharing)
<br>

## Table of Contents
   1. [Dependencies](#deps)
   2. [Download and Installation](#download)
   3. [Command line usage](#cmd)
   4. [Using the Graphical User Interface](#gui)
   5. [Supported file formats](#formats)
   6. [Used technologies](#techs)

<br>
<br>

### 1. Dependencies  
<a name="deps"></a>  

**Beads<sup>©</sup>** is a commandline tool built with Python for the backend and
web technologies for the GUI. To run beads you need to have<br>

<br>

   * **Python 3.x.x**
   * **a web browser of your choice**

<br>

installed on your system. And thats it. If you do not have python installed you
can get it from [here](https://www.python.org/downloads/).<br>
The tool is usable without any web browser, however only from the commandline.
<br>

As listed in the section Used technologies, **Beads<sup>©</sup>** is
built with the python library [Eel](https://pypi.org/project/Eel/) which utilizes Chrome / Chromium
in app-mode to display our GUI. We do not want to force a user that wants to work with the
GUI to install chrome/chromium, neither do we want to package a distribution of them for users
that do not care about the GUI.<br>
<br>
Chrome or Chromium is only a soft dependency, with which **Beads<sup>©</sup>** - GUI
works best. Alternatively any other modern web browser will suffice and the system standard
browser will be used, if no Chrome is detected.
<br>
<br>

### 2. Download and Installation  
<a name="download"></a>  

Dowloading and installing **Beads<sup>©</sup>** is extremely easy:<br>
We deploy the tool and all updates via the [Python Package Index](https://pypi.org). So to get your
hands on the tool simply install it with _pip_ and you are good to go.

```shell
$ pip install Beads
```

Any internal dependencies will be handled by pip!<br>

The second method is to clone the project with [Git](https://git-scm.com) and set it up
by yourself. We do not support this method and therefore provide no guide on how to.
Any usage described in the sections below may differ if you install the tool this way.
<br>
<br>

### 3. Commandline usage  
<a name="cmd"></a>  

**Beads<sup>©</sup>** follows standard conventions on commandline usage. A list of
available commands and options, as well as documentation for them can be found below.<br>
Alternatively running

```shell
$ beads --help  
#or
$ beads [command] --help
```

from the commandline will print the help section of the tool that contains all needed
information as well. We advise users to default to the cmd **--help** option for all commands
and options rather than consulting this section, as that is always up to date.

**List of commands and options**<br>
_(including examples of usage)_<br>

Printing information on the terminal:
```shell
$ beads [command] [option] --help
```

Printing the current version:
```shell
$ beads --version
```

Print an overview of all supported programming languages:
```shell
$ beads languages

# it is possible to filter the languages by appending a search string like 'ava'
# which will only display supported languages that contain the string like 'java' or 'javascript'
$ beads languages ava 
```

The main purpose of the tool is to parse a textual representation of a state machine
into working code.<br>
To to so you use the command 'parse':
```shell
$ beads parse FILES [options]

# Options
$ beads parse FILES
        -l / --language             # Specify the programming language of the generated code. Default: none
        -o / --out                  # Specify the output file. Default: ./FILENAME.language
        -re / --replace-existing    # FLAG to replace existing files with the generated code
        -nv / --no-validation       # FLAG to skip the internal validation of the state machine logic
        -bd / --base-directory      # Set a base directory, that all files will be saved in. Default: .
        
        -v / --verbose              # FLAG to execute the programm in verbose mode printing all debug information


# Examples

$ beads parse /E/documents/controller.bead
# assuming you have a state machine in a .bead file here: /E/documents/controller.bead
# the command will parse the file and save the generated code in the current working directoy.

$ beads parse /E/documents/controller.beads ../machines/statemachine.json
# it is possible to provide multiple files at once

$ beads parse machine.json --language python --no-validation
# will skip the validation of state machine logic and try to produce code in python

$ beads parse machine.json --out ../package/machine.py --replace-existing
# will save generated code in ../package/machine.py and replace an already existing file if there is one

$ beads parse machine1.bead machine2.bead machine3.bead --base-directory ./machines/code
# will parse all three provided machines and save them in the specified directory ./machines/code

$ beads parse machine1.bead controller2.json -l java -v -re -bd ../code/generated/
# Complex example executing verbose, replacing any existing file
# and placing the generated code from both files which will be java code into ../code/generated
```

All commands related to the Graphical User Interface are bound to 'gui':
```shell
$ beads gui [options]

# Options
$ beads gui
        -b / --background     # Run the gui in the background without opening a window
        -p / --port           # Run the gui on the specified port. Default: 8000
        -v / --verbose        # Run the gui in verbose mode. Default: false
        --file FILE           # Run the gui and load the provided FILE. Needs to be a valid json representation of a state machine.


# Examples

$ beads gui -v -p 11000
# Run the gui in verbose and on localhost:11000

$ beads gui --file ./stateMachine.json
# Open the gui and load the provided stateMachine.json to display upon loading
```

You can set some commandline options as default values that will be considered without having to provide them on the commandline. Providing options via commandline however will overwrite defaults.

```shell
$ beads options [options]

# Options
$ beads options
        -s / --set-default OPTION VALUE     # Set the default VALUE for OPTION
        -u / --unset-default OPTION         # Unset the default value for OPTION
        --unset-all                         # Unset all currently saved defaults.
        --show                              # Print a list of available Options and their data type


# Examples

$ beads options --show
# First prints all available options and then the overview of all currently set defaults

$ beads options --set-default language python
# Sets the default language used to generate code to python

$ beads options --unset-default language
# Unsets the default value of language

$ beads options -s port 11000 -s language java -u verbose
# Multiple -s / -u can be provided with one call:
# First unsets --verbose, then sets --port to 11000 and --language to java

$ beads options --unset-all
# Clears all saved default options
```

<br>
<br>

### 4. Using the Graphical User Interface
<a name="gui"></a>

The Graphical User Interface allows the drawing of simple fine state machines. You can draw states and transitions and save the whole graph in different file formats. A tutorial is available within the GUI!
<br>

All further functionality should be self-explanatory and is properly visualized in the gui.

<br>
<br>

### 5. Supported file formats
<a name="formats"></a>

State machines can be provided in textual representations. Currently there are two file formats that are supported by **Beads<sup>©</sup>**:

   + JSON: file.json
   + BEAD: file.bead

<br>

**Json format**

To provide a state machine as a JSON file follow the schema below:

Three attributes are required:

   + A **name** for the machine  
   + A list of **nodes** with an "ID" representing the states  
   + A list of **transitions** with "from" and "to" referencing nodes, and a "label"  

To declare a state as the initial starting state append '"start":true' to the node.

```json
{
   "name": "NAME",
   "nodes": [
      {"id":"ID1", "start":true},
      {"id":"ID2"}
   ],
   "transitions": [
      {"from":"ID1", "label":"TRANS1", "to":"ID2"},
      {"from":"ID2", "label":"TRANS2", "to":"ID1"}
   ]
}
```
<br>

**Bead format**

As an easy-to-write alternative to json files the tool accepts **.bead** files that adhere to the following format:

```
#! name:NAME start:ID1  

ID1:TRANS1:ID2  
ID2:TRANS2:ID1  
```

The **.bead** format is transition based. All transitions follow the schema:<br>
FROM_STATE : TRANSITION_NAME : TO_STATE<br>

The name and the starting point are optional and can be declared as key:value pairs in a config comment on the top of the file.
The comment has to start with '#!' which is followed by a whitespace.

Parsing of **.bead** files will extract all referenced states so they do not have to be declared separately.

<br>
<br>

### 6. Used technologies
<a name='techs'></a>

We are building an open source lightweight tool for commandline usage with the following techs:

**CLI**

___
![Python](https://img.stackshare.io/service/993/pUBY5pVj.png)
![Click](https://gitlab.com/a.wuillemet/beads/raw/master/documentation/media/click.png)
![Eel](https://gitlab.com/a.wuillemet/beads/raw/master/documentation/media/eel.png)

<br>
<br>

**GUI**

___
![HTML5](https://img.stackshare.io/service/2538/kEpgHiC9.png)
![Sass](https://img.stackshare.io/service/1171/jCR2zNJV.png)
![Typescript](https://img.stackshare.io/service/1612/bynNY5dJ.jpg)
![D3.js](https://img.stackshare.io/service/1491/d3-logo.png)
![Prism.js](https://avatars0.githubusercontent.com/u/11140484?s=400&v=4)
