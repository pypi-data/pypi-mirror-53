# Princeton University licenses this file to You under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.  You may obtain a copy of the License at:
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.


# **************************************  ParameterState ******************************************************

"""

Overview
--------

ParameterStates belong to either a `Mechanism <Mechanism>` or a `Projection <Projection>`. A ParameterState is created
to represent each `modulatable parameter <ParameterState_Configurable_Parameters>` of the `Mechanism
<Mechanism>` or a `Projection <Projection>`, as well as those of the component's `function <Component_Function>`. A
ParameterState provides the current value of the parameter it represents during any relevant computations, and serves as
an interface for parameter modulation.

A ParameterState can receive one or more `ControlProjections  <ControlProjection>` and/or `LearningProjections
<LearningProjection>` that modify the value returned by the ParameterState according to the ParameterState's
`function <ParameterState.function>`. The Projections received by a ParameterState  are listed in its `mod_afferents
<ParameterState.mod_afferents>` attribute.

When the Mechanism or Projection to which a ParameterState belongs executes, that component and its function use the
ParameterState's value -- not the parameter attribute's value -- for any computation. A ParameterState's corresponding
attribute on the Mechanism, Projection, or Function to which it belongs (i.e. MyTransferMech.function.gain),
stores the "base value" of that parameter. The base value of a parameter is the variable of the ParameterState's
function. The base value can be viewed or changed at any time through this attribute.

The ParameterState value is available on the ParameterState itself, as well as the mod_name attribute of the Mechanism
or Projection to which it belongs (i.e. MyTransferMech.mod_gain would return the value of the "gain" ParameterState
of the MyTransferMech mechanism.)

.. note::
    Either of these options for looking up the value of the ParameterState will return the parameter state value that
    was used during the most recent execution. This means that if the value of MyTransferMech.function.gain (the
    base value) is updated after execution #1, the base value will change immediately, but the ParameterState value (and
    MyTransferMech.mod_gain) will not be computed again until execution #2.

    As a result, if either MyTransferMech.mod_gain or MyTransferMech.parameter_states["gain"].value is viewed in between
    execution #1 and execution #2, it will return the gain parameter state value that was used during execution 1.

.. _ParameterState_Creation:

Creating a ParameterState
-------------------------

ParameterStates are created automatically when the `Mechanism <Mechanism>` or `Projection <Projection>` to which they
belong is created.  The `owner <ParameterState.owner>` of a ParameterState must be a `Mechanism` or `MappingProjection`.
One ParameterState is created for each configurable parameter of its owner, as well as for each configurable parameter
of the owner's `function <Component.function>` (the `configurable parameters <ParameterState_Configurable_Parameters>`
of a Component are listed in its `user_params <Component.user_params>` and function_params <Component.function_params>`
dictionaries. Each ParameterState is created using the value specified for the corresponding parameter, as described
below.  The ParameterStates for the parameters of a Mechanism or Projection are listed in its
:keyword:`parameter_states` attribute.

COMMENT:
    FOR DEVELOPERS: The instantiation of ParameterStates for all of the `user_params` of a Component can be
                    suppressed if a *PARAMETER_STATES* entry is included and set to `NotImplemented` in the
                    paramClassDefaults dictionary of its class definition;  the instantiation of a ParameterState
                    for an individual parameter in user_params can be suppressed by including it in
                    exclude_from_parameter_states for the class (or one of its parent classes)
                    (see LearningProjection and EVCControlMechanism for examples, and `note
                    <ParameterStates_Suppression>` below for additional information about how
                    to suppress creation of a ParameterState for individual parameters.  This should be done
                    for any parameter than can take a value or a string that is a keyword as its specification
                    (i.e., of the arg for the parameter in the Component's constructor) but should not have a
                    ParameterState (e.g., input_state and output_state), as otherwise the
                    specification will be interpreted as a numeric parameter (in the case of a value) or
                    a parameter of the keyword's type, a ParameterState will be created, and then it's value,
                    rather than the parameter's actual value, will be returned when the parameter is accessed
                    using "dot notation" (this is because the getter for an attribute's property first checks
                    to see if there is a ParameterState for that attribute and, if so, returns the value of the
                    ParameterState).
COMMENT

.. _ParameterState_Specification:

*Specifying Parameters*
~~~~~~~~~~~~~~~~~~~~~~~

Parameters can be specified in one of several places:

    * In the **argument** of the constructor for the `Component <Component>` to which the parameter belongs
      (see `Component_Structural_Attributes` for additional details).
    ..
    * In a *parameter specification dictionary* assigned to the **params** argument in the constructor for the
      Component to which the parameter belongs. The entry for each parameter must use the name of the parameter
      (or a corresponding keyword) as its key, and the parameter's specification as its value (see
      `examples <ParameterState_Specification_Examples>` below). Parameters for a Component's
      `function <Component.function>` can be specified in an entry with the key *FUNCTION_PARAMS*, and a value that
      is itself a parameter specification dictionary containing an entry for each of the function's parameters to be
      specified.  When a value is assigned to a parameter in a specification dictionary, it overrides any value
      assigned to the argument for the parameter in the Component's constructor.
    ..
    * By direct assignment to the Component's attribute for the parameter
      (see `below <ParameterState_Configurable_Parameters>`).
    ..
    * In the `assign_params <Component.assign_params>` method for the Component.
    ..
    * In the **runtime_params** argument of a call to a Composition's `Run` method

.. _ParameterState_Value_Specification:

The specification of the initial value of a parameter can take any of the following forms:

    .. _ParameterState_Value_Assignment:

    * **Value** -- this must be a valid value for the parameter. It creates a default ParameterState,
      assigns the parameter's default value as the ParameterState's `value <ParameterState.value>`,
      and assigns the parameter's name as the name of the ParameterState.

    * **ParameterState reference** -- this must refer to an existing **ParameterState** object; its name must be the
      name of a parameter of the owner or of the owner's `function <Component.function>`, and its value must be a valid
      one for the parameter.

      .. note::
          This capability is provided for generality and potential
          future use, but its current use is not advised.

    .. _ParameterState_Modulatory_Specification:

    * **Modulatory specification** -- this can be an existing `ControlSignal` or `ControlProjection`,
      a `LearningSignal` or `LearningProjection`, a constructor or the class name for any of these, or the
      keywords *CONTROL*, *CONTROL_PROJECTION*, *LEARNING*, or *LEARNING_PROJECTION*.  Any of these create a default
      ParameterState, assign the parameter's default value as the ParameterState's `value <ParameterState.value>`,
      and assign the parameter's name as the name of the ParameterState.  They also create and/or assign the
      corresponding ModulatorySignal and ModulatoryProjection, and assign the ParameterState as the
      ModulatoryProjection's `receiver <Projection_Base.receiver>`. If the ModulatorySignal and/or
      ModulatoryProjection already exist, their value(s) must be valid one(s) for the parameter.  Note that only
      Control and Learning Modulatory components can be assigned to a ParameterState (Gating components cannot be
      used -- they can only be assigned to `InputStates <InputState>` and `OutputStates <OutputState>`).

    .. _ParameterState_Tuple_Specification:

    * **2-item tuple:** *(<value>, <Modulatory specification>)* -- this creates a default ParameterState, uses the value
      specification (1st item) as parameter's `value assignment <ParameterState_Value_Assignment>`, and assigns the
      parameter's name as the name of the ParameterState.  The Modulatory specification (2nd item) is used as the
      ParameterState's `modulatory assignment <ParameterState_Modulatory_Specification>`, and the ParameterState
      is assigned as the `receiver <Projection_Base.receiver>` for the corresponding `ModulatoryProjection
      <ModulatoryProjection>`.

      .. note::
          Currently, the `function <Component.function>` of a Component, although it can be specified as a parameter
          value, cannot be assigned a `ModulatorySignal <ModulatorySignal>` or modified in the **runtime_params**
          argument of a call to a Mechanism's `execute <Mechanism_Base.execute>` method. This may change in the future.

The value specified for a parameter (either explicitly or by default) is assigned to an attribute of the Component or
of the Component's `function <Mechanism_Base.function>` to which the parameter belongs.  The attribute has the same
name as the parameter, and can be referenced using standard Python attribute ("dot") notation;  for example, the value
of a parameter named *param* is assigned to an attribute named ``param`` that can be referenced as
``my_component.param``). The parameter's value is assigned as the **default value** for the ParameterState.

.. _ParameterStates_Suppression:

.. note::
   If the value of a parameter is specified as `NotImplemented`, or any non-numeric value that is not one of those
   listed above, then no ParameterState is created and the parameter cannot be modified by a `ModulatorySignal
   <ModulatorySignal>` or in the **runtime_params** argument of a call to a Mechanism's `execute
   <Mechanism_Base.execute>` method.

.. _ParameterState_Specification_Examples:

*Examples*
~~~~~~~~~~

In the following example, a Mechanism is created by specifying two of its parameters, as well as its
`function <Component.function>` and two of that function's parameters, each using a different specification format::

    >>> import psyneulink as pnl
    >>> my_mechanism = pnl.RecurrentTransferMechanism(
    ...                         size=5,
    ...                         noise=pnl.ControlSignal(),
    ...                         function=pnl.Logistic(
    ...                                         gain=(0.5, pnl.ControlSignal),
    ...                                         bias=(1.0, pnl.ControlSignal(modulation=pnl.ADDITIVE))))

COMMENT:
    If assigning a default ControlSignal makes the noise value the same as the
    default noise value, why are we using a ControlSignal here??
COMMENT

The first argument of the constructor for the Mechanism specifies its `size <Component.size>` parameter by
directly assigning a value to it.  The second specifies the `noise <RecurrentTransferMechanism.noise>` parameter
by assigning a default `ControlSignal`;  this will use the default value of the
`noise <RecurrentTransferMechanism.noise>` attribute.  The **function** argument is specified using the constructor for
a `Logistic` function, that specifies two of its parameters.  The `gain <Logistic.gain>` parameter
is specified using a tuple, the first item of which is the value to be assigned, and the second specifies
a default `ControlSignal`.  The `bias <Logistic.bias>` parameter is also specified using a tuple,
in this case with a constructor for the ControlSignal that specifies its `modulation <ControlSignal.modulation>`
parameter.

In the following example, a `MappingProjection` is created, and its
`matrix <MappingProjection.MappingProjection.matrix>` parameter is assigned a random weight matrix (using a
`matrix keyword <Matrix_Keywords>`) and `LearningSignal`::

    >>> my_input_mechanism = pnl.TransferMechanism()
    >>> my_output_mechanism = pnl.TransferMechanism()
    >>> my_mapping_projection = pnl.MappingProjection(sender=my_input_mechanism,
    ...                                               receiver=my_output_mechanism,
    ...                                               matrix=(pnl.RANDOM_CONNECTIVITY_MATRIX,
    ...                                                       pnl.LearningSignal))

.. note::
   The `matrix <MappingProjection.MappingProjection.matrix>` parameter belongs to the MappingProjection's
   `function <MappingProjection.MappingProjection.function>`;  however, since it has only one standard function,
   its arguments are available in the constructor for the Projection (see
   `Component_Specifying_Functions_and_Parameters` for a more detailed explanation).

The example below shows how to specify the parameters in the first example using a parameter specification dictionary::

    >>> my_mechanism = pnl.RecurrentTransferMechanism(
    ...                      noise=5,
    ...                      params={pnl.NOISE: pnl.CONTROL,
    ...                              pnl.FUNCTION: pnl.Logistic,
    ...                              pnl.FUNCTION_PARAMS:{
    ...                                     pnl.GAIN:(0.5,pnl.ControlSignal),
    ...                                     pnl.BIAS:(1.0,pnl.ControlSignal(modulation=pnl.ADDITIVE))}})

There are several things to note here.

First, the parameter specification dictionary must be assigned to the **params** argument of the constructor. Note that
if the parameter is specified in a parameter specification dictionary, the key for the parameter must be a string that
is the same as the name of parameter (i.e., identical to how it appears as an arg in the constructor; as is shown
for **noise** in the example), or using a keyword that resolves to such a string (as shown for *NOISE* in the
example).

Second, both methods for specifying a parameter -- directly in an argument for the parameter, or in an entry of a
parameter specification dictionary -- can be used within the same constructor.

If a particular parameter is specified in both ways (as is the case for **noise** in the example), the value in the
parameter specification dictionary takes priority (i.e., it is the value that will be assigned to the parameter).

Finally, the keyword *FUNCTION_PARAMS* can be used in a parameter specification dictionary to specify
parameters of the Component's `function <Component.function>`, as shown for the **gain** and **bias** parameters of
the Logistic function in the example.

The example below shows how to access ParameterState values vs base values, and demonstrates their differences:

    >>> my_transfer_mechanism = pnl.TransferMechanism(              #doctest: +SKIP
    ...                      noise=5.0,                             #doctest: +SKIP
    ...                      function=pnl.Linear(slope=2.0))        #doctest: +SKIP
    >>> assert my_transfer_mechanism.noise == 5.0                   #doctest: +SKIP
    >>> assert my_transfer_mechanism.mod_noise == [5.0]             #doctest: +SKIP
    >>> assert my_transfer_mechanism.function.slope == 2.0   #doctest: +SKIP
    >>> assert my_transfer_mechanism.mod_slope == [2.0]             #doctest: +SKIP

Notice that the noise attribute, which stores the base value for the noise ParameterState of my_transfer_mechanism, is
on my_transfer_mechanism, while the slope attribute, which stores the base value for the slope ParameterState of
my_transfer_mechanism, is on my_transfer_mechanism's function. However, mod_noise and mod_slope are both properties on
my_transfer_mechanism.

    >>> my_transfer_mechanism.noise = 4.0                           #doctest: +SKIP
    >>> my_transfer_mechanism.function.slope = 1.0           #doctest: +SKIP
    >>> assert my_transfer_mechanism.noise == 4.0                   #doctest: +SKIP
    >>> assert my_transfer_mechanism.mod_noise == [5.0]             #doctest: +SKIP
    >>> assert my_transfer_mechanism.function.slope == 1.0   #doctest: +SKIP
    >>> assert my_transfer_mechanism.mod_slope == [2.0]             #doctest: +SKIP

When the base values of noise and slope are updated, we can inspect these attributes immediately and observe that they
have changed. We do not observe a change in mod_noise or mod_slope because the ParameterState value will not update
until the mechanism executes.

    >>> my_transfer_mechanism.execute([10.0])                       #doctest: +SKIP
    >>> assert my_transfer_mechanism.noise == 4.0                   #doctest: +SKIP
    >>> assert my_transfer_mechanism.mod_noise == [4.0]             #doctest: +SKIP
    >>> assert my_transfer_mechanism.function.slope == 1.0   #doctest: +SKIP
    >>> assert my_transfer_mechanism.mod_slope == 1.0               #doctest: +SKIP

Now that the mechanism has executed, we can see that each ParameterState evaluated its function with the base value,
producing a modulated noise value of 4.0 and a modulated slope value of 1.0. These values were used by
my_transfer_mechanism and its Linear function when the mechanism executed.

.. _ParameterState_Structure:

Structure
---------

Every ParameterState is owned by a `Mechanism <Mechanism>` or `MappingProjection`. It can receive one or more
`ControlProjections <ControlProjection>` or `LearningProjections <LearningProjection>`, that are listed in its
`mod_afferents <ParameterState.mod_afferents>` attribute.  A ParameterState cannot receive
`PathwayProjections <PathwayProjection>` or `GatingProjections <GatingProjection>`.  When the ParameterState is
updated (i.e., its owner is executed), it uses the values of its ControlProjections and LearningProjections to
determine whether and how to modify its parameter's attribute value, which is then assigned as the ParameterState's
`value <ParameterState.value>` (see `ParameterState_Execution` for addition details). ParameterStates have the
following core attributes:

* `variable <ParameterState.variable>` - the parameter's attribute value; that is, the value assigned to the
  attribute for the parameter of the ParameterState's owner;  it can be thought of as the parameter's "base" value.
  It is used by its `function <ParameterState.function>` to determine the ParameterState's
  `value <ParameterState.value>`.  It must match the format (the number and type of elements) of the parameter's
  attribute value.

* `mod_afferents <ParameterState.mod_afferents>` - lists the `ModulatoryProjections <ModulationProjection>` received
  by the ParameterState.  These specify either modify the ParameterState's `function <ParameterState.function>`, or
  directly assign the `value <ParameterState.value>` of the ParameterState itself (see `ModulatorySignals_Modulation`).

* `function <ParameterState.function>` - takes the parameter's attribute value as its input, modifies it under the
  influence of any `ModulatoryProjections` it receives (listed in `mod_afferents <ParameterState.mod_afferents>`,
  and assigns the result as the ParameterState's `value <ParameterState.value>` which is used as the parameter's
  "actual" value.

* `value <ParameterState.value>` - the result of `function <ParameterState.function>`; used by the ParameterState's
  owner as the value of the parameter for which the ParameterState is responsible.

.. _ParameterState_Configurable_Parameters:

All of the configurable parameters of a Component -- that is, for which it has ParameterStates -- are listed in its
`user_params <Component.user_params>` attribute, which is a read-only dictionary with an entry for each parameter.
The parameters for a Component's `function <Component.function>` are listed both in a *FUNCTION_PARAMS* entry of the
`user_params <Component.user_params>` dictionary, and in their own `function_params <Component.function_params>`
attribute, which is also a read-only dictionary (with an entry for each of its function's parameters).  The
ParameterStates for a Mechanism or Projection are listed in its :keyword:`parameter_states` attribute, which is also
read-only.

An initial value can be assigned to a parameter in the corresponding argument of the constructor for the Component
(see `above <ParameterState_Value_Specification>`.  Parameter values can also be modified by a assigning a value to
the corresponding attribute, or in groups using the Component's `assign_params <Component.assign_params>` method.
The parameters of a Component's function can be modified by assigning a value to the corresponding attribute of the
Component's `function <Component.function>` attribute (e.g., ``myMechanism.function.my_parameter``)
or in *FUNCTION_PARAMS* dict in a call to the Component's `assign_params <Component.assign_params>` method.
See `Mechanism_ParameterStates` for additional information.


.. _ParameterState_Execution:

Execution
---------

A ParameterState cannot be executed directly.  It is executed when the Component to which it belongs is executed.
When this occurs, the ParameterState executes any `ModulatoryProjections` it receives, the values of which
modulate parameters of the ParameterState's `function <ParameterState.function>`.  The ParameterState then calls
its `function <ParameterState.function>` and the result is assigned as its `value <ParameterState.value>`.  The
ParameterState's `value <ParameterState.value>` is used as the value of the corresponding parameter by the Component,
or by its own `function <Component.function>`.

.. note::
   It is important to note the distinction between the `function <ParameterState.function>` of a ParameterState,
   and the `function <Component.function>` of the Component to which it belongs. The former is used to determine the
   value of a parameter used by the latter (see `figure <ModulatorySignal_Anatomy_Figure>`, and `State_Execution` for
   additional details).

.. _ParameterState_Class_Reference:

Class Reference
---------------

"""

