# Princeton University licenses this file to You under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.  You may obtain a copy of the License at:
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.


# **********************************************  Projection ***********************************************************

"""
..
Sections
--------
      * `Projection_Overview`
      * `Projection_Creation`
      * `Projection_Structure`
         * `Projection_Sender`
         * `Projection_Receiver`
      * `Projection_Execution`
      * `Projection_Class_Reference`

.. _Projection_Overview:

Overview
--------

Projections allow information to be passed between `Mechanisms <Mechanism>`.  A Projection takes its input from
its `sender <Projection_Base.sender>` and transmits that information to its `receiver <Projection_Base.receiver>`.  The
`sender <Projection_Base.sender>` and `receiver <Projection_Base.receiver>` of a Projection are always `States <State>`:
the `sender <Projection_Base.sender>` is always the `OutputState` of a `Mechanism <Mechanism>`; the `receiver
<Projection_Base.receiver>` depends upon the type of Projection.  There are two broad categories of Projections,
each of which has subtypes that differ in the type of information they transmit, how they do this, and the type of
`State <State>` to which they project (i.e., of their `receiver <Projection_Base.receiver>`):

* `PathwayProjection <PathwayProjection>`
    Used in conjunction with `ProcessingMechanisms <ProcessingMechanism>` to convey information along a processing
    `pathway <Process.pathway>`.  There is currently one on type of PathwayProjection:

  * `MappingProjection`
      takes the `value <OutputState.value>` of an `OutputState` of a `ProcessingMechanism <ProcessingMechanism>`
      converts it by convolving it with the MappingProjection's `matrix <MappingProjection.MappingProjection.matrix>`
      parameter, and transmits the result to the `InputState` of another ProcessingMechanism.  Typically,
      MappingProjections are used to connect Mechanisms in the `pathway` of a `Process`, though they can be use for
      other purposes as well (for example, to convey the output of an `ObjectiveMechanism` to a `ModulatoryMechanism
      <ModulatoryMechanism>`).

* `ModulatoryProjection <ModulatoryProjection>`
    takes the `value <OutputState.value>` of a `ModulatorySignal <ModulatorySignal>` of a `ModulatoryMechanism
    <ProcessingMechanism>`, uses it to regulate modify the `value <State_Base.value>` of an `InputState`,
    `ParameterState` or `OutputState` of another Component.  ModulatorySignals are specialized types of `OutputState`,
    that are used to specify how to modify the `value <State_Base.value>` of the `State <State>` to which a
    ModulatoryProjection projects. There are three types of ModulatoryProjections, corresponding to the three types
    of ModulatoryMechanisms (and corresponding ModulatorySignals; see `figure <ModulatorySignal_Anatomy_Figure>`),
    that project to different types of `States <State>`:

  * `LearningProjection`
      takes the `value <LearningSignal.value>` of a `LearningSignal` of a `LearningMechanism`, and transmits
      this to the `ParameterState` of a `MappingProjection` that uses this to modify its `matrix
      <MappingProjection.MappingProjection.matrix>` parameter. LearningProjections are used when learning has
      been specified for a `Process <Process_Learning_Sequence>` or `System <System_Execution_Learning>`.
  ..
  * `ControlProjection`
      takes the `value <ControlSignal.value>` of a `ControlSignal` of a `ControlMechanism <ControlMechanism>`, and
      transmit this to the `ParameterState of a `ProcessingMechanism <ProcessingMechanism>` that uses this to modify
      the parameter of the (or its `function <Mechanism_Base.function>`) for which it is responsible.
      ControlProjections are used when control has been used specified for a `System`.
  ..
  * `GatingProjection`
      takes the `value <GatingSignal.value>` of a `GatingSignal` of a `GatingMechanism`, and transmits this to
      the `InputState` or `OutputState` of a `ProcessingMechanism <ProcessingMechanism>` that uses this to modify the
      State's `value <State_Base.value>`

.. _Projection_Creation:

Creating a Projection
---------------------

A Projection can be created on its own, by calling the constructor for the desired type of Projection.  More
commonly, however, Projections are either specified `in context <Projection_Specification>`, or are `created
automatically <Projection_Automatic_Creation>`, as described below.


.. _Projection_Specification:

*Specifying a Projection*
~~~~~~~~~~~~~~~~~~~~~~~~~

Projections can be specified in a number of places where they are required or permitted, for example in the
specification of a `pathway <Process.pathway>` for a `Process`, where the value of a parameter is specified
(e.g., to assign a `ControlProjection`) or where a `MappingProjection` is specified  (to assign it a
`LearningProjection <MappingProjection_Tuple_Specification>`).  Any of the following can be used to specify a
Projection in context:

  * **Constructor** -- used the same way in context as it is ordinarily.
  ..
  * **Projection object** -- must be a reference to a Projection that has already been created.
  ..
  * **Projection subclass** -- creates a default instance of the specified Projection type.  The assignment or creation
    of the Projection's `sender <Projection_Base.sender>` is handled in the same manner as described below for keyword
    specifications.
  ..
  * **Keyword** -- creates a default instance of the specified type, which can be any of the following:

      * *MAPPING_PROJECTION* -- if the `sender <MappingProjection.sender>` and/or its `receiver
        <MappingProjection.receiver>` cannot be inferred from the context in which this specification occurs, then its
        `initialization is deferred <MappingProjection_Deferred_Initialization>` until both of those have been
        determined (e.g., it is used in the specification of a `pathway <Process.pathway>` for a `Process`). For
        MappingProjections, a `matrix specification <Mapping_Matrix_Specification>` can also be used to specify the
        projection (see **value** below).
      COMMENT:

      * *LEARNING_PROJECTION*  (or *LEARNING*) -- this can only be used in the specification of a `MappingProjection`
        (see `tuple <Mapping_Matrix_Specification>` format).  If the `receiver <MappingProjection.receiver>` of the
        MappingProjection projects to a `LearningMechanism` or a `ComparatorMechanism` that projects to one, then a
        `LearningSignal` is added to that LearningMechanism and assigned as the LearningProjection's `sender
        <LearningProjection.sender>`;  otherwise, a LearningMechanism is `automatically created
        <LearningMechanism_Creation>`, along with a LearningSignal that is assigned as the LearningProjection's `sender
        <LearningProjection.sender>`. See `LearningMechanism_Learning_Configurations` for additional details.
      COMMENT

      * *CONTROL_PROJECTION* (or *CONTROL*) -- this can be used when specifying a parameter using the `tuple format
        <ParameterState_Tuple_Specification>`, to create a default `ControlProjection` to the `ParameterState` for that
        parameter.  If the `Component <Component>` to which the parameter belongs is part of a `System`, then a
        `ControlSignal` is added to the System's `controller <System.controller>` and assigned as the
        ControlProjection's `sender <ControlProjection.sender>`;  otherwise, the ControlProjection's `initialization
        is deferred <ControlProjection_Deferred_Initialization>` until the Mechanism is assigned to a System,
        at which time the ControlSignal is added to the System's `controller <System.controller>` and assigned
        as its the ControlProjection's `sender <ControlProjection.sender>`.  See `ControlMechanism_Control_Signals` for
        additional details.

      * *GATING_PROJECTION* (or *GATING*) -- this can be used when specifying an `InputState
        <InputState_Projection_Source_Specification>` or an `OutputState <OutputState_Projections>`, to create a
        default `GatingProjection` to the `State <State>`. If the GatingProjection's `sender <GatingProjection.sender>`
        cannot be inferred from the context in which this specification occurs, then its `initialization is deferred
        <GatingProjection_Deferred_Initialization>` until it can be determined (e.g., a `GatingMechanism` or
        `GatingSignal` is created to which it is assigned).
  ..
  * **value** -- creates a Projection of a type determined by the context of the specification, and using the
    specified value as the `value <Projection_Base.value>` of the Projection, which must be compatible with the
    `variable <State_Base.variable>` attribute of its `receiver <Projection_Base.receiver>`.  If the Projection is a
    `MappingProjection`, the value is interpreted as a `matrix specification <Mapping_Matrix_Specification>` and
    assigned as the `matrix <MappingProjection.matrix>` parameter of the Projection;  it must be compatible with the
    `value <State_Base.value>` attribute of its `sender <MappingProjection.sender>` and `variable <State_Base.variable>`
    attribute of its `receiver <MappingProjection.receiver>`.
  ..
  * **Mechanism** -- creates a `MappingProjection` to either the `primary InputState <InputState_Primary>` or
    `primary OutputState <OutputState_Primary>`, depending on the type of Mechanism and context of the specification.
  ..
  * **State** -- creates a `Projection` to or from the specified `State`, depending on the type of State and the
    context of the specification.

  .. _Projection_Specification_Dictionary:

  * **Specification dictionary** -- can contain an entry specifying the type of Projection, and/or entries
    specifying the value of parameters used to instantiate it. These should take the following form:

      * *PROJECTION_TYPE*: *<name of a Projection type>* --
        if this entry is absent, a default Projection will be created that is appropriate for the context
        (for example, a `MappingProjection` for an `InputState`, a `LearningProjection` for the `matrix
        <MappingProjection.matrix>` parameter of a `MappingProjection`, and a `ControlProjection` for any other
        type of parameter.

      * *PROJECTION_PARAMS*: *Dict[Projection argument, argument value]* --
        the key for each entry of the dictionary must be the name of a Projection parameter, and its value the value
        of the parameter.  It can contain any of the standard parameters for instantiating a Projection (in particular
        its `sender <Projection_Sender>` and `receiver <Projection_Receiver>`, or ones specific to a particular type
        of Projection (see documentation for subclass).  If the `sender <Projection_Sender>` and/or
        `receiver <Projection_Receiver>` are not specified, their assignment and/or creation are handled in the same
        manner as described above for keyword specifications.

      COMMENT:
          WHAT ABOUT SPECIFICATION USING OutputState/ModulatorySignal OR Mechanism? OR Matrix OR Matrix keyword
      COMMENT

      COMMENT:  ??IMPLEMENTED FOR PROJECTION PARAMS??
        Note that parameter
        values in the specification dictionary will be used to instantiate the Projection.  These can be overridden
        during execution by specifying `runtime parameters <Mechanism_Runtime_parameters>` for the Projection,
        either when calling the `execute <Mechanism_Base.execute>` or `run <Mechanism_Base.run>`
        method for a Mechanism directly, or where it is specified in the `pathway` of a Process.
      COMMENT

  .. _Projection_ProjectionTuple:

  * **ProjectionTuple** -- a 4-item tuple used in the context of a `State specification <State_Specification>` to
    create a Projection between it and another `State <State>`. It must have at least the first three of the following
    items in order, and can include the fourth optional item:

     * **State specification** -- specifies the `State <State_Specification>` to connect with (**not** the one being
       connected; that is determined from context)

     * **weight** -- must be a value specifying the `weight <Projection_Base.weight>` of the Projection;  it can be
       `None`, in which case it is ignored, but there must be a specification present;

     * **exponent** -- must be a value specifying the `exponent <Projection_Base.exponent>` of the Projection;  it
       can be `None`, in which case it is ignored, but there must be a specification present;

     * **Projection specification** -- this is optional but, if included, msut be a `Projection specification
       <Projection_Specification>`;  it can take any of the forms of a Projection specification described above for
       any Projection subclass; it can be used to provide additional specifications for the Projection, such as its
       `matrix <MappingProjection.matrix>` if it is a `MappingProjection`.

    .. note::
       A ProjectionTuple should not be confused with a `4-item InputState specification tuple
       <InputState_Tuple_Specification>`, which also contains weight and exponent items.  In a ProjectionTuple, those
       items specify the weight and/or exponent assigned to the *Projection* (see `Projection_Weight_Exponent`),
       whereas in an `InputState specification tuple <InputState_Weights_And_Exponents>` they specify the weight
       and/or exponent of the **InputState**.

    Any (but not all) of the items can be `None`.  If the State specification is `None`, then there must be a
    Projection specification (used to infer the State to be connected with).  If the Projection specification is
    `None` or absent, the State specification cannot be `None` (as it is then used to infer the type of Projection).
    If weight and/or exponent is `None`, it is ignored.  If both the State and Projection are specified, they must
    be compatible  (see `examples <State_Projections_Examples>` in State).


.. _Projection_Automatic_Creation:

*Automatic creation*
~~~~~~~~~~~~~~~~~~~~

Under some circumstances Projections are created automatically. For example, a `Process` automatically creates a
`MappingProjection` between adjacent `ProcessingMechanisms <ProcessingMechanism>` in its `pathway
<Process.pathway>` if none is specified; and `LearningProjections <LearningProjection>` are automatically created
when :keyword:`learning` is specified for a `Process <Process_Learning_Sequence>` or `System
<System_Execution_Learning>`).

.. _Projection_Deferred_Initialization:

*Deferred Initialization*
~~~~~~~~~~~~~~~~~~~~~~~~~

When a Projection is created, its full initialization is `deferred <Component_Deferred_Init>` until its `sender
<Projection_Base.sender>` and `receiver <Projection_Base.receiver>` have been fully specified.  This allows a
Projection to be created before its `sender <Projection_Base.sender>` and/or `receiver <Projection_Base.receiver>` have
been created (e.g., before them in a script), by calling its constructor without specifying its **sender** or
**receiver** arguments. However, for the Projection to be operational, initialization must be completed by calling
its `_deferred_init` method.  Under most conditions this occurs automatically (e.g., when the projection is assigned
to a type of Component that expects to be the `sender <Projection_Base.sender>` or `receiver <Projection_Base.receiver>`
for that type of Projection); these conditions are described in the section on *Deferred Initialization* for each type
of Projection.  Otherwise, the  Projection's `_deferred_init` method must be called explicitly, once the missing
attribute assignments have been made.


.. _Projection_Structure:

Structure
---------

In addition to its `function <Projection_Base.function>`, a Projection has two primary attributes: a `sender
<Projection_Base.sender>` and `receiver <Projection_Base.receiver>`.  The types of `State(s) <State>` that can be
assigned to these, and the attributes of those States to which Projections of each type are assigned, are
summarized in the following table, and described in greater detail in the subsections below.  In addition to the
State attributes to which different types of Projections are assigned (shown in the table), all of the Projections
of a State are listed in its `projections <State_Base.projections>` attribute.

.. _Projection_Table:

.. table:: **Sender, Receiver and Attribute Assignments for Projection Types**
    :align: center

    +----------------------+---------------------------------------+--------------------------------------------------+
    |     Projection       |   sender                              |  receiver                                        |
    |                      |   *(attribute)*                       |  *(attribute)*                                   |
    +======================+=======================================+==================================================+
    | `MappingProjection`  | `OutputState`                         | `InputState`                                     |
    |                      | (`efferents <OutputState.efferents>`) | (`path_afferents <InputState.path_afferents>`)   |
    +----------------------+---------------------------------------+--------------------------------------------------+
    | `LearningProjection` | `LearningSignal`                      | `ParameterState`                                 |
    |                      | (`efferents <OutputState.efferents>`) | (`mod_afferents <ParameterState.mod_afferents>`) |
    +----------------------+---------------------------------------+--------------------------------------------------+
    | `ControlProjection`  | `ControlSignal`                       | `ParameterState`                                 |
    |                      | (`efferents <OutputState.efferents>`) | (`mod_afferents <ParameterState.mod_afferents>`) |
    +----------------------+---------------------------------------+--------------------------------------------------+
    | `GatingProjection`   | `GatingSignal`                        | `InputState` or `OutputState`                    |
    |                      | (`efferents <OutputState.efferents>`) | (`mod_afferents <State_Base.mod_afferents>`)     |
    +----------------------+---------------------------------------+--------------------------------------------------+

.. _Projection_Sender:

*Sender*
~~~~~~~~

This must be an `OutputState` or a `ModulatorySignal <ModulatorySignal>` (a subclass of OutputState specialized for
`ModulatoryProjections <ModulatoryProjection>`).  The Projection is assigned to the OutputState or ModulatorySignal's
`efferents <State_Base.efferents>` list and, for ModulatoryProjections, to the list of ModulatorySignals specific to
the `ModulatoryMechanism <ModulatoryMechanism>` from which it projects.  The OutputState or ModulatorySignal's `value
<OutputState.value>` is used as the `variable <Function.variable>` for Projection's `function
<Projection_Base.function>`.

A sender can be specified as:

  * an **OutputState** or **ModulatorySignal**, as appropriate for the Projection's type, using any of the ways for
    `specifying an OutputState <OutputState_Specification>`.
  ..
  * a **Mechanism**;  for a `MappingProjection`, the Mechanism's `primary OutputState <OutputState_Primary>` is
    assigned as the `sender <Projection_Base.sender>`; for a `ModulatoryProjection <ModulatoryProjection>`, a
    `ModulatorySignal <ModulatorySignal>` of the appropriate type is created and assigned to the Mechanism.

If the `sender <Projection_Base.sender>` is not specified and it can't be determined from the context, or an OutputState
specification is not associated with a Mechanism that can be determined from , then the initialization of the
Projection is `deferred <Projection_Deferred_Initialization>`.

.. _Projection_Receiver:

*Receiver*
~~~~~~~~~~

The `receiver <Projection_Base.receiver>` required by a Projection depends on its type, as listed below:

    * MappingProjection: `InputState`
    * LearningProjection: `ParameterState` (for the `matrix <MappingProjection>` of a `MappingProjection`)
    * ControlProjection: `ParameterState`
    * GatingProjection: `InputState` or OutputState`

A `MappingProjection` (as a `PathwayProjection <PathwayProjection>`) is assigned to the `path_afferents
<State.path_afferents>` attribute of its `receiver <Projection_Base.receiver>`.  The ModulatoryProjections are assigned
to the `mod_afferents <State.mod_afferents>` attribute of their `receiver <Projection_Base.receiver>`.

A `receiver <Projection_Base.receiver>` can be specified as:

  * an existing **State**;
  ..
  * an existing **Mechanism** or **Projection**; which of these is permissible, and how a state is assigned to it, is
    determined by the type of Projection — see subclasses for details).
  ..
  * a **specification dictionary** (see subclasses for details).

.. _Projection_Weight_Exponent:

*Weight and Exponent*
~~~~~~~~~~~~~~~~~~~~~

Every Projection has a `weight <Projection_Base.weight>` and `exponent <Projection_Base.exponent>` attribute. These
are applied to its `value <Projection_Base.value>` before combining it with other Projections that project to the same
`State`.  If both are specified, the `exponent <Projection_Base.exponent>` is applied before the `weight
<Projection_Base.weight>`.  These attributes determine both how the Projection's `value <Projection.value>` is combined
with others to determine the `variable <State_Base.variable>` of the State to which they project.

.. note::
   The `weight <Projection_Base.weight>` and `exponent <Projection_Base.exponent>` attributes of a Projection are not
   the same as a State's `weight <State_Base.weight>` and `exponent <State_Base.exponent>` attributes.  Also, they are
   not normalized: their aggregate effects contribute to the magnitude of the `variable <State.variable>` to which
   they project.


*ParameterStates and Parameters*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`ParameterStates <ParameterState>` provide the value for each parameter of a Projection and its `function
<Mechanism_Base.function>`.  ParameterStates and their associated parameters are handled in the same way by
Projections as they are for Mechanisms (see `Mechanism_ParameterStates` for details).  The ParameterStates for a
Projection are listed in its `parameter_states <Projection_Base.parameter_states>` attribute.


.. _Projection_Execution:

Execution
---------

A Projection cannot be executed directly.  It is executed when the `State <State>` to which it projects (i.e., its
`receiver <Projection_Base.receiver>`) is updated;  that occurs when the State's owner `Mechanism <Mechanism>` is
executed. When a Projection executes, it gets the value of its `sender <Projection_Base.sender>`, assigns this as the
`variable <Projection_Base.variable>` of its `function <Projection_Base.function>`, calls the `function
<Projection_Base.function>`, and provides the result as to its `receiver <Projection_Base.receiver>`.  The `function
<Projection_Base.function>` of a Projection converts the value received from its `sender <Projection_Base.sender>` to
a form suitable as input for its `receiver <Projection_Base.receiver>`.


COMMENT:
*** ADD EXAMPLES

GET FROM Scratch Pad

for example, if a ProjectionTuple is used in the context of an
    `InputState specification
    <InputState_Specification>` to specify a MappingProjection to it from an `OutputState` that is specified
    in the first item of the tuple, and a Projection specification is included in the fourth, its sender (and/or the
    sending dimensions of its `matrix <MappingProjection.matrix>` parameter) must be compatible with the specified
    OutputState (see `examples <XXX>` below)

COMMENT

.. _Projection_Class_Reference:

"""
import abc
import inspect
import itertools
import warnings

