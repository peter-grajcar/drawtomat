# Drawtomat

Drawtomat is a picture generator which creates pictures based on a natural 
language description.

## Installation

To download UDPipe pretreained models use:

```console
$ make udpipe
```

Following command will set up Python virtual environment:

```console
$ make install
```

Then the programme can be executed with following command:

```console
$ make run
```

Or alternatively
```console
$ export PYTHONPATH=src
$ python3 -m drawtomat [-h] [--help]
                       [--description DRAWING_DESCRIPTION]
                       [--graph_output GRAPH_OUTPUT_PATH]
                       [--image_output IMAGE_OUTPUT_PATH]
                       [--show]
```

Or start a HTTP API server:

```console
$ make run-api
```

## Code Documentation

Code is documented using *[Sphinx][5]*. Documentation can be generated using
following command:

```console
$ make docs
```

The documentation is also available [here](http://www.ms.mff.cuni.cz/~grajcarp/drawtomat/docs/).

## Overview

The picture is generated in two phases. These phases are discussed in more 
detail in following sections. 

In the first phase a text description is transformed into a relation graph. 
The graph contains all objects which will be drawn and relations between the 
objects and groups of objects.

The second phases uses relation graph to place objects and compose a scene 
which is then drawn. 

<p align="center">
<img alt="Drawtomat picture generation phases" src="resources/images/phase-diagram.svg" />
</p>

<p align="center">
<i>Diagram of picture generation phases</i>
</p>

Drawtomat user interface is very simple. It takes the standard input as a
description.

```console
$ make run
Description: A dog and a couch are in a house. The dog is on the couch.
```

<p align="center">
<i>Example input</i>
</p>

After receiving the input an image is generated and a window with the image
and relation graph will show up.

<p align="center">
<img height="400" alt="Drawtomat output example" src="resources/images/drawtomat-window.png" />
</p>

<p align="center">
<i>Example output</i>
</p>

### Scene Graphs

A scene graph is a directed graph where entities (objects and groups) are the 
nodes and mutual relations between objects are the edges. An example can be
found in the picture below. 

Formally groups can be seen as nodes and object membership in a group is a 
special relation represented by an edge. However, for the sake of simplicity
the groups will be drawn as containers with objects inside in relation graph
diagrams.

Drawtomat allows relation graph export in [dot language][6].

<p align="center">
<img height="350" alt="Relation graph example" src="resources/images/relation-graph.svg" />
</p>
<p align="center">
<i>Example of a relation graph</i>
</p>

&copy; 2020 Peter Grajcar

[1]: http://ufal.mff.cuni.cz/udpipe "UDPipe"
[2]: https://universaldependencies.org/format.html "CoNLL-U Format"
[3]: http://lindat.mff.cuni.cz/services/udpipe/ "UDPipe Online Service"
[4]: https://quickdraw.withgoogle.com/ "Quick, Draw! dataset"
[5]: https://www.sphinx-doc.org/en/master/ "Sphinx Documentation"
[6]: https://graphviz.org/doc/info/lang.html "Graphviz Dot Language"
[7]: https://docs.python.org/3/library/tkinter.html "Tkinter"