import inspect
import warnings

import numpy as np
import typecheck as tc

from psyneulink.core.components.component import Component, function_type, method_type, parameter_keywords
from psyneulink.core.components.functions.function import get_param_value_for_keyword
from psyneulink.core.components.shellclasses import Mechanism, Projection
from psyneulink.core.components.states.modulatorysignals.modulatorysignal import ModulatorySignal
from psyneulink.core.components.states.state import StateError, State_Base, _instantiate_state, state_type_keywords
from psyneulink.core.globals.context import ContextFlags
from psyneulink.core.globals.keywords import \
    CONTEXT, CONTROL_PROJECTION, CONTROL_SIGNAL, CONTROL_SIGNALS, FUNCTION, FUNCTION_PARAMS, \
    LEARNING_SIGNAL, LEARNING_SIGNALS, MECHANISM, NAME, PARAMETER_STATE, PARAMETER_STATES, \
    PARAMETER_STATE_PARAMS, PATHWAY_PROJECTION, PROJECTION, PROJECTIONS, PROJECTION_TYPE, REFERENCE_VALUE, SENDER, VALUE
from psyneulink.core.globals.preferences.basepreferenceset import is_pref_set
from psyneulink.core.globals.preferences.preferenceset import PreferenceLevel
from psyneulink.core.globals.utilities \
    import ContentAddressableList, ReadOnlyOrderedDict, is_iterable, is_numeric, is_value_spec, iscompatible