import numpy as np
import typecheck as tc

from psyneulink.core.components.component import Component
from psyneulink.core.components.functions.transferfunctions import LinearMatrix, get_matrix
from psyneulink.core.components.shellclasses import Mechanism, Process_Base, Projection, State
from psyneulink.core.components.states.modulatorysignals.modulatorysignal import _is_modulatory_spec
from psyneulink.core.components.states.state import StateError
from psyneulink.core.globals.context import ContextFlags
from psyneulink.core.globals.keywords import CONTROL, CONTROL_PROJECTION, CONTROL_SIGNAL, EXPONENT, FUNCTION_PARAMS, GATING, GATING_PROJECTION, GATING_SIGNAL, INPUT_STATE, LEARNING, LEARNING_PROJECTION, LEARNING_SIGNAL, MAPPING_PROJECTION, MATRIX, MATRIX_KEYWORD_SET, MECHANISM, MODEL_SPEC_ID_RECEIVER_MECH, MODEL_SPEC_ID_RECEIVER_STATE, MODEL_SPEC_ID_SENDER_MECH, MODEL_SPEC_ID_SENDER_STATE, NAME, OUTPUT_STATE, OUTPUT_STATES, PARAMS, PATHWAY, PROJECTION, PROJECTION_PARAMS, PROJECTION_SENDER, PROJECTION_TYPE, RECEIVER, SENDER, STANDARD_ARGS, STATE, STATES, WEIGHT, ADD_INPUT_STATE, ADD_OUTPUT_STATE, PROJECTION_COMPONENT_CATEGORY
from psyneulink.core.globals.parameters import Parameter
from psyneulink.core.globals.preferences.preferenceset import PreferenceLevel
from psyneulink.core.globals.registry import register_category
from psyneulink.core.globals.socket import ConnectionInfo
from psyneulink.core.globals.utilities import ContentAddressableList, is_matrix, is_numeric

__all__ = [
    'Projection_Base', 'projection_keywords', 'PROJECTION_SPEC_KEYWORDS',
    'ProjectionError', 'DuplicateProjectionError', 'ProjectionRegistry',
    'kpProjectionTimeScaleLogEntry'
]

ProjectionRegistry = {}

kpProjectionTimeScaleLogEntry = "Projection TimeScale"

projection_keywords = set()

PROJECTION_ARGS = {PROJECTION_TYPE, SENDER, RECEIVER, WEIGHT, EXPONENT} | STANDARD_ARGS

PROJECTION_SPEC_KEYWORDS = {PATHWAY: MAPPING_PROJECTION,
                            LEARNING: LEARNING_PROJECTION,
                            LEARNING_SIGNAL: LEARNING_PROJECTION,
                            LEARNING_PROJECTION: LEARNING_PROJECTION,
                            CONTROL: CONTROL_PROJECTION,
                            CONTROL_SIGNAL: CONTROL_PROJECTION,
                            CONTROL_PROJECTION: CONTROL_PROJECTION,
                            GATING: GATING_PROJECTION,
                            GATING_SIGNAL: GATING_PROJECTION,
                            GATING_PROJECTION: GATING_PROJECTION
                            }

from collections import namedtuple
ProjectionTuple = namedtuple("ProjectionTuple", "state, weight, exponent, projection")


class ProjectionError(Exception):
    def __init__(self, error_value):
        self.error_value = error_value

class DuplicateProjectionError(Exception):
    def __init__(self, error_value):
        self.error_value = error_value

    def __str__(self):
        return repr(self.error_value)

