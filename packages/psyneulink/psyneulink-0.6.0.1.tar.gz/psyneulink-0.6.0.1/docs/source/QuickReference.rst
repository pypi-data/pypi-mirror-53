Quick Reference
===============

Sections
--------
    * `Conventions`
    * `Repository_Organization`
    * `PsyNeuLink_Objects`
        * `Quick_Reference_Overview`
        * `Quick_Reference_Components`
        * `Quick_Reference_Compositions`
    * `Quick_Reference_Scheduling`
    * `Quick_Reference_Logging`
    * `Quick_Reference_Graphic_Displays`
    * `Quick_Reference_Preferences`

.. _Conventions:

Conventions
-----------

The following conventions are used for the names of PsyNeuLink objects and their documentation:

  + Class (type of object): names use CamelCase (with initial capitalization); the initial mention in a section of
    documentation is formatted as a link (in colored text) to the documentation for that class;
  ..
  + `attribute` or `method` of a `Component` or `Composition`:  names use lower_case_and_underscore; appear in a
    `small box` in documentation;
  ..
  + **argument** of a method or function:  names use lower_case_and_underscore; formatted in **boldface** in
    documentation.
  ..
  + KEYWORD: uses *UPPER_CASE_AND_UNDERSCORE*;  italicized in documentation.
  ..
  + Examples::

          Appear in boxed insets.

See `Naming` for conventions for default and user-assigned names of instances.

.. _Repository_Organization:

Repository Organization
-----------------------

The PsyNeuLink "repo" is organized into two major sections:

`Core`
~~~~~~

This contains the basic PsyNeuLink objects (described in the next section) that are used to build models and run
simulations, and is divided into three subsections:  `Components <Quick_Reference_Components>` (the basic building
blocks of PsyNeuLink models), `Compositions <Quick_Reference_Compositions>` (objects used to combine Components into
models), and `Scheduling <Quick_Reference_Scheduling>` (used to control execution of the Components within a
Composition).

`Library`
~~~~~~~~~

This contains extensions based on the Core objects (under `Compositions` and `Components`), and
PsyNeuLink implementations of published models (under `Models`).  The Library is meant to be extended, and used both
to compare different models that address similar neural mechanisms and/or psychological functions, and to integrate
these into higher level models of system-level function.

.. _PsyNeuLink_Objects:

PsyNeuLink Objects
------------------

.. _Quick_Reference_Overview:

Overview
~~~~~~~~

The two primary types of objects in PsyNeuLink are `Components <Component>` (basic building blocks) and `Compositions
<Composition>` (combinations of Components that implement a model).  There are four primary types of Components:
Functions, Mechanisms, States and Projections.

`Functions <Function>` are the basic units of computation in PsyNeuLink -- every other type of Component in PsyNeuLink
has at least one Function, and sometimes more.  They "package" an executable method that is assigned to a Component's
`function <Component.function>` attribute, and used to carry out the computation for which the Component is
responsible.

`Mechanisms <Mechanism>` are the basic units of processing in a PsyNeuLink model. They have one or more Functions that
perform their characteristic operations.

`States <State>` represent the input(s) and output(s) of a Mechanism, and the parameters of its Function(s).  States
have Functions themselves, that determine the value of the State, and that can be used to modulate that value for
learning, control and/or gating.

`Projections <Projection>` are used to connect Mechanisms, transmit information between them, and to modulate the value
of their States.

Mechanisms and Projections are used to construct `Processes <Process>` -- simple Compositions that comprise a linear
sequence of Mechanisms and Projections. Processes, in turn, can be combined to construct a `System` -- a more complex
Composition used to implement a full PsyNeuLink model. The `figure <QuickReference_Overview_Figure>` below shows
examples of some of the Components (various kinds of Mechanisms and Projections) in PsyNeuLink, combined to form two
Processes and a System.  The sections that follow provide a description of these and the other basic objects in
PsyNeuLink.

.. _QuickReference_Overview_Figure:

.. figure:: _static/Overview_fig.svg

    **Constituents of a PsyNeuLink Model**. Includes examples of some types of Components (Mechanisms and Projections)
    and Compositions (Processes and a System).

.. _Quick_Reference_Components:

`Components <Component>`
~~~~~~~~~~~~~~~~~~~~~~~~

Components are objects that perform a specific function. Every Component has the following core attributes:

* `function <Component.function>` - performs the core computation of the Component (belongs to a PsyNeuLink Function
  assigned to the Component's `function <Component.function>` attribute);

* `variable <Component.variable>` - the input used for the Component's `function <Component.function>`;

* *parameter(s)* - determine how a Component's `function <Component.function>` operates;

* `value <Component.value>` - represents the result of the Component's `function <Component.function>`;

* `name <Component.name>` - string label that uniquely identifies the Component.

The four types of Components in PsyNeuLink, Mechanisms, Projections, States and Functions, are described below:

* `Mechanisms <Mechanism>`
     A Mechanism takes one or more inputs received from its afferent `Projections <Projection>`,
     uses its `function <Mechanism_Base.function>` to combine and/or transform these in some way, and makes the output
     available to other Components.  There are two primary types of Mechanisms in PsyNeuLink:
     ProcessingMechanisms and AdaptiveMechanisms:

     + `ProcessingMechanism`
         Aggregates the inputs it receives from its afferent Projections, transforms them in some way,
         and provides the result as output to its efferent Projections.

     + `AdaptiveMechanism`
         Uses the input it receives from other Mechanisms to modify the parameters of one or more other
         PsyNeuLink Components.  There are three primary types:

         + `LearningMechanism`
             Modifies the matrix of a `MappingProjection`.

         + `ControlMechanism`
             Modifies one or more parameters of other Mechanisms.

         + `GatingMechanism`
             Modifies the value of one or more `InputStates <InputState>` and/or `OutputStates <OutputStates>`
             of other Mechanisms.

* `Projections <Projection>`
   A Projection takes the output of a Mechanism, and transforms it as necessary to provide it
   as the input to another Component. There are two types of Projections, that correspond to the two types of
   Mechanisms:

   + `PathwayProjection`
       Used in conjunction with ProcessingMechanisms to convey information along a processing pathway.
       There is currently one on type of PathwayProjection:

       + `MappingProjection`
         Takes the value of the `OutputState` of one Mechanism, and converts it as necessary to provide it as
         the variable for the `InputState` of another Mechanism.

   + `ModulatoryProjection`
       Used in conjunction with AdaptiveMechanisms to regulate the function of other Components.
       Takes the output of an `AdaptiveMechanism` and uses it to modify the input, output or parameter of
       another Component.  There are three types of ModulatoryProjections, corresponding to the three
       types of AdaptiveMechanisms (see `figure <ModulatorySignal_Anatomy_Figure>`):

       + `LearningProjection`
            Takes a LearningSignal from a `LearningMechanism` and uses it to modify the matrix of a
            MappingProjection.

       + `ControlProjection`
            Takes a ControlSignal from a `ControlMechanism` and uses it to modify the parameter of a
            ProcessingMechanism.

       + `GatingProjection`
            Takes a GatingSignal from a `GatingMechanism` and uses it to modulate the input or output of a
            ProcessingMechanism

* `States <State>`
   A State is a Component that belongs to a `Mechanism` and is used to represent it input(s), the parameter(s)
   of its function, or its output(s).   There are three types of States, one for each type of representation
   (see `figure <Mechanism_Figure>`), each of which can receive and/or send `PathwayProjections <PathwayProjection>`
   and/or `ModulatoryProjections <ModulatoryProjection>` (see `figure <ModulatorySignal_Anatomy_Figure>`):

   + `InputState`
       Represents a set of inputs to the Mechanism.
       Receives one or more afferent PathwayProjections to a Mechanism, combines them using its `function
       <State_Base.function>`, and assigns the result (its `value <State_Base.value>`)as an item of the Mechanism's
       `variable <Mechanism_Base.variable>`.  It can also receive one or more `GatingProjections <GatingProjection>`,
       that modify the parameter(s) of the State's function, and thereby the State's `value <State_Base.value>`.

   + `ParameterState`
       Represents a parameter of the Mechanism's `function <Mechanism_Base.function>`.  Takes the assigned value of the
       parameter as the `variable <State_Base.variable>` for the State's `function <State_Base.function>`, and assigns
       the result as the value of the parameter used by the Mechanism's `function <Mechanism_Base.function>` when the
       Mechanism executes.  It can also receive one or more `ControlProjections <ControlProjection>` that modify
       parameter(s) of the State's `function <State_Base.function>, and thereby the value of the parameters used by the
       Mechanism's `function <Mechanism_Base.function>`.

   + `OutputState`
       Represents an output of the Mechanism.
       Takes an item of the Mechanism's `value <Mechanism_Base.value>` as the `variable <State_Base.variable>` for the
       State's `function <State_Base.function>`, assigns the result as the State's `value <OutputState.value>`, and
       provides that to one or more efferent PathwayProjections.  It can also receive one or more
       `GatingProjections <GatingProjection>`, that modify parameter(s) of the State's function, and thereby the
       State's `value <State_Base.value>`.

* `Functions <Function>`
   A Function is the most fundamental unit of computation in PsyNeuLink.  Every `Component` has a Function
   object, that wraps a callable object (usually an executable function) together with attributes for its parameters.
   This allows parameters to be maintained from one call of a function to the next, for those parameters to be subject
   to modulation by `ModulatoryProjections <ModulatoryProjection>` (see below), and for Functions to be swapped out
   for one another or replaced with customized ones.  PsyNeuLink provides a library of standard Functions (e.g. for
   linear, non-linear, and matrix transformations, integration, and comparison), as well as a standard Application
   Programmers Interface (API) or creating new Functions that can be used to "wrap" any callable object that can be
   written in or called from Python.

.. _Quick_Reference_Compositions:

`Compositions <Composition>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Compositions are combinations of Components that make up a PsyNeuLink model.  There are two primary types of
Compositions:

   + `Processes <Process>`
       One or more `Mechanisms <Mechanism>` connected in a linear chain by `Projections <Projection>`.  A Process can
       have recurrent Projections, but it cannot have any branches.

   + `System`
       A collection of Processes that can have any configuration, and is represented by a graph in which each node is
        a `Mechanism` and each edge is a `Projection`.  Systems are generally constructed from Processes, but they
        can also be constructed directly from Mechanisms and Projections.


.. _Quick_Reference_Compositions__Figure:

**PsyNeuLink Compositions**

.. figure:: _static/System_simple_fig.jpg
   :alt: Overview of major PsyNeuLink Components
   :scale: 50 %

   Two `Processes <Process>` are shown, both belonging to the same `System`.  Each Process has a series of
   `ProcessingMechanisms <ProcessingMechanism>` linked by `MappingProjections <MappingProjection>`, that converge on
   a common final ProcessingMechanism (see figure `above <QuickReference_Overview_Figure>` for a more complete
   example, and `ModulatorySignals <ModulatorySignal_Anatomy_Figure>` for details of Components responsible for
   `learning <LearningMechanism>`, `control <ControlMechanism>` and `gating <GatingMechanism>`).


.. _Quick_Reference_Scheduling:

`Scheduling <Scheduler>`
------------------------

PsyNeuLink Mechanisms can be executed on their own.  However, usually, they are executed when a Composition to which
they belong is executed, under the control of the `Scheduler`.  The Schedule executes Compositions iteratively
in rounds of execution referred to as `PASS` es, in which each Mechanism in the Composition is given an opportunity
to execute;  By default, each Mechanism in a Composition executes exactly once per `PASS`.  However, the Scheduler
can be used to specify one or more `Conditions <Condition>` for each Mechanism that determine whether it executes in
a given `PASS`.  This can be used to determine when a Mechanism begins and/or ends executing, how many times it
executes or the frequency with which it executes relative to other Mechanisms, and any other dependency that can be
expressed in terms of the attributes of other Components in PsyNeuLink. Using a `Scheduler` and a combination of
`pre-specified <Condition_Pre_Specified>` and `custom <Condition_Custom>` Conditions, any pattern of execution can be
 configured that is logically possible.

Using a Scheduler, a Composition continues to execute `PASS` es until its `TRIAL` `termination Condition
<Scheduler_Termination_Conditions>` is met, which constitutes a `TRIAL` of executions.  This is associated with a
single input to the System. Multiple `TRIAL` s (corresponding to a sequences of inputs) can be executed using a
Composition's `run <Composition.run>` method.

.. _Quick_Reference_Logging:

Logging
-------

PsyNeuLink supports logging of any attribute of any `Component` or `Composition` under various specified
conditions.  `Logs <Log>` are dictionaries, with an entry for each Component being logged.  The key for each entry is
the name of the Component, and the value is a record of the Component's `value <Component.value>` recorded under the
conditions specified by its `logPref <Component.logPref>` attribute, specified as a `LogLevel`; each record is a
tuple, the first item of which is a time stamp (the `TIME_STEP` of the `RUN`), the second a string indicating the
context in which the value was recorded, and the third the `value <Component.value>` itself.

.. _Quick_Reference_Graphic_Displays:

Graphic Displays
----------------

At the moment, PsyNeuLink has limited support for graphic displays:  the graph of a `System` can be displayed
using its `show_graph <System.show_graph>` method.  This can be used to display just the processing components
(i.e., `ProcessingMechanisms <ProcessingMechanism>` and `MappingProjections <MappingProjection>`), or to include
`learning <LearningMechanism>` and/or `control <ControlMechanism>` components.  A future release may include
a more complete graphical user interface.


.. _Quick_Reference_Preferences:

Preferences
-----------

PsyNeuLink supports a hierarchical system of `Preferences` for all Components and Compositions.  Every object has its
own set of preferences, as does every class of object.  Any preference for an object can be assigned its own value, or
the default value for any of its parent classes for that preference (e.g., an instance of a `DDM` can be assigned
its own preference for reporting, or use the default value for `ProcessingMechanisms <ProcessingMechanism>`,
`Mechanisms <Mechanism>`, or `Components <Component>`.  There are preferences for reporting (i.e., which results of
processing are printed to the console during execution), logging, levels of warnings, and validation (useful for
debugging, but suppressible for efficiency of execution).