__all__ = [
    'ParameterState', 'ParameterStateError', 'state_type_keywords',
]

state_type_keywords = state_type_keywords.update({PARAMETER_STATE})


class ParameterStateError(Exception):
    def __init__(self, error_value):
        self.error_value = error_value

    def __str__(self):
        return repr(self.error_value)


class ParameterState(State_Base):
    """
    ParameterState(                                              \
    owner,                                                       \
    reference_value=None                                         \
    function=LinearCombination(operation=PRODUCT),               \
    variable=None,                                               \
    size=None,                                                   \
    parameter_modulation_operation=Modulation.MULTIPLY,          \
    params=None,                                                 \
    name=None,                                                   \
    prefs=None)

    Subclass of `State <State>` that represents and possibly modifies the parameter of
    a `Mechanism <Mechanism>`, `Projection <Projection>`, or its `Function`.


    COMMENT:

        Description
        -----------
            The ParameterState class is a componentType in the State category of Function,
            Its FUNCTION executes the Projections that it receives and updates the ParameterState's value

        Class attributes
        ----------------
            + componentType (str) = kwMechanisParameterState
            + classPreferences
            + classPreferenceLevel (PreferenceLevel.Type)
            + paramClassDefaults (dict)
                + FUNCTION (Linear)
                + PROJECTION_TYPE (CONTROL_PROJECTION)

        Class methods
        -------------
            _instantiate_function: insures that function is ARITHMETIC) (default: Operation.PRODUCT)
            update: updates self.value from Projections, base_value and runtime in PARAMETER_STATE_PARAMS

        StateRegistry
        -------------
            All ParameterStates are registered in StateRegistry, which maintains an entry for the subclass,
              a count for all instances of it, and a dictionary of those instances

    COMMENT

    COMMENT:

    Arguments
    ---------

    owner : Mechanism or MappingProjection
        the `Mechanism <Mechanism>` or `MappingProjection` to which to which the ParameterState belongs; it must be
        specified or determinable from the context in which the ParameterState is created. The owner of a ParameterState
        for the parameter of a `function <Component.function>` should be specified as the Mechanism or Projection to
        which the function belongs.

    reference_value : number, list or np.ndarray
        specifies the default value of the parameter for which the ParameterState is responsible.

    variable : number, list or np.ndarray
        specifies the parameter's initial value and attribute value — that is, the value of the attribute of the
        ParameterState's owner or its `function <Component.function>` assigned to the parameter.

    size : int, list or np.ndarray of ints
        specifies variable as array(s) of zeros if **variable** is not passed as an argument;
        if **variable** is specified, it takes precedence over the specification of **size**.
        As an example, the following mechanisms are equivalent::
            T1 = TransferMechanism(size = [3, 2])
            T2 = TransferMechanism(default_variable = [[0, 0, 0], [0, 0]])

    function : Function or method : default LinearCombination(operation=SUM)
        specifies the function used to convert the parameter's attribute value (same as the ParameterState's
        `variable <ParameterState.variable>`) to the ParameterState's `value <ParameterState.value>`.

    params : Dict[param keyword: param value] : default None
        a `parameter dictionary <ParameterState_Specification>` that can be used to specify the parameters for
        the ParameterState or its function, and/or a custom function and its parameters.  Values specified for
        parameters in the dictionary override any assigned to those parameters in arguments of the constructor.

    name : str : default see `name <ParameterState.name>`
        specifies the name of the ParameterState; see ParameterState `name <ParameterState.name>` for details.

    prefs : PreferenceSet or specification dict : default State.classPreferences
        specifies the `PreferenceSet` for the ParameterState; see `prefs <ParameterState.prefs>` for details.

    COMMENT

    Attributes
    ----------

    owner : Mechanism or MappingProjection
        the `Mechanism <Mechanism>` or `MappingProjection` to which the ParameterState belongs.

    mod_afferents : Optional[List[Projection]]
        a list of the `ModulatoryProjection <ModulatoryProjection>` that project to the ParameterState (i.e.,
        for which it is a `receiver <Projection_Base.receiver>`); these can be
        `ControlProjection(s) <ControlProjection>` and/or `LearningProjection(s) <LearningProjection>`,
        but not `GatingProjection <GatingProjection>`.  The `value <ModulatoryProjection_Base.value>` of each
        must match the format (number and types of elements) of the ParameterState's
        `variable <ParameterState.variable>`.

    variable : number, list or np.ndarray
        the parameter's attribute value — that is, the value of the attribute of the
        ParameterState's owner or its `function <Component.function>` assigned to the parameter.

    function : Function : default Linear
        converts the parameter's attribute value (same as the ParameterState's `variable <ParameterState.variable>`)
        to the ParameterState's `value <ParameterState.value>`, under the influence of any
        `ModulatoryProjections <ModulatoryProjection>` received by the ParameterState (and listed in its
        `mod_afferents <ParameterState.mod_afferents>` attribute.  The result is assigned as the ParameterState's
        `value <ParameterState>`.

    value : number, List[number] or np.ndarray
        the result returned by the ParameterState's `function <ParameterState.function>`, and used by the
        ParameterState's owner or its `function <Component.function>` as the value of the parameter for which the
        ParmeterState is responsible.  Note that this is not necessarily the same as the parameter's attribute value
        (that is, the value of the owner's attribute for the parameter), since the ParameterState's
        `function <ParameterState.function>` may modify the latter under the influence of its
        `mod_afferents <ParameterState.mod_afferents>`.

    name : str
        the name of the ParameterState; same as the name of the attribute for the Parameter to which the
        ParameterState corresponds.

        .. note::
            Unlike other PsyNeuLink components, State names are "scoped" within a Mechanism, meaning that States with
            the same name are permitted in different Mechanisms.

    prefs : PreferenceSet or specification dict
        the `PreferenceSet` for the ParameterState; if it is not specified in the **prefs** argument of the
        constructor, a default is assigned using `classPreferences` defined in __init__.py (see :doc:`PreferenceSet
        <LINK>` for details).
    """

    #region CLASS ATTRIBUTES

    componentType = PARAMETER_STATE
    paramsType = PARAMETER_STATE_PARAMS

    stateAttributes = State_Base.stateAttributes

    connectsWith = [CONTROL_SIGNAL, LEARNING_SIGNAL]
    connectsWithAttribute = [CONTROL_SIGNALS, LEARNING_SIGNALS]
    projectionSocket = SENDER
    modulators = [CONTROL_SIGNAL, LEARNING_SIGNAL]
    canReceive = modulators

    classPreferenceLevel = PreferenceLevel.TYPE
    # Any preferences specified below will override those specified in TYPE_DEFAULT_PREFERENCES
    # Note: only need to specify setting;  level will be assigned to TYPE automatically
    # classPreferences = {
    #     PREFERENCE_SET_NAME: 'ParameterStateCustomClassPreferences',
    #     PREFERENCE_KEYWORD<pref>: <setting>...}

    paramClassDefaults = State_Base.paramClassDefaults.copy()
    paramClassDefaults.update({PROJECTION_TYPE: CONTROL_PROJECTION})
    #endregion

    tc.typecheck
    def __init__(self,
                 owner,
                 reference_value=None,
                 variable=None,
                 size=None,
                 function=None,
                 projections=None,
                 params=None,
                 name=None,
                 prefs:is_pref_set=None,
                 **kwargs):

        # If context is not COMPONENT or CONSTRUCTOR, raise exception
        context = kwargs.pop(CONTEXT, None)
        if context is None:
            raise ParameterStateError(f"Contructor for {self.__class__.__name__} cannot be called directly"
                                      f"(context: {context}")

        # FIX: UPDATED TO INCLUDE LEARNING [CHANGE THIS TO INTEGRATOR FUNCTION??]
        # # Reassign default for MATRIX param of MappingProjection
        # if isinstance(owner, MappingProjection) and name is MATRIX:
        #     function = LinearCombination(operation=SUM)

        # Assign args to params and functionParams dicts
        params = self._assign_args_to_param_dicts(function=function,
                                                  params=params)

        self.reference_value = reference_value

        # Validate sender (as variable) and params, and assign to variable and paramInstanceDefaults
        # Note: pass name of Mechanism (to override assignment of componentName in super.__init__)
        super(ParameterState, self).__init__(owner,
                                             variable=variable,
                                             size=size,
                                             projections=projections,
                                             function=function,
                                             params=params,
                                             name=name,
                                             prefs=prefs,
                                             context=context)

    def _validate_params(self, request_set, target_set=None, context=None):
        """Insure that ParameterState (as identified by its name) is for a valid parameter of the owner

        Parameter can be either owner's, or owner's function
        """

        # If the parameter is not in either the owner's user_params dict or its function_params dict, throw exception
        if not self.name in self.owner.user_params.keys() and not self.name in self.owner.function_params.keys():
            raise ParameterStateError("Name of requested ParameterState ({}) does not refer to a valid parameter "
                                      "of the component ({}) or its function ({})".
                                      format(self.name,
                                             # self.owner.function.__class__.__name__,
                                             self.owner.name,
                                             self.owner.function.componentName))

        super()._validate_params(request_set=request_set, target_set=target_set, context=context)

    def _validate_against_reference_value(self, reference_value):
        """Validate that value of the State is compatible with the reference_value

        reference_value is the value of the parameter to which the ParameterState is assigned
        """
        if reference_value is not None and not iscompatible(np.squeeze(reference_value), np.squeeze(self.defaults.value)):
            iscompatible(np.squeeze(reference_value), np.squeeze(self.defaults.value))
            name = self.name or ""
            raise ParameterStateError("Value specified for {} {} of {} ({}) is not compatible "
                                      "with its expected format ({})".
                                      format(name, self.componentName, self.owner.name, self.defaults.value, reference_value))

    def _instantiate_projections(self, projections, context=None):
        """Instantiate Projections specified in PROJECTIONS entry of params arg of State's constructor

        Disallow any PathwayProjections
        Call _instantiate_projections_to_state to assign ModulatoryProjections to .mod_afferents

        """

        # MODIFIED 7/8/17
        # FIX:  THIS SHOULD ALSO LOOK FOR OTHER FORMS OF SPECIFICATION
        # FIX:  OF A PathwayProjection (E.G., TARGET STATE OR MECHANISM)

        from psyneulink.core.components.projections.pathway.pathwayprojection import PathwayProjection_Base
        pathway_projections = [proj for proj in projections if isinstance(proj, PathwayProjection_Base)]
        if pathway_projections:
            pathway_proj_names = []
            for proj in pathway_projections:
                pathway_proj_names.append(proj.name + ' ')
            raise StateError("{} not allowed for {}: {}".
                             format(PathwayProjection_Base.__self__.__name__,
                                    self.__class__.__name__,
                                    pathway_proj_names))

        self._instantiate_projections_to_state(projections=projections, context=context)

    def _check_for_duplicate_projections(self, projection):
        """Check if projection is redundant with one in mod_afferents of ParameterState

        Check for any instantiated projection in mod_afferents with the same sender as projection
        or one in deferred_init status with sender specification that is the same type as projection.

        Returns redundant Projection if found, otherwise False.
        """

        duplicate = next(iter([proj for proj in self.mod_afferents
                               if ((proj.sender == projection.sender and proj != projection)
                                   or (proj.initialization_status == ContextFlags.DEFERRED_INIT
                                       and proj.init_args[SENDER] == type(projection.sender)))]), None)
        if duplicate and self.verbosePref or self.owner.verbosePref:
            from psyneulink.core.components.projections.projection import Projection
            warnings.warn(f'{Projection.__name__} from {projection.sender.name}  {projection.sender.__class__.__name__}'
                          f' of {projection.sender.owner.name} to {self.name} {self.__class__.__name__} of '
                          f'{self.owner.name} already exists; will ignore additional one specified ({projection.name}).')
        return duplicate


    @tc.typecheck
    def _parse_state_specific_specs(self, owner, state_dict, state_specific_spec):
        """Get connections specified in a ParameterState specification tuple

        Tuple specification can be:
            (state_spec, projections)
        Assumes that state_spec has already been extracted and used by _parse_state_spec

        Returns params dict with PROJECTIONS entries if any of these was specified.

        """
        from psyneulink.core.components.projections.projection import _parse_connection_specs, _is_projection_spec

        params_dict = {}
        state_spec = state_specific_spec

        if isinstance(state_specific_spec, dict):
            return None, state_specific_spec

        elif isinstance(state_specific_spec, tuple):

            tuple_spec = state_specific_spec

            # GET STATE_SPEC (PARAM VALUE) AND ASSIGN PROJECTIONS_SPEC **********************************************

            # 2-item tuple specification
            if len(tuple_spec) == 2:

                # 1st item is a value, so treat as State spec (and return to _parse_state_spec to be parsed)
                #   and treat 2nd item as Projection specification
                if is_numeric(tuple_spec[0]):
                    state_spec = tuple_spec[0]
                    reference_value = state_dict[REFERENCE_VALUE]
                    # Assign value so sender_dim is skipped below
                    # (actual assignment is made in _parse_state_spec)
                    if reference_value is None:
                        state_dict[REFERENCE_VALUE]=state_spec
                    elif  not iscompatible(state_spec, reference_value):
                        raise StateError("Value in first item of 2-item tuple specification for {} of {} ({}) "
                                         "is not compatible with its {} ({})".
                                         format(ParameterState.__name__, owner.name, state_spec,
                                                REFERENCE_VALUE, reference_value))
                    projections_spec = tuple_spec[1]

                elif _is_projection_spec(tuple_spec[0], include_matrix_spec=True):
                    state_spec, projections_spec = tuple_spec

                # Tuple is Projection specification that is used to specify the State,
                else:
                    # return None in state_spec to suppress further, recursive parsing of it in _parse_state_spec
                    state_spec = None
                    if tuple_spec[0] != self:
                        # If 1st item is not the current state (self), treat as part of the projection specification
                        projections_spec = tuple_spec
                    else:
                        # Otherwise, just use 2nd item as projection spec
                        state_spec = None
                        projections_spec = tuple_spec[1]

            # 3- or 4-item tuple specification
            elif len(tuple_spec) in {3,4}:
                # Tuple is projection specification that is used to specify the State,
                #    so return None in state_spec to suppress further, recursive parsing of it in _parse_state_spec
                state_spec = None
                # Reduce to 2-item tuple Projection specification
                projection_item = tuple_spec[3] if len(tuple_spec)==4 else None
                projections_spec = (tuple_spec[0],projection_item)

            # GET PROJECTIONS IF SPECIFIED *************************************************************************

            try:
                projections_spec
            except UnboundLocalError:
                pass
            else:
                try:
                    params_dict[PROJECTIONS] = _parse_connection_specs(self,
                                                                       owner=owner,
                                                                       connections=projections_spec)

                    # Parse the value of all of the Projections to get/validate parameter value
                    from psyneulink.core.components.projections.modulatory.controlprojection import ControlProjection
                    from psyneulink.core.components.projections.modulatory.learningprojection import LearningProjection

                    for projection_spec in params_dict[PROJECTIONS]:
                        if state_dict[REFERENCE_VALUE] is None:
                            # FIX: - PUTTING THIS HERE IS A HACK...
                            # FIX:     MOVE TO _parse_state_spec UNDER PROCESSING OF ProjectionTuple SPEC
                            # FIX:     USING _get_state_for_socket
                            # from psyneulink.core.components.projections.projection import _parse_projection_spec

                            # defaults.value?
                            mod_signal_value = projection_spec.state.value \
                                if isinstance(projection_spec.state, State_Base) else None

                            mod_projection = projection_spec.projection
                            if isinstance(mod_projection, dict):
                                if mod_projection[PROJECTION_TYPE] not in {ControlProjection, LearningProjection}:
                                    raise ParameterStateError("PROGRAM ERROR: {} other than {} or {} ({}) found "
                                                              "in specification tuple for {} param of {}".
                                                              format(Projection.__name__,
                                                                     ControlProjection.__name__,
                                                                     LearningProjection.__name__,
                                                                     mod_projection, state_dict[NAME], owner.name))
                                elif VALUE in mod_projection:
                                    mod_proj_value = mod_projection[VALUE]
                                else:
                                    mod_proj_value = None
                            elif isinstance(mod_projection, Projection):
                                if not isinstance(mod_projection, (ControlProjection, LearningProjection)):
                                    raise ParameterStateError("PROGRAM ERROR: {} other than {} or {} ({}) found "
                                                              "in specification tuple for {} param of {}".
                                                              format(Projection.__name__,
                                                                     ControlProjection.__name__,
                                                                     LearningProjection.__name__,
                                                                     mod_projection, state_dict[NAME], owner.name))
                                elif mod_projection.initialization_status == ContextFlags.DEFERRED_INIT:
                                    continue
                                mod_proj_value = mod_projection.defaults.value
                            else:
                                raise ParameterStateError("Unrecognized Projection specification for {} of {} ({})".
                                                      format(self.name, owner.name, projection_spec))

                            # FIX: 11/25/17 THIS IS A MESS:  CHECK WHAT IT'S ACTUALLY DOING
                            # If ModulatoryProjection's value is not specified, try to assign one
                            if mod_proj_value is None:
                                # If not specified for State, assign that
                                if VALUE not in state_dict or state_dict[VALUE] is None:
                                    state_dict[VALUE] = mod_signal_value
                                # If value has been assigned, make sure value is the same for ModulatorySignal
                                elif state_dict[VALUE] != mod_signal_value:
                                    # If the values differ, assign None so that State's default is used
                                    state_dict[VALUE] = None
                                    # No need to check any more ModulatoryProjections
                                    break

                            #
                            else:
                                state_dict[VALUE] = mod_proj_value

                except ParameterStateError:
                    raise ParameterStateError("Tuple specification in {} specification dictionary "
                                          "for {} ({}) is not a recognized specification for one or more "
                                          "{}s, {}s, or {}s that project to it".
                                          format(ParameterState.__name__,
                                                 owner.name,
                                                 projections_spec,
                                                 Mechanism.__name__,
                                                 ModulatorySignal.__name__,
                                                 Projection.__name__))

        elif state_specific_spec is not None:
            raise ParameterStateError("PROGRAM ERROR: Expected tuple or dict for {}-specific params but, got: {}".
                                  format(self.__class__.__name__, state_specific_spec))

        return state_spec, params_dict

    @staticmethod
    def _get_state_function_value(owner, function, variable):
        """Return parameter variable (since ParameterState's function never changes the form of its variable"""
        return variable

    def _get_fallback_variable(self, context=None):
        """
        Get backingfield ("base") value of param of function of Mechanism to which the ParameterState belongs.
        """

        # FIX 3/6/19: source does not yet seem to have been assigned to owner.function
        return getattr(self.source.parameters, self.name)._get(context)

    @property
    def pathway_projections(self):
        raise ParameterStateError("PROGRAM ERROR: Attempt to access {} for {}; {}s do not have {}s".
                                  format(PATHWAY_PROJECTION, self.name, PARAMETER_STATE, PATHWAY_PROJECTION))

    @pathway_projections.setter
    def pathway_projections(self, value):
        raise ParameterStateError("PROGRAM ERROR: Attempt to assign {} to {}; {}s cannot accept {}s".
                                  format(PATHWAY_PROJECTION, self.name, PARAMETER_STATE, PATHWAY_PROJECTION))