# Projection factory method:
# def projection(name=NotImplemented, params=NotImplemented, context=None):
#         """Instantiates default or specified subclass of Projection
#
#         If called w/o arguments or 1st argument=NotImplemented, instantiates default subclass (ParameterState)
#         If called with a name string:
#             - if registered in ProjectionRegistry class dictionary as name of a subclass, instantiates that class
#             - otherwise, uses it as the name for an instantiation of the default subclass, and instantiates that
#         If a params dictionary is included, it is passed to the subclass
#
#         :param name:
#         :param param_defaults:
#         :return:
#         """
#
#         # Call to instantiate a particular subclass, so look up in MechanismRegistry
#         if name in ProjectionRegistry:
#             return ProjectionRegistry[name].mechanismSubclass(params)
#         # Name is not in MechanismRegistry or is not provided, so instantiate default subclass
#         else:
#             # from Components.Defaults import DefaultProjection
#             return DefaultProjection(name, params)
#

class Projection_Base(Projection):
    """
    Projection_Base(  \
    receiver,         \
    sender=None,      \
    params=None,      \
    name=None,        \
    prefs=None)

    Base class for all Projections.

    .. note::
       Projection is an abstract class and should NEVER be instantiated by a direct call to its constructor.
       It should be created by calling the constructor for a subclass` or by using any of the other methods for
       `specifying a Projection <Projection_Specification>`.


    COMMENT:
        Description
        -----------
            Projection category of Component class (default type:  MappingProjection)

        Gotchas
        -------
            When referring to the Mechanism that is a Projection's sender or receiver Mechanism, must add ".owner"

        Class attributes
        ----------------
            + componentCategory (str): kwProjectionFunctionCategory
            + className (str): kwProjectionFunctionCategory
            + suffix (str): " <className>"
            + registry (dict): ProjectionRegistry
            + classPreference (PreferenceSet): ProjectionPreferenceSet, instantiated in __init__()
            + classPreferenceLevel (PreferenceLevel): PreferenceLevel.CATEGORY
            + class_defaults.variable (value): [0]
            + requiredParamClassDefaultTypes = {PROJECTION_SENDER: [str, Mechanism, State]}) # Default sender type
            + paramClassDefaults (dict)
            + FUNCTION (Function class or object, or method)

        Class methods
        -------------
            None

        ProjectionRegistry
        ------------------
            All Projections are registered in ProjectionRegistry, which maintains a dict for each subclass,
              a count for all instances of that type, and a dictionary of those instances
    COMMENT


    Attributes
    ----------

    variable : value
        input to Projection, received from `value <OutputState.value>` of `sender <Projection_Base.sender>`.

    sender : State
        State from which Projection receives its input (see `Projection_Sender` for additional information).

    receiver : State
        State to which Projection sends its output  (see `Projection_Receiver` for additional information)

    value : value
        output of Projection, transmitted to variable of function of its `receiver <Projection_Base.receiver>`.

    parameter_states : ContentAddressableList[str, ParameterState]
        a list of the Projection's `ParameterStates <Projection_ParameterStates>`, one for each of its specifiable
        parameters and those of its `function <Mechanism_Base.function>` (i.e., the ones for which there are
        arguments in their constructors).  The value of the parameters of the Projection are also accessible as
        attributes of the Projection (using the name of the parameter); the function parameters are listed in the
        Projection's `function_params <Projection_Base.function_params>` attribute, and as attributes of the `Function`
        assigned to its `function <Component.function>` attribute.

    parameter_states : ContentAddressableList[str, ParameterState]
        a read-only list of the Projection's `ParameterStates <Mechanism_ParameterStates>`, one for each of its
        `configurable parameters <ParameterState_Configurable_Parameters>`, including those of its `function
        <Projection_Base.function>`.  The value of the parameters of the Projection and its `function
        <Projection_Base.function>` are also accessible as (and can be modified using) attributes of the Projection,
        in the same manner as they can for a `Mechanism <Mechanism_ParameterStates>`).

    weight : number
       multiplies the `value <Projection_Base.value>` of the Projection after applying the `exponent
       <Projection_Base.exponent>`, and before combining with any other Projections that project to the same `State`
       to determine that State's `variable <State_Base.variable>`.

    exponent : number
        exponentiates the `value <Projection_Base.value>` of the Projection, before applying `weight
        <Projection_Base.weight>`, and before combining it with any other Projections that project to the same
        `State` to determine that State's `variable <State_Base.variable>`.

    COMMENT:
        projectionSender : Mechanism, State, or Object
            This is assigned by __init__.py with the default sender state for each subclass.
            It is used if sender arg is not specified in the constructor or when the Projection is assigned.
            If it is different than the default;  where it is used, it overrides the ``sender`` argument even if that is
            provided.

        projectionSender : 1d array
            Used to instantiate projectionSender
    COMMENT

    name : str
        the name of the Projection. If the Projection's `initialization has been deferred
        <Projection_Deferred_Initialization>`, it is assigned a temporary name (indicating its deferred initialization
        status) until initialization is completed, at which time it is assigned its designated name.  If that is the
        name of an existing Projection, it is appended with an indexed suffix, incremented for each Projection with the
        same base name (see `Naming`). If the name is not  specified in the **name** argument of its constructor, a
        default name is assigned by the subclass (see subclass for details)

    prefs : PreferenceSet or specification dict
        the `PreferenceSet` for the Projection; if it is not specified in the **prefs** argument of the constructor,
        a default is assigned using `classPreferences` defined in __init__.py (see :doc:`PreferenceSet <LINK>` for
        details).

    """

    color = 0

    componentCategory = PROJECTION_COMPONENT_CATEGORY
    className = componentCategory
    suffix = " " + className

    class Parameters(Projection.Parameters):
        """
            Attributes
            ----------

                exponent
                    see `exponent <Projection_Base.exponent>`

                    :default value: None
                    :type:

                function
                    see `function <Projection_Base.function>`

                    :default value: `LinearMatrix`
                    :type: `Function`

                weight
                    see `weight <Projection_Base.weight>`

                    :default value: None
                    :type:

        """
        weight = Parameter(None, modulable=True)
        exponent = Parameter(None, modulable=True)
        function = Parameter(LinearMatrix, stateful=False, loggable=False)

    registry = ProjectionRegistry

    classPreferenceLevel = PreferenceLevel.CATEGORY

    requiredParamClassDefaultTypes = Component.requiredParamClassDefaultTypes.copy()
    requiredParamClassDefaultTypes.update({PROJECTION_SENDER: [str, Mechanism, State]}) # Default sender type

    @abc.abstractmethod
    def __init__(self,
                 receiver,
                 sender=None,
                 weight=None,
                 exponent=None,
                 function=None,
                 params=None,
                 name=None,
                 prefs=None,
                 context=None,
                 ):
        """Assign sender, receiver, and execute method and register Mechanism with ProjectionRegistry

        This is an abstract class, and can only be called from a subclass;
           it must be called by the subclass with a context value

        # DOCUMENT:  MOVE TO ABOVE, UNDER INSTANTIATION
        Initialization arguments:
            - sender (Mechanism, State or dict):
                specifies source of input to Projection (default: senderDefault)
            - receiver (Mechanism, State or dict)
                 destination of Projection (default: none)
            - params (dict) - dictionary of Projection params:
                + FUNCTION:<method>
        - name (str): if it is not specified, a default based on the class is assigned in register_category,
                            of the form: className+n where n is the n'th instantiation of the class
            - prefs (PreferenceSet or specification dict):
                 if it is omitted, a PreferenceSet will be constructed using the classPreferences for the subclass
                 dict entries must have a preference keyPath as key, and a PreferenceEntry or setting as their value
                 (see Description under PreferenceSet for details)
            - context (str): must be a reference to a subclass, or an exception will be raised

        NOTES:
        * Receiver is required, since can't instantiate a Projection without a receiving State
        * If sender and/or receiver is a Mechanism, the appropriate State is inferred as follows:
            MappingProjection:
                sender = <Mechanism>.output_state
                receiver = <Mechanism>.input_state
            ControlProjection:
                sender = <Mechanism>.output_state
                receiver = <Mechanism>.paramsCurrent[<param>] IF AND ONLY IF there is a single one
                            that is a ParameterState;  otherwise, an exception is raised
        * _instantiate_sender, _instantiate_receiver must be called before _instantiate_function:
            - _validate_params must be called before _instantiate_sender, as it validates PROJECTION_SENDER
            - instantatiate_sender may alter self.defaults.variable, so it must be called before _validate_function
            - instantatiate_receiver must be called before _validate_function,
                 as the latter evaluates receiver.value to determine whether to use self.function or FUNCTION
        * If variable is incompatible with sender's output, it is set to match that and revalidated (_instantiate_sender)
        * if FUNCTION is provided but its output is incompatible with receiver value, self.function is tried
        * registers Projection with ProjectionRegistry

        :param sender: (State or dict)
        :param receiver: (State or dict)
        :param param_defaults: (dict)
        :param name: (str)
        :param context: (str)
        :return: None
        """
        from psyneulink.core.components.states.parameterstate import ParameterState
        from psyneulink.core.components.states.state import State_Base

        params = self._assign_args_to_param_dicts(weight=weight,
                                                  exponent=exponent,
                                                  params=params)

        if self.initialization_status == ContextFlags.DEFERRED_INIT:
            self._assign_deferred_init_name(name, context)
            self.init_args = locals().copy()
            self.init_args[NAME] = name

            # remove local imports
            del self.init_args['ParameterState']
            del self.init_args['State_Base']
            return

        self.receiver = receiver

         # Register with ProjectionRegistry or create one
        register_category(entry=self,
                          base_class=Projection_Base,
                          name=name,
                          registry=ProjectionRegistry,
                          context=context)

        # Create projection's _stateRegistry and ParameterState entry
        self._stateRegistry = {}

        register_category(entry=ParameterState,
                          base_class=State_Base,
                          registry=self._stateRegistry,
                          context=context)

        self._instantiate_sender(sender, context=context)

        # FIX: ADD _validate_variable, THAT CHECKS FOR SENDER?
        # FIX: NEED TO KNOW HERE IF SENDER IS SPECIFIED AS A MECHANISM OR STATE
        try:
            # this should become _default_value when that is fully implemented
            variable = self.sender.defaults.value
        except AttributeError:
            if receiver.prefs.verbosePref:
                warnings.warn("Unable to get value of sender ({0}) for {1};  will assign default ({2})".
                              format(self.sender, self.name, self.class_defaults.variable))
            variable = None

        # Assume that if receiver was specified as a Mechanism, it should be assigned to its (primary) InputState
        # MODIFIED 11/1/17 CW: Added " hasattr(self, "prefs") and" in order to avoid errors. Otherwise, this was being
        # called and yielding an error: " AttributeError: 'MappingProjection' object has no attribute '_prefs' "

        if isinstance(self.receiver, Mechanism):
            if (len(self.receiver.input_states) > 1 and hasattr(self, 'prefs') and
                    (self.prefs.verbosePref or self.receiver.prefs.verbosePref)):
                print("{0} has more than one InputState; {1} has been assigned to the first one".
                      format(self.receiver.owner.name, self.name))
            self.receiver = self.receiver.input_state

        if hasattr(self.receiver, "afferents_info"):
            if self not in self.receiver.afferents_info:
                self.receiver.afferents_info[self] = ConnectionInfo()

       # Validate variable, function and params, and assign params to paramInstanceDefaults
        # Note: pass name of Projection (to override assignment of componentName in super.__init__)
        super(Projection_Base, self).__init__(default_variable=variable,
                                              function=function,
                                              param_defaults=params,
                                              name=self.name,
                                              prefs=prefs)

        self._assign_default_projection_name()

    def _validate_params(self, request_set, target_set=None, context=None):
        """Validate PROJECTION_SENDER and/or sender arg (current self.sender), and assign one of them as self.sender

        Check:
        - that PROJECTION_SENDER is a Mechanism or State
        - if it is different from paramClassDefaults[PROJECTION_SENDER], use it
        - if it is the same or is invalid, check if sender arg was provided to __init__ and is valid
        - if sender arg is valid use it (if PROJECTION_SENDER can't be used);
        - if both were not provided, use paramClassDefaults[PROJECTION_SENDER]
        - otherwise, if one was not provided and the other is invalid, generate error
        - when done, sender is assigned to self.sender

        Note: check here only for sender's type, NOT content (e.g., length, etc.); that is done in _instantiate_sender

        :param request_set:
        :param target_set:
        :param context:
        :return:
        """

        super(Projection, self)._validate_params(request_set, target_set, context)

        # FIX: 10/3/17 SHOULD ADD CHECK THAT RECEIVER/SENDER SOCKET SPECIFICATIONS ARE CONSISTENT WITH
        # FIX:         PROJECTION_TYPE SPECIFIED BY THE CORRESPONDING STATE TYPES

        if (PROJECTION_SENDER in target_set and
                not (target_set[PROJECTION_SENDER] in {None, self.paramClassDefaults[PROJECTION_SENDER]})):
            # If PROJECTION_SENDER is specified it will be the sender
            sender = target_set[PROJECTION_SENDER]
            sender_string = PROJECTION_SENDER
        else:
            # PROJECTION_SENDER is not specified or None, so sender argument of constructor will be the sender
            sender = self.sender
            sender_string = "\'{}\' argument".format(SENDER)
        if not ((isinstance(sender, (Mechanism, State)) or
                (inspect.isclass(sender) and issubclass(sender, (Mechanism, State))))):
            raise ProjectionError("Specification of {} for {} ({}) is invalid; "
                                  "it must be a {}, {} or a class of one of these.".
                                  format(sender_string, self.name, sender,
                                         Mechanism.__name__, State.__name__))

    def _instantiate_attributes_before_function(self, function=None, context=None):
        self._instantiate_parameter_states(function=function, context=context)

    def _instantiate_parameter_states(self, function=None, context=None):

        from psyneulink.core.components.states.parameterstate import _instantiate_parameter_states
        _instantiate_parameter_states(owner=self, function=function, context=context)

    def _instantiate_sender(self, sender, context=None):
        """Assign self.sender to OutputState of sender

        Assume self.sender has been assigned in _validate_params, from either sender arg or PROJECTION_SENDER
        Validate, and assign projection to sender's efferents attribute

        If self.sender is a Mechanism, re-assign it to <Mechanism>.output_state
        If self.sender is a State class reference, validate that it is a OutputState
        Assign projection to sender's efferents attribute
        """
        from psyneulink.core.compositions.composition import Composition
        from psyneulink.core.components.states.outputstate import OutputState

        if not (
            isinstance(sender, (Composition, Mechanism, State, Process_Base))
            or (inspect.isclass(sender) and issubclass(sender, (Mechanism, State)))
        ):
            assert False, \
                f"PROGRAM ERROR: Invalid specification for {SENDER} ({sender}) of {self.name} " \
                f"(including paramClassDefaults: {self.paramClassDefaults[PROJECTION_SENDER]})."

        # If self.sender is specified as a Mechanism (rather than a State),
        #     get relevant OutputState and assign it to self.sender
        # IMPLEMENTATION NOTE: Assume that self.sender should be the primary OutputState; if that is not the case,
        #                      self.sender should either be explicitly assigned, or handled in an override of the
        #                      method by the relevant subclass prior to calling super
        if isinstance(sender, Composition):
            sender = sender.output_CIM
        if isinstance(sender, Mechanism):
            sender = sender.output_state
        self.sender = sender

        # At this point, self.sender should be a OutputState
        if not isinstance(self.sender, OutputState):
            raise ProjectionError("Sender specified for {} ({}) must be a Mechanism or an OutputState".
                                  format(self.name, self.sender))

        # Assign projection to self.sender's efferents list attribute
        # First make sure that projection is not already in efferents
        # IMPLEMENTATON NOTE:  Currently disallows *ANY* Projections with same sender and receiver
        #                      (even if they are in different Compositions)
        if self not in self.sender.efferents:
            # Then make sure there is not already a projection to its receiver
            receiver = self.receiver
            if isinstance(receiver, Composition):
                receiver = receiver.input_CIM
            if isinstance(receiver, Mechanism):
                receiver = receiver.input_state
            assert isinstance(receiver, (State)), \
                f"Illegal receiver ({receiver}) detected in _instantiate_sender() method for {self.name}"
            dup = receiver._check_for_duplicate_projections(self)
            # If duplicate is a deferred_init Projection, delete it and use one currently being instantiated
            # IMPLEMENTATION NOTE:  this gives precedence to a Projection to a Component specified by its sender
            #                      (e.g., controller of a Composition for a ControlProjection)
            #                       over its specification in the constructor for the receiver or its owner
            # IMPLEMENTATION NOTE:  This should be removed if/when different Projections are permitted between
            #                       the same sender and receiver in different Compositions
            if dup:
                if dup.initialization_status == ContextFlags.DEFERRED_INIT:
                    del receiver.mod_afferents[receiver.mod_afferents.index(dup)]
                else:
                    raise DuplicateProjectionError(f"Attempt to assign {Projection.__name__} to {receiver.name} of "
                                                   f"{receiver.owner.name} that already has an identical "
                                                   f"{Projection.__name__}.")
            self.sender.efferents.append(self)
        else:
            raise DuplicateProjectionError(f"Attempt to assign {Projection.__name__} from {sender.name} of "
                                           f"{sender.owner.name} that already has an identical {Projection.__name__}.")

    def _instantiate_attributes_after_function(self, context=None):
        from psyneulink.core.components.states.parameterstate import _instantiate_parameter_state
        self._instantiate_receiver(context=context)
        # instantiate parameter states from UDF custom parameters if necessary
        try:
            cfp = self.function.cust_fct_params
            udf_parameters_lacking_states = {param_name: cfp[param_name] for param_name in cfp if param_name not in self.parameter_states.names}

            _instantiate_parameter_state(self, FUNCTION_PARAMS, udf_parameters_lacking_states, context=context, function=self.function)
        except AttributeError:
            pass

        super()._instantiate_attributes_after_function(context=context)

    def _instantiate_receiver(self, context=None):
        """Call receiver's owner to add projection to its afferents list

        Notes:
        * Assume that subclasses implement this method in which they:
          - test whether self.receiver is a Mechanism and, if so, replace with State appropriate for projection
          - calls this method (as super) to assign projection to the Mechanism
        * Constraint that self.value is compatible with receiver.input_state.value
            is evaluated and enforced in _instantiate_function, since that may need to be modified (see below)
        * Verification that projection has not already been assigned to receiver is handled by _add_projection_to;
            if it has, a warning is issued and the assignment request is ignored

        :param context: (str)
        :return:
        """
        # IMPLEMENTATION NOTE: since projection is added using Mechanism.add_projection(projection, state) method,
        #                      could add state specification as arg here, and pass through to add_projection()
        #                      to request a particular state
        # IMPLEMENTATION NOTE: should check that projection isn't already received by receivers

        if isinstance(self.receiver, State):
            _add_projection_to(receiver=self.receiver.owner,
                               state=self.receiver,
                               projection_spec=self,
                               context=context)

        # This should be handled by implementation of _instantiate_receiver by projection's subclass
        elif isinstance(self.receiver, Mechanism):
            raise ProjectionError("PROGRAM ERROR: receiver for {0} was specified as a Mechanism ({1});"
                                  "this should have been handled by _instantiate_receiver for {2}".
                                  format(self.name, self.receiver.name, self.__class__.__name__))

        else:
            raise ProjectionError("Unrecognized receiver specification ({0}) for {1}".format(self.receiver, self.name))

    def _update_parameter_states(self, context=None, runtime_params=None):
        for state in self._parameter_states:
            state_name = state.name
            state._update(context=context, params=runtime_params)

            # Assign version of ParameterState.value matched to type of template
            #    to runtime param or paramsCurrent (per above)
            # FYI (7/18/17 CW) : in addition to the params and attribute being set, the state's variable is ALSO being
            # set by the statement below. For example, if state_name is 'matrix', the statement below sets
            # params['matrix'] to state.value, calls setattr(state.owner, 'matrix', state.value), which sets the
            # 'matrix' parameter state's variable to ALSO be equal to state.value! If this is unintended, please change.
            value = state.parameters.value._get(context)
            getattr(self.parameters, state_name)._set(value, context)
            # manual setting of previous value to matrix value (happens in above param['matrix'] setting
            if state_name == MATRIX:
                state.function.parameters.previous_value._set(value, context)

    def add_to(self, receiver, state, context=None):
        _add_projection_to(receiver=receiver, state=state, projection_spec=self, context=context)

    def _execute(self, variable=None, context=None, runtime_params=None):
        if variable is None:
            variable = self.sender.parameters.value._get(context)

        value = super()._execute(
            variable=variable,
            context=context,
            runtime_params=runtime_params,

        )
        return value

    def _activate_for_compositions(self, composition):
        try:
            self.receiver.afferents_info[self].add_composition(composition)
        except KeyError:
            self.receiver.afferents_info[self] = ConnectionInfo(compositions=composition)

        try:
            if self not in composition.projections:
                composition._add_projection(self)
        except AttributeError:
            # composition may be ALL or None, in this case we don't need to add
            pass

    def _activate_for_all_compositions(self):
        self._activate_for_compositions(ConnectionInfo.ALL)

    # FIX: 10/3/17 - replace with @property on Projection for receiver and sender
    @property
    def socket_assignments(self):

        if self.initialization_status == ContextFlags.DEFERRED_INIT:
            sender = self.init_args[SENDER]
            receiver = self.init_args[RECEIVER]
        else:
            sender = self.sender
            receiver = self.receiver

        return {SENDER:sender,
                RECEIVER:receiver}

    def _projection_added(self, projection, context=None):
        """Stub that can be overidden by subclasses that need to know when a projection is added to the Projection"""
        pass

    def _assign_default_name(self, **kwargs):
        self._assign_default_projection_name(**kwargs)

    def _assign_default_projection_name(self, state=None, sender_name=None, receiver_name=None):
        raise ProjectionError("PROGRAM ERROR: {} must implement _assign_default_projection_name().".
                              format(self.__class__.__name__))

    @property
    def parameter_states(self):
        """Read-only access to _parameter_states"""
        return self._parameter_states

    @parameter_states.setter
    def parameter_states(self, value):
        # IMPLEMENTATION NOTE:
        # This keeps parameter_states property readonly,
        #    but averts exception when setting paramsCurrent in Component (around line 850)
        pass

    # Provide invocation wrapper
    def _gen_llvm_function_body(self, ctx, builder, params, state, arg_in, arg_out):
        mf_state = ctx.get_state_ptr(self, builder, state, self.parameters.function.name)
        mf_params = ctx.get_param_ptr(self, builder, params, self.parameters.function.name)
        main_function = ctx.get_llvm_function(self.function)
        builder.call(main_function, [mf_params, mf_state, arg_in, arg_out])

        return builder

    @property
    def _dependent_components(self):
        return list(itertools.chain(
            super()._dependent_components,
            self.parameter_states,
        ))

    def _delete_projection(projection):
        raise ProjectionError(f"{Projection.__name__} class {type(projection)} does not implement _delete method.")

    @property
    def _dict_summary(self):
        # these may occur during deferred init
        if not isinstance(self.sender, type):
            sender_name = self.sender.name
            sender_mech = self.sender.owner.name
        else:
            sender_name = None
            sender_mech = None

        if not isinstance(self.receiver, type):
            receiver_name = self.receiver.name
            receiver_mech = self.receiver.owner.name
        else:
            receiver_name = None
            receiver_mech = None

        socket_dict = {
            MODEL_SPEC_ID_SENDER_STATE: sender_name,
            MODEL_SPEC_ID_RECEIVER_STATE: receiver_name,
            MODEL_SPEC_ID_SENDER_MECH: sender_mech,
            MODEL_SPEC_ID_RECEIVER_MECH: receiver_mech
        }

        return {
            **super()._dict_summary,
            **socket_dict
        }


