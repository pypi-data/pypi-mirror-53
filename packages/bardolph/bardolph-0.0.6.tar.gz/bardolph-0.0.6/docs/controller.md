![bulb](bulb.png) 
# Bardolph Controller Module

 Part of the [Bardolph Project](https://www.bardolph.org)

## Introduction
This document is the first draft of an description of Bardolph's core module
that interprets a script and accesses the lights.

The module builds on a very simple virtual machine that executes a program 
built out of a narrow set of instructions, described below.

## VM Architecture
The VM has a set of special-purpose registers. They are:
1. hue
1. saturation
1. brightness
1. kelvin
1. duration
1. power
1. name
1. operand
1. time

Although each register is expected to have a specific type, in practice each one
is a Python variable and can reference any object.

## Instructions
An *instruction* contains an op-code and maybe parameters. The interesting
instructions are:

1. set_reg
1. color
1. get
1. power
1. pause
1. time_wait

### Set Register - set_reg
This is the only instruction with any parameters: register name and its value.
This instruction stores the given value in the register of the given name.
If the name is not that of a valid register, it will be stored but never used. 

### Set Color - color
To execute the "color" command, the VM reads the values from its `hue`, 
`saturation`, `brightness`, and `kelvin` registers to assemble a color for the
target device. If the `operand` register contains "light", the `name` register is
assumed to contain the name of a light. Correspondingly, if `operand` contains
"group" or "location", the `name` register will be treated as the name of a
group or location. If the `name` register is empty, the VM will set *all* lights
to that color, regardless of the contents of `operand`.

If `operand` contains "group" or "location", the VM will perform the operation
(set the color pr power) on all of the lights within that collection.

### Get Color - get
This command retrieves current color information from lights themselves and sets
the registers accordingly. The affected registers are hug, saturation,
brightness, and kelvin.

The "operand" register determines the source of the color data. If it contains
`light`, the "name" register is assumed to contain the light's name, and the
colors are retrieved from light with that name. If the "name" register is empty,
all lights are examined, and the arithmetic mean of each setting is stored in
the registers.

If the "operand" register contains `group` or `location	, then the registers 
receive the arithmetic mean of the lights belonging to that group or location.

### Set Power - power
Similar to the `color` instruction, `power` relies on the `operand` and `name`
registers to determine which lights to turn on or off. The content of the
`power` determines whether to turn the lights on or off.
Technically, to remain consistent with the LIFX API, this should be either 0
or 65535. However, the VM will interpret any non-zero or non-False value to
mean turn the lights on, and will send 65535 to the lights.

### Pause for Keypress - pause
Display a message on the console, and wait for the user to press a key. If they
press !, the script will continue to run and ignore any subsequent pause
instructions. Pressing 'q' stops the execution and exits. Any other key resumes
normal execution of the script.

### Time Wait - time
Wait for the given delay to expire. The `time` register contains the delay,
expressed in milliseconds. 

### Operand
Setting the "operand" register indicates what the next "set" or "power"
instrucion will affect. Meaningful values for this register are "light",
"group", and "location". If the register is empty, the behavior is undefined.

The content of this register  determines the meaning of the contents of the VM's
"name" register, which could be a name of a light, the name of a group, or
location.

## Job Scheduling
The controller maintains an internal queue of scripts to execute. When a script
completes, the job scheduler moves on to the next one and launches it. The 
process executing the script runs in a separate thread.

By default, when script finishes, the sceduler discards it. When the queue is
empty, the scheduler effectively becomes idle. However, if "repeat" mode is 
active, completed scripts are immediately added to the end of the queue. The
effect of this is to repeatedly execute all the scripts indefinitely until
a stop is requested.