def _instantiate_parameter_states(owner, function=None, context=None):
    """Call _instantiate_parameter_state for all params in user_params to instantiate ParameterStates for them

    If owner.params[PARAMETER_STATE] is None or False:
        - no ParameterStates will be instantiated.
    Otherwise, instantiate ParameterState for each allowable param in owner.user_params
    :param function:

    """

    # TBI / IMPLEMENT: use specs to implement ParameterStates below

    owner._parameter_states = ContentAddressableList(component_type=ParameterState,
                                                     name=owner.name+'.parameter_states')

    # Check that all ParameterStates for owner have not been explicitly suppressed
    #    (by assigning `NotImplemented` to PARAMETER_STATES entry of paramClassDefaults)
    try:
        if owner.params[PARAMETER_STATES] is NotImplemented:
            return
    except KeyError:
        # PARAMETER_STATES not specified at all, so OK to continue and construct them
        pass

    try:
        owner.user_params
    except AttributeError:
        return
    # Instantiate ParameterState for each param in user_params (including all params in function_params dict),
    #     using its value as the state_spec
    # Exclude input_states and output_states which are also in user_params
    # IMPLEMENTATION NOTE:  Use user_params_for_instantiation since user_params may have been overwritten
    #                       when defaults were assigned to paramsCurrent in Component.__init__,
    #                       (since that will assign values to the properties of each param;
    #                       and that, in turn, will overwrite their current values with the defaults from paramsCurrent)
    for param_name, param_value in owner.user_params_for_instantiation.items():
        # Skip any parameter that has been specifically excluded
        if param_name in owner.exclude_from_parameter_states:
            continue
        if hasattr(owner.parameters, param_name) and not getattr(owner.parameters, param_name).modulable:
            # skip non modulable parameters
            continue

        _instantiate_parameter_state(owner, param_name, param_value, context=context, function=function)