@tc.typecheck
def _is_projection_spec(spec, proj_type:tc.optional(type)=None, include_matrix_spec=True):
    """Evaluate whether spec is a valid Projection specification

    Return `True` if spec is any of the following:
    + Projection object, and of specified type (if proj_type is specified)
    + Projection class (or keyword string constant for one), and of specified type (if proj_type is specified)
    + 2-item tuple of which the second is a projection_spec (checked recursively with this method):
    + specification dict containing:
        + PROJECTION_TYPE:<Projection class> - must be a subclass of Projection
    + valid matrix specification (if include_matrix_spec is set to `True`)
    + state

    Otherwise, return :keyword:`False`
    """

    if isinstance(spec, Projection):
        if proj_type is None or isinstance(spec, proj_type):
                return True
        else:
            return False
    if isinstance(spec, State):
        # FIX: CHECK STATE AGAIN ALLOWABLE STATES IF type IS SPECIFIED
        return True
    # # MODIFIED 11/29/17 NEW:
    # if isinstance(spec, Mechanism):
    #     if proj_type is None:
    #     # FIX: CHECK STATE AGAIN ALLOWABLE STATES IF type IS SPECIFIED
    #         return True
    # MODIFIED 11/29/17 END
    if inspect.isclass(spec):
        if issubclass(spec, Projection):
            if proj_type is None or issubclass(spec, proj_type):
                return True
            else:
                return False
        if issubclass(spec, State):
            # FIX: CHECK STATE AGAIN ALLOWABLE STATES IF type IS SPECIFIED
            return True
    # # MODIFIED 11/29/17 NEW:
        # if issubclass(spec, Mechanism):
        #     # FIX: CHECK STATE AGAIN ALLOWABLE STATES IF type IS SPECIFIED
        #     return True
    # MODIFIED 11/29/17 END
    if isinstance(spec, dict) and any(key in spec for key in {PROJECTION_TYPE, SENDER, RECEIVER, MATRIX}):
        # FIX: CHECK STATE AGAIN ALLOWABLE STATES IF type IS SPECIFIED
        return True
    if isinstance(spec, str) and spec in PROJECTION_SPEC_KEYWORDS:
        # FIX: CHECK STATE AGAIN ALLOWABLE STATES IF type IS SPECIFIED
        return True
    if include_matrix_spec:
        if isinstance(spec, str) and spec in MATRIX_KEYWORD_SET:
            return True
        if get_matrix(spec) is not None:
            return True
    if isinstance(spec, tuple) and len(spec) == 2:
        # Call recursively on first item, which should be a standard projection spec
        if _is_projection_spec(spec[0], proj_type=proj_type, include_matrix_spec=include_matrix_spec):
            if spec[1] is not None:
                # IMPLEMENTATION NOTE: keywords must be used to refer to subclass, to avoid import loop
                if _is_projection_subclass(spec[1], MAPPING_PROJECTION):
                    return True
                if _is_modulatory_spec(spec[1]):
                    return True
        # if _is_projection_spec(spec[1], proj_type=proj_type, include_matrix_spec=include_matrix_spec):
        #         # IMPLEMENTATION NOTE: keywords must be used to refer to subclass, to avoid import loop
        #     if is_numeric(spec[0]):
        #         # if _is_projection_subclass(spec[1], MAPPING_PROJECTION):
        #         #     return True
        #         if _is_modulatory_spec(spec[1]):
        #             return True

    return False