def _instantiate_parameter_state(owner, param_name, param_value, context, function=None):
    """Call _instantiate_state for allowable params, to instantiate a ParameterState for it

    Include ones in owner.user_params[FUNCTION_PARAMS] (nested iteration through that dict)
    Exclude if it is a:
        ParameterState that already exists (e.g., in case of a call from Component.assign_params)
        non-numeric value (including NotImplemented, False or True)
            unless it is:
                a tuple (could be one specifying Modulatory Component)
                a dict with the name FUNCTION_PARAMS (otherwise exclude)
        function or method
            IMPLEMENTATION NOTE: FUNCTION_RUNTIME_PARAM_NOT_SUPPORTED
            (this is because paramInstanceDefaults[FUNCTION] could be a class rather than an bound method;
            i.e., not yet instantiated;  could be rectified by assignment in _instantiate_function)
    # FIX: UPDATE WITH MODULATION_MODS
    # FIX:    CHANGE TO IntegratorFunction FUnction ONCE LearningProjection MODULATES ParameterState Function:
    If param_name is FUNCTION_PARAMS and param is a matrix (presumably for a MappingProjection)
        modify ParameterState's function to be LinearCombination (rather Linear which is the default)
    """
    from psyneulink.core.components.states.modulatorysignals.modulatorysignal import _is_modulatory_spec
    from psyneulink.core.components.projections.modulatory.modulatoryprojection import ModulatoryProjection_Base

    def _get_tuple_for_single_item_modulatory_spec(obj, name, value):
        """Return (<default param value>, <modulatory spec>) for modulatory spec
        """
        try:
            param_default_value = obj.get_constructor_defaults()[name]
            # Only assign default value if it is not None
            if param_default_value is not None:
                return (param_default_value, value)
            else:
                return value
        except KeyError:
            raise ParameterStateError("Unrecognized specification for {} paramater of {} ({})".
                                      format(param_name, owner.name, param_value))

    # EXCLUSIONS:

    # # Skip if ParameterState already exists (e.g., in case of call from Component.assign_params)
    # if param_name in owner.ParameterStates:
    #     return

    if param_value is NotImplemented:
        return
    # Allow numerics but omit booleans (which are treated by is_numeric as numerical)
    if is_numeric(param_value) and not isinstance(param_value, bool):
        pass
    # Only allow a FUNCTION_PARAMS dict
    elif isinstance(param_value, (ReadOnlyOrderedDict, dict)) and param_name is FUNCTION_PARAMS:
        pass
    # Allow ModulatoryProjection
    elif isinstance(param_value, Projection):
        if isinstance(param_value, ModulatoryProjection_Base):
            pass
        else:
            return
    # Allow Projection class
    elif inspect.isclass(param_value) and issubclass(param_value, Projection):
        if issubclass(param_value, (ModulatoryProjection_Base)):
            pass
        else:
            return

    elif _is_modulatory_spec(param_value, include_matrix_spec=False) and not isinstance(param_value, tuple):
        # If parameter is a single Modulatory specification (e.g., ControlSignal, or CONTROL, etc.)
         #  try to place it in a tuple (for interpretation by _parse_state_spec) using default value as 1st item
        #   (note: exclude matrix since it is allowed as a value specification but not a projection reference)
        try:
            param_value = _get_tuple_for_single_item_modulatory_spec(function, param_name, param_value)
        except ParameterStateError:
            param_value = _get_tuple_for_single_item_modulatory_spec(owner, param_name, param_value)

    # Allow tuples (could be spec that includes a Projection or Modulation)
    elif isinstance(param_value, tuple):
        # # FIX: EXTRACT VALUE HERE (AS IN Component.__init__?? [4/18/17]
        # param_value = owner._get_param_value_from_tuple(param_value)
        pass
    # Allow if it is a keyword for a parameter
    elif isinstance(param_value, str) and param_value in parameter_keywords:
        pass
    # Exclude function (see docstring above)
    elif param_name is FUNCTION:
        return
    # (7/19/17 CW) added this if statement below while adding `hetero` and `auto` and AutoAssociativeProjections: this
    # allows `hetero` to be specified as a matrix, while still generating a ParameterState
    elif isinstance(param_value, np.ndarray) or isinstance(param_value, np.matrix):
        pass
    # Exclude all others
    else:
        return

    # Assign ParameterStates to Component for parameters of its function (function_params), except for ones that are:
    #    - another component
    #    - a function or method
    #    - have a value of None (see IMPLEMENTATION_NOTE below)
    #    - they have the same name as another parameter of the component (raise exception for this)
    if param_name is FUNCTION_PARAMS:
        for function_param_name in param_value.keys():
            if (hasattr(function.parameters, function_param_name) and
                    not getattr(function.parameters, function_param_name).modulable):
                # skip non modulable function parameters
                continue

            function_param_value = param_value[function_param_name]

            # IMPLEMENTATION NOTE:
            # The following is necessary since, if ANY parameters of a function are specified, entries are made
            #    in the FUNCTION_PARAMS dict of its owner for ALL of the function's params;  however, their values
            #    will be set to None (and there may not be any relevant paramClassDefaults or a way to determine a
            #    default; e.g., the length of the array for the weights or exponents params for LinearCombination).
            #    Therefore, None will be passed as the reference_value, which will cause validation of the
            #    ParameterState's function (in _instantiate_function()) to fail.
            #  Current solution is to simply not instantiate a ParameterState for any function_param that has
            #    not been explicitly specified
            if function_param_value is None:
                continue

            if not _is_legal_param_value(owner, function_param_value):
                continue

            # Raise exception if the function parameter's name is the same as one that already exists for its owner
            if function_param_name in owner.user_params:
                if inspect.isclass(function):
                    function_name = function.__name__
                else:
                    function_name= function.name
                raise ParameterStateError("PROGRAM ERROR: the function ({}) of a component ({}) has a parameter ({}) "
                                          "with the same name as a parameter of the component itself".
                                          format(function_name, owner.name, function_param_name))

            elif (_is_modulatory_spec(function_param_value, include_matrix_spec=False)
                  and not isinstance(function_param_value, tuple)):
                # If parameter is a single Modulatory specification (e.g., ControlSignal, or CONTROL, etc.)
                # try to place it in a tuple (for interpretation by _parse_state_spec) using default value as 1st item
                #   (note: exclude matrix since it is allowed as a value specification vs. a projection reference)
                try:
                    function_param_value = _get_tuple_for_single_item_modulatory_spec(
                        function,
                        function_param_name,
                        function_param_value
                    )
                except ParameterStateError:
                    function_param_value = _get_tuple_for_single_item_modulatory_spec(
                        owner,
                        function_param_name,
                        function_param_value
                    )


            # # FIX: 10/3/17 - ??MOVE THIS TO _parse_state_specific_specs ----------------
            # # Use function_param_value as constraint
            # # IMPLEMENTATION NOTE:  need to copy, since _instantiate_state() calls _parse_state_value()
            # #                       for constraints before state_spec, which moves items to subdictionaries,
            # #                       which would make them inaccessible to the subsequent parse of state_spec
            from psyneulink.core.components.states.modulatorysignals.modulatorysignal import ModulatorySignal
            from psyneulink.core.components.mechanisms.modulatory.modulatorymechanism import ModulatoryMechanism_Base
            if (
                is_iterable(function_param_value)
                and any(isinstance(item, (ModulatorySignal, ModulatoryProjection_Base, ModulatoryMechanism_Base)) for item in function_param_value)
            ):
                reference_value = function_param_value
            else:
                from copy import deepcopy
                reference_value = deepcopy(function_param_value)

            # Assign parameterState for function_param to the component
            state = _instantiate_state(owner=owner,
                                      state_type=ParameterState,
                                      name=function_param_name,
                                      state_spec=function_param_value,
                                      reference_value=reference_value,
                                      reference_value_name=function_param_name,
                                      params=None,
                                      context=context)
            if state:
                owner._parameter_states[function_param_name] = state
                # will be parsed on assignment of function
                # FIX: if the function is manually changed after assignment,
                # FIX: the source will remain pointing to the original Function
                state.source = FUNCTION

    elif _is_legal_param_value(owner, param_value):
        state = _instantiate_state(owner=owner,
                                  state_type=ParameterState,
                                  name=param_name,
                                  state_spec=param_value,
                                  reference_value=param_value,
                                  reference_value_name=param_name,
                                  params=None,
                                  context=context)
        if state:
            owner._parameter_states[param_name] = state
            state.source = owner


def _is_legal_param_value(owner, value):

    from psyneulink.core.components.mechanisms.modulatory.control.controlmechanism import _is_control_spec
    from psyneulink.core.components.mechanisms.modulatory.control.gating.gatingmechanism import _is_gating_spec

    # LEGAL PARAMETER VALUES:

    # # lists, arrays or numeric values
    if is_value_spec(value):
        return True

    # tuple, first item of which is a legal parameter value
    #     note: this excludes (param_name, Mechanism) tuples used to specify a ParameterState
    #           (e.g., if specified for the control_signals param of ControlMechanism)
    if isinstance(value, tuple):
        if _is_legal_param_value(owner, value[0]):
            return True

    if isinstance(value, dict) and VALUE in value:
        return True

    if _is_control_spec(value) or _is_gating_spec(value):
        return True

    # keyword that resolves to one of the above
    if get_param_value_for_keyword(owner, value) is not None:
        return True

    # Assignment of ParameterState for Component objects, function or method are not currently supported
    if isinstance(value, (function_type, method_type, Component)):
        return False


def _get_parameter_state(sender_owner, sender_type, param_name, component):
    """Return ParameterState for named parameter of a Mechanism requested by owner
    """

    # Validate that component is a Mechanism or Projection
    if not isinstance(component, (Mechanism, Projection)):
        raise ParameterStateError("Request for {} of a component ({}) that is not a {} or {}".
                                  format(PARAMETER_STATE, component, MECHANISM, PROJECTION))

    try:
        return component._parameter_states[param_name]
    except KeyError:
        # Check that param (named by str) is an attribute of the Mechanism
        if not (hasattr(component, param_name) or hasattr(component.function, param_name)):
            raise ParameterStateError("{} (in specification of {}  {}) is not an attribute "
                                        "of {} or its function"
                                        .format(param_name, sender_type, sender_owner.name, component))
        # Check that the Mechanism has a ParameterState for the param
        if not param_name in component._parameter_states.names:
            raise ParameterStateError("There is no ParameterState for the parameter ({}) of {} "
                                        "specified in {} for {}".
                                        format(param_name, component.name, sender_type, sender_owner.name))