def _is_projection_subclass(spec, keyword):
    """Evaluate whether spec is a valid specification of type

    keyword must specify a class registered in ProjectionRegistry

    Return true if spec ==
    + keyword
    + subclass of Projection associated with keyword (from ProjectionRegistry)
    + instance of the subclass
    + specification dict for instance of the subclass:
        keyword is a keyword for an entry in the spec dict
        keyword[spec] is a legal specification for the subclass

    Otherwise, return :keyword:`False`
    """
    if spec is keyword:
        return True
    # Get projection subclass specified by keyword
    try:
        proj_type = ProjectionRegistry[keyword].subclass
    except KeyError:
        pass
    else:
        # Check if spec is either the name of the subclass or an instance of it
        if inspect.isclass(spec) and issubclass(spec, proj_type):
            return True
        if isinstance(spec, proj_type):
            return True
    # spec is a specification dict for an instance of the projection subclass
    if isinstance(spec, dict) and keyword in spec:
        # Recursive call to determine that the entry of specification dict is a legal spec for the projection subclass
        if _is_projection_subclass(spec[keyword], keyword):
            return True
    return False


def _parse_projection_spec(projection_spec,
                           owner = None,       # Used only for error message
                           state_type = None,  # Used only for default assignment
                           # socket=None,
                           **kwargs):
    """Return either Projection object or Projection specification dict for projection_spec

    All keys in kwargs must be from PROJECTION_ARGS

    If projection_spec is or resolves to a Projection object, returns Projection object.
    Otherwise, return Projection specification dictionary using any arguments provided as defaults
    """

    bad_arg = next((key for key in kwargs if not key in PROJECTION_ARGS), None)
    if bad_arg:
        raise ProjectionError("Illegal argument in call to _parse_state_spec: {}".format(bad_arg))

    from collections import defaultdict
    proj_spec_dict = defaultdict(lambda :None)
    proj_spec_dict.update(kwargs)

    # Projection object
    if isinstance(projection_spec, Projection):
        projection = projection_spec
        # FIX: NOT SURE WHICH TO GIVE PRECEDENCE: SPEC IN ProjectionTuple OR INSTANTIATED Projection:
        if ((proj_spec_dict[WEIGHT] is not None and projection.weight is not None) or
            (proj_spec_dict[EXPONENT] is not None and projection.exponent is not None)):
            raise ProjectionError("PROGRAM ERROR: Conflict in weight and/or exponent specs "
                                  "between Projection and ProjectionTuple")
        projection._weight = proj_spec_dict[WEIGHT] or projection.weight
        projection._exponent = proj_spec_dict[EXPONENT] or projection.exponent
        if projection.initialization_status == ContextFlags.DEFERRED_INIT:
            projection.init_args[NAME] = proj_spec_dict[NAME] or projection.init_args[NAME]
        else:
            projection.name = proj_spec_dict[NAME] or projection.name

        return projection

    # Projection class
    elif inspect.isclass(projection_spec) and issubclass(projection_spec, Projection):
        proj_spec_dict[PROJECTION_TYPE] = projection_spec

    # Matrix
    elif is_matrix(projection_spec):
        is_matrix(projection_spec)
        proj_spec_dict[MATRIX] = projection_spec

    # Projection keyword
    elif isinstance(projection_spec, str):
        proj_spec_dict[PROJECTION_TYPE] = _parse_projection_keyword(projection_spec)

    # State object or class
    elif (isinstance(projection_spec, State)
          or (isinstance(projection_spec, type) and issubclass(projection_spec, State))):
        proj_spec_dict[PROJECTION_TYPE] = projection_spec.paramClassDefaults[PROJECTION_TYPE]
        state_type = projection_spec.__class__

    # Mechanism object or class
    elif (isinstance(projection_spec, Mechanism)
          or (isinstance(projection_spec, type) and issubclass(projection_spec, Mechanism))):
        proj_spec_dict[PROJECTION_TYPE] = projection_spec.outputStateTypes.paramClassDefaults[PROJECTION_TYPE]

    # Dict
    elif isinstance(projection_spec, dict):

        proj_spec_dict = projection_spec

        # Get projection params from specification dict
        if PROJECTION_PARAMS in proj_spec_dict:
            proj_spec_dict[PARAMS].update = proj_spec_dict[PROJECTION_PARAMS]
            # projection_spec[PARAMS].update(projection_params)
            assert False, "PROJECTION_PARAMS ({}) passed in spec dict in ProjectionTuple for {}.".\
                           format(proj_spec_dict[PROJECTION_PARAMS], projection_spec, proj_spec_dict[NAME])

    # None
    if not proj_spec_dict[PROJECTION_TYPE]:
        # Assign default type
        proj_spec_dict[PROJECTION_TYPE] = state_type.paramClassDefaults[PROJECTION_TYPE]

        # prefs is not always created when this is called, so check
        try:
            owner.prefs
            has_prefs = True
        except AttributeError:
            has_prefs = False

        if has_prefs and owner.prefs.verbosePref:
            warnings.warn("Unrecognized specification ({}) for a Projection for {} of {}; "
                          "default {} has been assigned".
                          format(projection_spec,
                                 state_type.__class__.__name__,
                                 owner.name,
                                 proj_spec_dict[PROJECTION_TYPE]))
    return proj_spec_dict


def _parse_projection_keyword(projection_spec:str):
    """Takes keyword (str) and returns corresponding Projection class
    """
    # get class for keyword in registry
    try:
        projection_type = ProjectionRegistry[PROJECTION_SPEC_KEYWORDS[projection_spec]].subclass
    except KeyError:
        # projection_spec was not a recognized key
        raise ProjectionError("{} is not a recognized {} keyword".format(projection_spec, Projection.__name__))
    # projection_spec was legitimate keyword
    else:
        return projection_type


def _parse_connection_specs(connectee_state_type,
                            owner,
                            connections):
    """Parse specification(s) for States to/from which the connectee_state_type should be connected

    TERMINOLOGY NOTE:
        "CONNECTION" is used instead of "PROJECTION" because:
            - the method abstracts over type and direction of Projection, so it is ambiguous whether
                the projection involved is to or from connectee_state_type; however, can always say it "connects with"
            - specification is not always (in fact, usually is not) in the form of a Projection; usually it is a
                Mechanism or State to/from which the connectee_state_type should send/receive the Projection

    Connection attributes declared for each type (subclass) of State that are used here:
        connectsWith : State
           - specifies the type (subclass) of State with which the connectee_state_type should be connected
        connectsWithAttribute : str
           - specifies the name of the attribute of the Mechanism that holds the states of the connectsWith's type
        projectionSocket : [SENDER or RECEIVER]
           - specifies for this method whether to use a Projection's sender or receiver for the connection
        modulators : ModulatorySignal
           -  class of ModulatorySignal that can send ModulatoryProjection to the connectee_state_type

    This method deals with connection specifications that are made in one of the following places/ways:
        - *PROJECTIONS* entry of a State specification dict;
        - last item of a State specification tuple.

    In both cases, the connection specification can be a single (stand-alone) item or a list of them.

    Projection(s) in connection(s) can be specified in any of the ways a Projection can be specified;
        * Mechanism specifications are resolved to a primary InputState or OutputState, as appropriate
        * State specifications are assumed to be for connect_with State,
            and checked for compatibilty of assignment (using projection_socket)
        * keyword specifications are resolved to corresponding Projection class
        * Class assignments are checked for compatiblity with connectee_state_type and connect_with State

    Each connection specification can, itself, be one of the following:
        * State object or class;
        * Mechanism object or class - primary State is used, if applicable, otherwise an exception is generated;
        * dict - must have the first and can have any of the additional entries below:
            *STATE*:<state_spec> - required; must resolve to an instantiated state;  can use any of the following:
                                       State - the State is used;
                                       Mechanism - primary State will be used if appropriate,
                                                   otherwise generates an exception;
                                       {Mechanism:state_spec or [state_spec<, state_spec...>]} -
                                                   each state_spec must be for an instantiated State of the Mechanism,
                                                   referenced by its name or in a CONNECTION specification that uses
                                                   its name (or, for completeness, the State itself);
                                                   _parse_connections() is called recursively for each state_spec
                                                   (first replacing the name with the actual state);
                                                   and returns a list of ProjectionTuples; any weights, exponents,
                                                   or projections assigned in those tuples are left;  otherwise, any
                                                   values in the entries of the outer dict (below) are assigned;
                                                   note:  the dictionary can have multiple Mechanism entries
                                                          (which permits the same defaults to be assigned to all the
                                                          States for all of the Mechanisms)
                                                          or they can be assigned each to their own dictionary
                                                          (which permits different defaults to be assigned to the
                                                          States for each Mechanism);
            *WEIGHT*:<int> - optional; specifies weight given to projection by receiving InputState
            *EXPONENT:<int> - optional; specifies weight given to projection by receiving InputState
            *PROJECTION*:<projection_spec> - optional; specifies projection (instantiated or matrix) for connection
                                             default is PROJECTION_TYPE specified for STATE
        * tuple or list of tuples: (specification requirements same as for dict above);  each must be:
            (state_spec, projection_spec) or
            (state_spec, weight, exponent, projection_spec)

    Returns list of ProjectionTuples, each of which specifies:
        - the state to be connected with
        - weight and exponent for that connection (assigned to the projection)
        - projection specification

    """

    from psyneulink.core.components.states.state import _get_state_for_socket
    from psyneulink.core.components.states.state import StateRegistry
    from psyneulink.core.components.states.inputstate import InputState
    from psyneulink.core.components.states.outputstate import OutputState
    from psyneulink.core.components.states.parameterstate import ParameterState
    from psyneulink.core.components.mechanisms.modulatory.modulatorymechanism import ModulatoryMechanism_Base
    from psyneulink.core.components.mechanisms.modulatory.control.controlmechanism import _is_control_spec
    from psyneulink.core.components.mechanisms.modulatory.control.gating.gatingmechanism import _is_gating_spec

    if not inspect.isclass(connectee_state_type):
        raise ProjectionError("Called for {} with \'connectee_state_type\' arg ({}) that is not a class".
                         format(owner.name, connectee_state_type))

    # Get connection attributes for connectee
    connects_with = [StateRegistry[name].subclass for name in connectee_state_type.connectsWith]
    connect_with_attr = connectee_state_type.connectsWithAttribute
    projection_socket = connectee_state_type.projectionSocket
    modulators = [StateRegistry[name].subclass for name in connectee_state_type.modulators]

    DEFAULT_WEIGHT = None
    DEFAULT_EXPONENT = None
    DEFAULT_PROJECTION = None

    # Convert to list for subsequent processing
    if isinstance(connections, set):
        # if owner.verbosePref:
        #     warnings.warn("Connection specification for {} of {} was a set ({});"
        #                   "it was converted to a list, but the order of {} assignments is not "
        #                   "predictable".format(connectee_state_type, owner.name,
        #                                        connections, Projection.__name__))
        # connections = list(connections)
        raise ProjectionError("Connection specification for {} of {} is a set ({}); it should be a list.".
                              format(connectee_state_type.__name__, owner.name, connections, Projection.__name__))

    elif not isinstance(connections, list):
        connections = [connections]
    connect_with_states = []

    for connection in connections:

        # If a Mechanism, State, or State type is used to specify the connection on its own (i.e., w/o dict or tuple)
        #     put in ProjectionTuple as both State spec and Projection spec (to get Projection for that State)
        #     along with defaults for weight and exponent, and call _parse_connection_specs recursively
        #     to validate the state spec and append ProjectionTuple to connect_with_states
        if isinstance(connection, (Mechanism, State, type)):
            # FIX: 10/3/17 - REPLACE THIS (AND ELSEWHERE) WITH ProjectionTuple THAT HAS BOTH SENDER AND RECEIVER
            # FIX: 11/28/17 - HACKS TO HANDLE PROJECTION FROM GatingSignal TO InputState or OutputState
            # FIX:            AND PROJECTION FROM ControlSignal to ParameterState
            # # If it is a ModulatoryMechanism specification, get its ModulatorySignal class
            # # (so it is recognized by _is_projection_spec below (Mechanisms are not for secondary reasons)
            # if isinstance(connection, type) and issubclass(connection, ModulatoryMechanism_Base):
            #     connection = connection.outputStateTypes
            if ((isinstance(connectee_state_type, (InputState, OutputState, ParameterState))
                 or isinstance(connectee_state_type, type)
                and issubclass(connectee_state_type, (InputState, OutputState, ParameterState)))
                and _is_modulatory_spec(connection)):
                # Convert ModulatoryMechanism spec to corresponding ModulatorySignal spec
                if isinstance(connection, type) and issubclass(connection, ModulatoryMechanism_Base):
                    # If the connection supports multiple outputStateTypes,
                    #    get the one compatible with the current connectee:
                    output_state_types = connection.outputStateTypes
                    if not isinstance(output_state_types, list):
                        output_state_types = [output_state_types]
                    output_state_type = [o for o in output_state_types if o.__name__ in
                                          connectee_state_type.connectsWith]
                    assert len(output_state_type)==1, \
                        f"PROGRAM ERROR:  More than one {OutputState.__name__} type found for {connection}  " \
                            f"({output_state_types}) that can be assigned a modulatory {Projection.__name__} " \
                            f"to {connectee_state_type.__name__} of {owner.name}"
                    connection = output_state_type[0]
                elif isinstance(connection, ModulatoryMechanism_Base):
                    connection = connection.output_state

                projection_spec = connection

            else:
                projection_spec = connectee_state_type

            projection_tuple = (connection, DEFAULT_WEIGHT, DEFAULT_EXPONENT, projection_spec)
            connect_with_states.extend(_parse_connection_specs(connectee_state_type, owner, projection_tuple))

        # If a Projection specification is used to specify the connection:
        #  assign the Projection specification to the projection_specification item of the tuple,
        #  but also leave it is as the connection specification (it will get resolved to a State reference when the
        #    tuple is created in the recursive call to _parse_connection_specs below).
        elif _is_projection_spec(connection, include_matrix_spec=False):
            projection_spec = connection
            projection_tuple = (connection, DEFAULT_WEIGHT, DEFAULT_EXPONENT, projection_spec)
            connect_with_states.extend(_parse_connection_specs(connectee_state_type, owner, projection_tuple))

        # Dict of one or more Mechanism specifications, used to specify individual States of (each) Mechanism;
        #   convert all entries to tuples and call _parse_connection_specs recursively to generate ProjectionTuples;
        #   main purpose of this is to resolve any str references to name of state (using context of owner Mechanism)
        elif isinstance(connection, dict):

            # Check that dict has at least one entry with a Mechanism as the key
            if (not any(isinstance(spec, Mechanism) for spec in connection) and
                    not any(spec == STATES for spec in connection)):
                raise ProjectionError("There are no {}s or {}s in the list ({}) specifying {}s for an {} of {}".
                                 format(Mechanism.__name__, State.__name__, connection, Projection.__name__,
                                        connectee_state_type.__name__, owner.name))

            # Add default WEIGHT, EXPONENT, and/or PROJECTION specification for any that are not aleady in the dict
            #    (used as the default values for all the States of all Mechanisms specified for this dict;
            #    can use different dicts to implement different sets of defaults for the States of diff Mechanisms)
            if not WEIGHT in connection:
                connection[WEIGHT] = DEFAULT_WEIGHT
            if not EXPONENT in connection:
                connection[EXPONENT] = DEFAULT_EXPONENT
            if not PROJECTION in connection:
                connection[PROJECTION] = DEFAULT_PROJECTION

            # Now process each entry that has *STATES* or a Mechanism as its key
            for key, state_connect_specs in connection.items():

                # Convert state_connect_specs to a list for subsequent processing
                if not isinstance(state_connect_specs, list):
                    state_connect_specs = [state_connect_specs]

                for state_connect_spec in state_connect_specs:

                    # State, str (name) or Projection specification
                    if isinstance(state_connect_spec, (State, str, _is_projection_spec)):

                        # If state_connection_spec is a string (name), it has to be in a Mechanism entry
                        if isinstance(state_connect_spec, str) and isinstance(key, Mechanism):
                            mech = key
                        else:
                            raise ProjectionError("{} specified by name ({}) is not in a {} entry".
                                             format(State.__name__, state_connect_spec, Mechanism.__name__))

                        # Call _get_state_for_socket to parse if it is a str,
                        #    and in either case to make sure it belongs to mech
                        state = _get_state_for_socket(owner=owner,
                                                      state_spec=state_connect_spec,
                                                      state_types=connect_with_attr,
                                                      mech=mech,
                                                      projection_socket=projection_socket)
                        if isinstance(state, list):
                            assert False, 'Got list of allowable states for {} as specification for {} of {}'.\
                                          format(state_connect_spec, projection_socket, mech.name)

                        # Assign state along with dict's default values to tuple
                        state_connect_spec = (state,
                                              connection[WEIGHT],
                                              connection[EXPONENT],
                                              connection[PROJECTION])

                    # Dict specification for state itself
                    elif isinstance(state_connect_spec, dict):
                        # Get STATE entry
                        state_spec = state_connect_spec[STATE]
                        # Parse it to get reference to actual State make sure it belongs to mech:
                        state = _get_state_for_socket(owner=owner,
                                                    state_spec=state_spec,
                                                    state_types=connect_with_attr,
                                                    mech=mech,
                                                    projection_socket=projection_socket)
                        if isinstance(state, list):
                            assert False, 'Got list of allowable states for {} as specification for {} of {}'.\
                                           format(state_connect_spec, projection_socket, mech.name)
                        # Re-assign to STATE entry of dict (to preserve any other connection specifications in dict)
                        state_connect_spec[STATE] = state

                    # Tuple specification for State itself
                    elif isinstance(state_connect_spec, tuple):
                        # Get STATE entry
                        state_spec = state_connect_spec[0]
                        # Parse it to get reference to actual State make sure it belongs to mech:
                        state = _get_state_for_socket(owner=owner,
                                                    state_spec=state_spec,
                                                    state_types=connect_with_attr,
                                                    mech=mech,
                                                    projection_socket=projection_socket)
                        if isinstance(state, list):
                            assert False, 'Got list of allowable states for {} as specification for {} of {}'.\
                                           format(state_connect_spec, projection_socket, mech.name)
                        # Replace parsed value in original tuple, but...
                        #    tuples are immutable, so have to create new one, with state_spec as (new) first item
                        # Get items from original tuple
                        state_connect_spec_tuple_items = [item for item in state_connect_spec]
                        # Replace state_spec
                        state_connect_spec_tuple_items[0] = state
                        # Reassign to new tuple
                        state_connect_spec = tuple(state_connect_spec_tuple_items)

                    # Recusively call _parse_connection_specs to get ProjectionTuple and append to connect_with_states
                    connect_with_states.extend(_parse_connection_specs(connectee_state_type, owner, state_connect_spec))

        # Process tuple, including final validation of State specification
        # Tuple could be:
        #     (state_spec, projection_spec) or
        #     (state_spec, weight, exponent, projection_spec)
        # Note:  this is NOT the same as the State specification tuple (which can have a similar format);
        #        the weights and exponents here specify *individual* Projections to a particular state,
        #            (vs. weights and exponents for an entire state, such as for InputState);
        #        State specification tuple is handled in the _parse_state_specific_specs() method of State subclasses

        elif isinstance(connection, tuple):

            # 2-item tuple: can be (<value>, <projection_spec>) or (<state name or list of state names>, <Mechanism>)
            mech=None

            if len(connection) == 2:
                first_item, last_item = connection
                weight = DEFAULT_WEIGHT
                exponent = DEFAULT_EXPONENT
            elif len(connection) == 4:
                first_item, weight, exponent, last_item = connection
            else:
                raise ProjectionError("{} specification tuple for {} ({}) must have either two or four items".
                                      format(connectee_state_type.__name__, owner.name, connection))

            # Default assignments, possibly overridden below
            state_spec = first_item
            projection_spec = last_item

            # (<value>, <projection_spec>)
            if is_numeric(first_item):
                projection_spec = first_item

            # elif is_matrix(first_item):
            #     projection_spec = last_item
            #     state_spec = None

            elif _is_projection_spec(last_item):

                # If specification is a list of States and/or Mechanisms, get Projection spec for each
                if isinstance(first_item, list):
                     # Call _parse_connection_spec for each State or Mechanism, to generate a conection spec for each
                    for connect_with_spec in first_item:
                        if not isinstance(connect_with_spec, (State, Mechanism)):
                              raise StateError(f"Item in the list used to specify a {last_item.__name__} "
                                               f"for {owner.name} ({connect_with_spec.__name__}) "
                                               f"is not a {State.__name__} or {Mechanism.__name__}")
                        c = _parse_connection_specs(connectee_state_type=connectee_state_type,
                                                    owner=owner,
                                                    connections=ProjectionTuple(connect_with_spec,
                                                                                weight, exponent,
                                                                                last_item))
                        connect_with_states.extend(c)
                    # Move on to other connections
                    continue
                # Otherwise, go on to process this Projection specification
                state_spec = first_item
                projection_spec = last_item


            # (<state name or list of state names>, <Mechanism>)
            elif isinstance(first_item, (str, list)):
                state_item = first_item
                mech_item = last_item

                if not isinstance(mech_item, Mechanism):
                    raise ProjectionError("Expected 2nd item of the {} specification tuple for {} ({}) to be a "
                                          "Mechanism".format(connectee_state_type.__name__, owner.name, mech_item))
                # First item of tuple is a list of State names, so recursively process it
                if isinstance(state_item, list):
                     # Call _parse_connection_spec for each State name, to generate a conection spec for each
                    for state_name in state_item:
                        if not isinstance(state_name, str):
                             raise ProjectionError("Expected 1st item of the {} specification tuple for {} ({}) to be "
                                                   "the name of a {} of its 2nd item ({})".
                                                      format(connectee_state_type.__name__, owner.name, state_name,
                                                              connects_with, mech_item.name))
                        c = _parse_connection_specs(connectee_state_type=connectee_state_type,
                                                    owner=owner,
                                                    connections=ProjectionTuple(state_name,
                                                                                weight, exponent,
                                                                                mech_item))
                        connect_with_states.extend(c)
                    # Move on to other connections
                    continue
                # Otherwise, go on to process (<State name>, Mechanism) spec
                state_spec = state_item
                projection_spec = None
                mech=mech_item

            # Validate state specification, and get actual state referenced if it has been instantiated
            try:
                # FIX: 11/28/17 HACK TO DEAL WITH GatingSignal Projection to OutputState
                # FIX: 5/11/19: CORRECTED TO HANDLE ControlMechanism SPECIFIED FOR GATING
                if ((_is_gating_spec(first_item) or _is_control_spec(first_item))
                    and (isinstance(last_item, OutputState) or last_item == OutputState)
                ):
                    projection_socket = SENDER
                    state_types = [OutputState]
                    mech_state_attribute = [OUTPUT_STATES]
                else:
                    state_types = connects_with
                    mech_state_attribute=connect_with_attr

                state = _get_state_for_socket(owner=owner,
                                              connectee_state_type=connectee_state_type,
                                              state_spec=state_spec,
                                              state_types=state_types,
                                              mech=mech,
                                              mech_state_attribute=mech_state_attribute,
                                              projection_socket=projection_socket)
            except StateError as e:
                raise ProjectionError(f"Problem with specification for {State.__name__} in {Projection.__name__} "
                                      f"specification{(' for ' + owner.name) if owner else ' '}: " + e.error_value)

            # Check compatibility with any State(s) returned by _get_state_for_socket

            if isinstance(state, list):
                states = state
            else:
                states = [state]

            for item in states:
                if inspect.isclass(item):
                    state_type = item
                else:
                    state_type = item.__class__

                # # Test that state_type is in the list for state's connects_with
                from psyneulink.core.components.states.modulatorysignals.controlsignal import ControlSignal

                # KAM 7/26/18 modified to allow ControlMechanisms to be terminal nodes of compositions
                # We could only include ControlSignal in the allowed types if the receiver is a CIM?
                allowed = connects_with + modulators + [ControlSignal]

                if not any(issubclass(connects_with_state, state_type)
                           for connects_with_state in allowed):
                    spec = projection_spec or state_type.__name__
                    raise ProjectionError(f"Projection specification (\'{spec}\') for an incompatible connection: "
                                          f"{state_type.__name__} with {connectee_state_type.__name__} of {owner.name};"
                                          f" spec should be one of the following: "
                                          f"{' or '.join([r for r in state_type.canReceive])}, "
                                          f" or connectee should be one of the following: "
                                          f"{' or '.join([c.__name__ for c in connects_with])},")

            # Parse projection specification into Projection specification dictionary
            # Validate projection specification
            if _is_projection_spec(projection_spec) or _is_modulatory_spec(projection_spec) or projection_spec is None:

                # FIX: 11/21/17 THIS IS A HACK TO DEAL WITH GatingSignal Projection TO InputState or OutputState
                from psyneulink.core.components.states.inputstate import InputState
                from psyneulink.core.components.states.outputstate import OutputState
                from psyneulink.core.components.states.modulatorysignals.gatingsignal import GatingSignal
                from psyneulink.core.components.projections.modulatory.gatingprojection import GatingProjection
                from psyneulink.core.components.projections.modulatory.controlprojection import ControlProjection
                if (not isinstance(projection_spec, GatingProjection)
                    and isinstance(state, GatingSignal)
                    and connectee_state_type in {InputState, OutputState}):
                    projection_spec = state
                if (
                        (not isinstance(projection_spec, GatingProjection)
                         and state.__class__ == GatingSignal
                         and connectee_state_type in {InputState, OutputState})
                # # MODIFIED 9/27/19 NEW: [JDC]
                #     or
                #         (not isinstance(projection_spec, ControlProjection)
                #          and state.__class__ == ControlSignal
                #          and connectee_state_type in {InputState, OutputState})
                ):
                    projection_spec = state

                elif (_is_gating_spec(first_item) or _is_control_spec((first_item))
                      and not isinstance(last_item, (GatingProjection, ControlProjection))):
                    projection_spec = first_item
                projection_spec = _parse_projection_spec(projection_spec,
                                                         owner=owner,
                                                         state_type=connectee_state_type)

                _validate_connection_request(owner,
                                             connects_with + modulators,
                                             projection_spec,
                                             projection_socket,
                                             connectee_state_type)
            else:
                raise ProjectionError("Invalid {} specification ({}) for connection "
                                      "between {} \'{}\' and {} of \'{}\'.".
                                 format(Projection.__name__,
                                        projection_spec,
                                        state_type.__name__,
                                        state.name,
                                        connectee_state_type.__name__,
                                        owner.name))

            connect_with_states.extend([ProjectionTuple(state, weight, exponent, projection_spec)])

        else:
            raise ProjectionError("Unrecognized, invalid or insufficient specification of connection for {}: \'{}\'".
                                  format(owner.name, connection))

    if not all(isinstance(projection_tuple, ProjectionTuple) for projection_tuple in connect_with_states):
        raise ProjectionError("PROGRAM ERROR: Not all items are ProjectionTuples for {}".format(owner.name))

    return connect_with_states

@tc.typecheck
def _validate_connection_request(
        owner,                                   # Owner of State seeking connection
        connect_with_states:list,                # State to which connection is being sought
        projection_spec:_is_projection_spec,     # projection specification
        projection_socket:str,                   # socket of Projection to be connected to target state
        connectee_state:tc.optional(type)=None): # State for which connection is being sought
    """Validate that a Projection specification is compatible with the State to which a connection is specified

    Carries out undirected validation (i.e., without knowing whether the connectee is the sender or receiver).
    Use _validate_receiver or ([TBI] validate_sender) for directed validation.
    Note: connectee_state is used only for name in errors

    If projection_spec is a Projection:
        - if it is instantiated, compare the projection_socket specified (sender or receiver) with connect_with_state
        - if it in deferred_init, check to see if the specified projection_socket has been specified in init_args;
            otherwise, use Projection's type
    If projection_spec is a class specification, use Projection's type
    If projection_spec is a dict:
        - check if there is an entry for the socket and if so, use that
        - otherwise, check to see if there is an entry for the Projection's type

    Returns:
        `True` if validation has been achieved to same level (though possibly with warnings);
        `False` if validation could not be done;
        raises an exception if an incompatibility is detected.
    """


    if connectee_state:
        connectee_str = " {} of".format(connectee_state.__name__)
    else:
        connectee_str = ""

    # Convert connect_with_states (a set of classes) into a tuple for use as second arg in isinstance()
    connect_with_states = tuple(connect_with_states)
    # Make sure none of its entries are None (which will fail in isinstance()):
    if None in connect_with_states:
        raise ProjectionError("PROGRAM ERROR: connect_with_states ({}) should not have any entries that are \'None\'; "
                              "Check assignments to \'connectsWith' and \'modulators\' for each State class".
                              format(connect_with_states))

    connect_with_state_names = ", ".join([c.__name__ for c in connect_with_states if c is not None])

    # Used below
    def _validate_projection_type(projection_class):
        # Validate that Projection's type can connect with a class in connect_with_states
        if any(state.__name__ in getattr(projection_class.sockets, projection_socket) for state in connect_with_states):
            return True
        else:
            return False

    # If it is an actual Projection
    if isinstance(projection_spec, Projection):

        # It is in deferred_init status
        if projection_spec.initialization_status == ContextFlags.DEFERRED_INIT:

            # Try to get the State to which the Projection will be connected when fully initialized
            #     as confirmation that it is the correct type for state_type
            try:
                projection_socket_state = projection_spec.socket_assignments[projection_socket]
            # State for projection's socket couldn't be determined
            except KeyError:
                # Use Projection's type for validation
                # At least validate that Projection's type can connect with a class in connect_with_states
                return _validate_projection_type(projection_spec.__class__)
                    # Projection's socket has been assigned to a State
            else:
                # if both SENDER and RECEIVER are specified:
                if projection_spec.init_args[SENDER] and projection_spec.init_args[RECEIVER]:
                    # Validate that the State is a class in connect_with_states
                    if (isinstance(projection_socket_state, connect_with_states) or
                            (inspect.isclass(projection_socket_state)
                             and issubclass(projection_socket_state, connect_with_states))):
                        return True
                # Otherwise, revert again to validating Projection's type
                else:
                    return _validate_projection_type(projection_spec.__class__)

        # Projection has been instantiated
        else:
            # Determine whether the State to which the Projection's socket has been assigned is in connect_with_states
            # FIX: 11/4/17 - THIS IS A HACK TO DEAL WITH THE CASE IN WHICH THE connectee_state IS AN OutputState
            # FIX:               THE projection_socket FOR WHICH IS USUALLY A RECEIVER;
            # FIX:           HOWEVER, IF THE projection_spec IS A GatingSignal
            # FIX:               THEN THE projection_socket MUST BE SENDER
            from psyneulink.core.components.states.outputstate import OutputState
            from psyneulink.core.components.projections.modulatory.gatingprojection import GatingProjection
            from psyneulink.core.components.projections.modulatory.controlprojection import ControlProjection
            if connectee_state is OutputState and isinstance(projection_spec, (GatingProjection, ControlProjection)):
                projection_socket = SENDER
            projection_socket_state = getattr(projection_spec, projection_socket)
            if  issubclass(projection_socket_state.__class__, connect_with_states):
                return True

        # None of the above worked, so must be incompatible
        raise ProjectionError("{} specified to be connected with{} {} "
                              "is not consistent with the {} of the specified {} ({})".
                              format(State.__name__, connectee_str, owner.name,
                                     projection_socket, Projection.__name__, projection_spec))

    # Projection class
    elif inspect.isclass(projection_spec) and issubclass(projection_spec, State):
        if issubclass(projection_spec, connect_with_states):
            return True
        raise ProjectionError("{} type specified to be connected with{} {} ({}) "
                              "is not compatible with the {} of the specified {} ({})".
                              format(State.__name__, connectee_str, owner.name,  projection_spec.__name__,
                                     projection_socket, Projection.__name__, connect_with_state_names))

    # State
    elif isinstance(projection_spec, State):
        if isinstance(projection_spec, connect_with_states):
            return True
        raise ProjectionError("{} specified to be connected with{} {} ({}) "
                              "is not compatible with the {} of the specified {} ({})".
                              format(State.__name__, connectee_str, owner.name,  projection_spec,
                                     projection_socket, Projection.__name__, connect_with_state_names))

    # State class
    elif inspect.isclass(projection_spec) and issubclass(projection_spec, Projection):
        _validate_projection_type(projection_spec)
        return True

    # Projection specification dictionary
    elif isinstance(projection_spec, dict):
        # Try to validate using entry for projection_socket
        if projection_socket in projection_spec and projection_spec[projection_socket] is not None:
            # Specification for the [projection_socket] entry (i.e., SENDER or RECEIVER)
            #    should be either of the correct class or a Mechanism
            #    (which assumes it will get properly resolved in context when the Projection is instantiated)
            if (projection_spec[projection_socket] in connect_with_states or
                    isinstance(projection_spec[projection_socket], Mechanism)):
                return True
            else:
                raise ProjectionError("{} ({}) specified to be connected with{} {} is not compatible "
                                      "with the {} ({}) in the specification dict for the {}.".
                                      format(State.__name__,
                                             connect_with_state_names,
                                             connectee_str,
                                             owner.name,
                                             projection_socket,
                                             projection_spec[projection_socket],
                                             Projection.__name__))
        # Try to validate using entry for Projection' type
        elif PROJECTION_TYPE in projection_spec and projection_spec[PROJECTION_TYPE] is not None:
            _validate_projection_type(projection_spec[PROJECTION_TYPE])
            return True

    # Projection spec is too abstract to validate here
    #    (e.g., value or a name that will be used in context to instantiate it)
    return False

def _get_projection_value_shape(sender, matrix):
    """Return shape of a Projection's value given its sender and matrix"""
    from psyneulink.core.components.functions.transferfunctions import get_matrix
    matrix = get_matrix(matrix)
    return np.zeros(matrix.shape[np.atleast_1d(sender.value).ndim :])

# IMPLEMENTATION NOTE: MOVE THIS TO ModulatorySignals WHEN THAT IS IMPLEMENTED
@tc.typecheck
def _validate_receiver(sender_mech:Mechanism,
                       projection:Projection,
                       expected_owner_type:type,
                       spec_type=None,
                       context=None):
    """Check that Projection is to expected_receiver_type and in the same System as the sender_mech (if specified)

    expected_owner_type must be a Mechanism or a Projection
    spec_type should be LEARNING_SIGNAL, CONTROL_SIGNAL or GATING_SIGNAL

    Note:  this is a "directed" validation;
           for undirected validation of a Projection, use _validate_projection_specification

    """
    spec_type = " in the {} arg ".format(spec_type) or ""

    if projection.initialization_status == ContextFlags.DEFERRED_INIT:
        # receiver = projection.init_args['receiver'].owner
        state = projection.init_args['receiver']
        receiver = state.owner
    else:
        # receiver = projection.receiver.owner
        state = projection.receiver
        receiver = state.owner

    if isinstance(receiver, Mechanism):
        receiver_mech = receiver
    elif isinstance(receiver, Projection):
        receiver_mech = receiver.receiver.owner
    else:
        raise ProjectionError("receiver of projection ({}) must be a {} or {}".
                              format(projection.name, MECHANISM, PROJECTION))

    if not isinstance(receiver, expected_owner_type):
        raise ProjectionError("A {} specified {}for {} ({}) projects to a component other than the {} of a {}".
                                    format(projection.__class__.__name__,
                                           spec_type,
                                           sender_mech.name,
                                           receiver,
                                           state.__class__.__name__,
                                           expected_owner_type.__name__))

    # Check if receiver_mech is in the same system as sender_mech;
    #    if either has not been assigned a system, return

    # Check whether mech is in the same system as sender_mech
    receiver_systems = set()
    # receiver_mech is a ControlMechanism (which has a system but no systems attribute)
    if hasattr(receiver_mech, 'system') and receiver_mech.system:
        receiver_systems.update({receiver_mech.system})
    # receiver_mech is a ProcessingMechanism (which has a systems but system attribute is usually None)
    elif hasattr(receiver_mech, 'systems') and receiver_mech.systems:
        receiver_systems.update(set(receiver_mech.systems))
    else:
        return

    sender_systems = set()
    # sender_mech is a ControlMechanism (which has a system but no systems attribute)
    if hasattr(sender_mech, 'system') and sender_mech.system:
        sender_systems.update({sender_mech.system})
    # sender_mech is a ProcessingMechanism (which has a systems but system attribute is usually None)
    elif hasattr(sender_mech, 'systems')and sender_mech.systems:
        sender_systems.update(set(sender_mech.systems))
    else:
        return

    #  Check that projection is to a (projection to a) mechanisms in the same system as sender_mech
    if not receiver_systems & sender_systems:
        raise ProjectionError("A {} specified {}for {} projects to a Component that is not in the same System".
                                    format(projection.__class__.__name__,
                                           spec_type,
                                           sender_mech.name))


# IMPLEMENTATION NOTE:  THIS SHOULD BE MOVED TO COMPOSITION ONCE THAT IS IMPLEMENTED
def _add_projection_to(receiver, state, projection_spec, context=None):
    """Assign an "incoming" Projection to a receiver InputState or ParameterState of a Component object

    Verify that projection has not already been assigned to receiver;
        if it has, issue a warning and ignore the assignment request.

    Requirements:
       * receiver must be an appropriate Component object (currently, a Mechanism or a Projection);
       * state must be a specification of an InputState or ParameterState;
       * specification of InputState can be any of the following:
                - INPUT_STATE - assigns projection_spec to (primary) InputState;
                - InputState object;
                - index for Mechanism.input_states;
                - name of an existing InputState (i.e., key for Mechanism.input_states);
                - the keyword ADD_INPUT_STATE or the name for an InputState to be added;
       * specification of ParameterState must be a ParameterState object
       * projection_spec can be any valid specification of a projection_spec
           (see `State._instantiate_projections_to_state`).

    Args:
        receiver (Mechanism or Projection)
        state (State subclass)
        projection_spec: (Projection, dict, or str)
        context

    """
    # IMPLEMENTATION NOTE:  ADD FULL SET OF ParameterState SPECIFICATIONS
    #                       CURRENTLY, ASSUMES projection_spec IS AN ALREADY INSTANTIATED PROJECTION

    from psyneulink.core.components.states.state import _instantiate_state
    from psyneulink.core.components.states.state import State_Base
    from psyneulink.core.components.states.inputstate import InputState

    if not isinstance(state, (int, str, State)):
        raise ProjectionError("State specification(s) for {} (as receiver(s) of {}) contain(s) one or more items"
                             " that is not a name, reference to a {} or an index for one".
                             format(receiver.name, projection_spec.name, State.__name__))

    # state is State object, so use thatParameterState
    if isinstance(state, State_Base):
        return state._instantiate_projections_to_state(projections=projection_spec, context=context)

    # Generic INPUT_STATE is specified, so use (primary) InputState
    elif state is INPUT_STATE:
        return receiver.input_state._instantiate_projections_to_state(projections=projection_spec, context=context)

    # input_state is index into input_states OrderedDict, so get corresponding key and assign to input_state
    elif isinstance(state, int):
        try:
            key = receiver.input_states[state]
        except IndexError:
            raise ProjectionError("Attempt to assign projection_spec ({0}) to InputState {1} of {2} "
                                 "but it has only {3} input_states".
                                 format(projection_spec.name, state, receiver.name, len(receiver.input_states)))
        else:
            input_state = key

    # input_state is string (possibly key retrieved above)
    #    so try as key in input_states OrderedDict (i.e., as name of an InputState)
    if isinstance(state, str):
        try:
            return receiver.input_state[state]._instantiate_projections_to_state(projections=projection_spec, context=context)
        except KeyError:
            pass
        else:
            if receiver.prefs.verbosePref:
                warnings.warn("Projection_spec {0} added to {1} of {2}".
                              format(projection_spec.name, state, receiver.name))
            # return

    # input_state is either the name for a new InputState or ADD_INPUT_STATE
    if not state is ADD_INPUT_STATE:
        if receiver.prefs.verbosePref:
            reassign = input("\nAdd new InputState named {0} to {1} (as receiver for {2})? (y/n):".
                             format(input_state, receiver.name, projection_spec.name))
            while reassign != 'y' and reassign != 'n':
                reassign = input("\nAdd {0} to {1}? (y/n):".format(input_state, receiver.name))
            if reassign == 'n':
                raise ProjectionError("Unable to assign projection {0} to receiver {1}".
                                      format(projection_spec.name, receiver.name))

    # validate that projection has not already been assigned to receiver
    if receiver.verbosePref or projection_spec.sender.owner.verbosePref:
        if projection_spec in receiver.all_afferents:
            warnings.warn("Request to assign {} as projection to {} was ignored; it was already assigned".
                          format(projection_spec.name, receiver.owner.name))

    input_state = _instantiate_state(owner=receiver,
                                    state_type=InputState,
                                    name=input_state,
                                    reference_value=projection_spec.value,
                                    reference_value_name='Projection_spec value for new InputState',
                                    context=context)

    #  Update InputState and input_states
    if receiver.input_states:
        receiver.input_states[input_state.name] = input_state

    # No InputState(s) yet, so create them
    else:
        receiver.input_states = ContentAddressableList(component_type=State_Base,
                                                       list=[input_state],
                                                       name=receiver.name+'.input_states')

    return input_state._instantiate_projections_to_state(projections=projection_spec, context=context)


# IMPLEMENTATION NOTE:  THIS SHOULD BE MOVED TO COMPOSITION ONCE THAT IS IMPLEMENTED
def _add_projection_from(sender, state, projection_spec, receiver, context=None):
    """Assign an "outgoing" Projection from an OutputState of a sender Mechanism

    projection_spec can be any valid specification of a projection_spec (see State._instantiate_projections_to_state)
    state must be a specification of an OutputState
    Specification of OutputState can be any of the following:
            - OUTPUT_STATE - assigns projection_spec to (primary) OutputState
            - OutputState object
            - index for Mechanism OutputStates OrderedDict
            - name of OutputState (i.e., key for Mechanism.OutputStates OrderedDict))
            - the keyword ADD_OUTPUT_STATE or the name for an OutputState to be added

    Args:
        sender (Mechanism):
        projection_spec: (Projection, dict, or str)
        state (OutputState, str, or value):
        context:
    """


    from psyneulink.core.components.states.state import _instantiate_state
    from psyneulink.core.components.states.state import State_Base
    from psyneulink.core.components.states.outputstate import OutputState

    # Validate that projection is not already assigned to sender; if so, warn and ignore

    if isinstance(projection_spec, Projection):
        projection = projection_spec
        if ((isinstance(sender, OutputState) and projection.sender is sender) or
                (isinstance(sender, Mechanism) and projection.sender is sender.output_state)):
            if sender.verbosePref:
                warnings.warn("Request to assign {} as sender of {}, but it has already been assigned".
                              format(sender.name, projection.name))
                return

    if not isinstance(state, (int, str, OutputState)):
        raise ProjectionError("State specification for {0} (as sender of {1}) must be the name, reference to "
                              "or index of an OutputState of {0} )".format(sender.name, projection_spec))

    # state is State object, so use that
    if isinstance(state, State_Base):
        state._instantiate_projection_from_state(projection_spec=projection_spec, receiver=receiver, context=context)
        return

    # Generic OUTPUT_STATE is specified, so use (primary) OutputState
    elif state is OUTPUT_STATE:
        sender.output_state._instantiate_projections_to_state(projections=projection_spec, context=context)
        return

    # input_state is index into OutputStates OrderedDict, so get corresponding key and assign to output_state
    elif isinstance(state, int):
        try:
            key = list(sender.output_states.keys)[state]
        except IndexError:
            raise ProjectionError("Attempt to assign projection_spec ({0}) to OutputState {1} of {2} "
                                 "but it has only {3} OutputStates".
                                 format(projection_spec.name, state, sender.name, len(sender.output_states)))
        else:
            output_state = key

    # output_state is string (possibly key retrieved above)
    #    so try as key in output_states ContentAddressableList (i.e., as name of an OutputState)
    if isinstance(state, str):
        try:
            sender.output_state[state]._instantiate_projections_to_state(projections=projection_spec, context=context)
        except KeyError:
            pass
        else:
            if sender.prefs.verbosePref:
                warnings.warn("Projection_spec {0} added to {1} of {2}".
                              format(projection_spec.name, state, sender.name))
            # return

    # output_state is either the name for a new OutputState or ADD_OUTPUT_STATE
    if not state is ADD_OUTPUT_STATE:
        if sender.prefs.verbosePref:
            reassign = input("\nAdd new OutputState named {0} to {1} (as sender for {2})? (y/n):".
                             format(output_state, sender.name, projection_spec.name))
            while reassign != 'y' and reassign != 'n':
                reassign = input("\nAdd {0} to {1}? (y/n):".format(output_state, sender.name))
            if reassign == 'n':
                raise ProjectionError("Unable to assign projection {0} to sender {1}".
                                      format(projection_spec.name, sender.name))

    output_state = _instantiate_state(owner=sender,
                                      state_type=OutputState,
                                      name=output_state,
                                      reference_value=projection_spec.value,
                                      reference_value_name='Projection_spec value for new InputState',
                                      context=context)
    #  Update output_state and output_states
    try:
        sender.output_states[output_state.name] = output_state
    # No OutputState(s) yet, so create them
    except AttributeError:
        from psyneulink.core.components.states.state import State_Base
        sender.output_states = ContentAddressableList(component_type=State_Base,
                                                      list=[output_state],
                                                      name=sender.name+'.output_states')

    output_state._instantiate_projections_to_state(projections=projection_spec, context=context)
