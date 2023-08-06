# Princeton University licenses this file to You under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.  You may obtain a copy of the License at:
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.


# *******************************************  InputState *****************************************************
#
"""

Overview
--------

The purpose of an InputState is to receive and combine inputs to a `Mechanism`, allow them to be modified, and provide
them to the Mechanism's `function <Mechanism_Base.function>`. An InputState receives input to a `Mechanism`
provided by the `Projections <Projection>` to that Mechanism from others in a `Process` or `System`.  If the
InputState belongs to an `ORIGIN` Mechanism (see `role of Mechanisms in Processes and Systems
<Mechanism_Role_In_Processes_And_Systems>`), then it receives the input specified when that Process or System is
`run <Run>`.  The `PathwayProjections <PathWayProjection>` received by an InputState are listed in its `path_afferents
<InputState.path_afferents>`, and its `ModulatoryProjections <ModulatoryProjection>` in its `mod_afferents
<InputState.mod_afferents>` attribute.  Its `function <InputState.function>` combines the values received from its
PathWayProjections, modifies the combined value according to value(s) any ModulatoryProjections it receives, and
provides the result to the assigned item of its owner Mechanism's `variable <Mechanism_Base.variable>` and
`input_values <Mechanism_Base.input_values>` attributes (see `below` and `Mechanism InputStates <Mechanism_InputStates>`
for additional details about the role of InputStates in Mechanisms, and their assignment to the items of a Mechanism's
`variable <Mechanism_Base.variable>` attribute).

.. _InputState_Creation:

Creating an InputState
----------------------

An InputState can be created by calling its constructor, but in general this is not necessary as a `Mechanism` can
usually automatically create the InputState(s) it needs when it is created.  For example, if the Mechanism is
being created within the `pathway <Process.pathway>` of a `Process`, its InputState is created and  assigned as the
`receiver <MappingProjection.receiver>` of a `MappingProjection` from the  preceding Mechanism in the `pathway
<Process.pathway>`.  InputStates can also be specified in the **input_states** argument of a Mechanism's
constructor (see `below <InputState_Specification>`).

The `variable <InputState.variable>` of an InputState can be specified using the **variable** or **size** arguments of
its constructor.  It can also be specified using the **projections** argument, if neither **variable** nor **size** is
specified.  The **projections** argument is used to `specify Projections <State_Projections>` to the InputState. If
neither the **variable** nor **size** arguments is specified, then the value of the `Projections(s) <Projection>` or
their `sender <Projection_Base.sender>`\\s (all of which must be the same length) is used to determine the `variable
<InputState.variable>` of the InputState.

If an InputState is created using its constructor, and a Mechanism is specified in the **owner** argument,
it is automatically assigned to that Mechanism.  Note that its `value <InputState.value>` (generally determined
by the size of its `variable <InputState.variable>` -- see `below <InputState_Variable_and_Value>`) must
be compatible (in number and type of elements) with the item of its owner's `variable <Mechanism_Base.variable>` to
which it is assigned (see `below <InputState_Variable_and_Value>` and `Mechanism <Mechanism_Variable_and_InputStates>`).
If the **owner** argument is not specified, `initialization <State_Deferred_Initialization>` is deferred.

.. _InputState_Deferred_Initialization:

*Owner Assignment and Deferred Initialization*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An InputState must be owned by a `Mechanism <Mechanism>`.  When InputState is specified in the constructor for a
Mechanism (see `below <InputState_Specification>`), it is automatically assigned to that Mechanism as its owner. If
the InputState is created on its own, its `owner <InputState.owner>` can specified in the **owner**  argument of its
constructor, in which case it is assigned to that Mechanism. If its **owner** argument is not specified, its
initialization is `deferred <State_Deferred_Initialization>` until
COMMENT:
TBI: its `owner <State_Base.owner>` attribute is assigned or
COMMENT
the InputState is assigned to a Mechanism using the Mechanism's `add_states <Mechanism_Base.add_states>` method.

.. _InputState_Primary:

*Primary InputState*
~~~~~~~~~~~~~~~~~~~~~

Every Mechanism has at least one InputState, referred to as its *primary InputState*.  If InputStates are not
`explicitly specified <InputState_Specification>` for a Mechanism, a primary InputState is automatically created
and assigned to its `input_state <Mechanism_Base.input_state>` attribute (note the singular), and also to the first
entry of the Mechanism's `input_states <Mechanism_Base.input_states>` attribute (note the plural).  The `value
<InputState.value>` of the primary InputState is assigned as the first (and often only) item of the Mechanism's
`variable <Mechanism_Base.variable>` and `input_values <Mechanism_Base.input_values>` attributes.

.. _InputState_Specification:

*InputState Specification*
~~~~~~~~~~~~~~~~~~~~~~~~~~

Specifying InputStates when a Mechanism is created
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

InputStates can be specified for a `Mechanism <Mechanism>` when it is created, in the **input_states** argument of the
Mechanism's constructor (see `examples <State_Constructor_Argument_Examples>` in State), or in an *INPUT_STATES* entry
of a parameter dictionary assigned to the constructor's **params** argument.  The latter takes precedence over the
former (that is, if an *INPUT_STATES* entry is included in the parameter dictionary, any specified in the
**input_states** argument are ignored).

    .. _InputState_Replace_Default_Note:

    .. note::
       Assigning InputStates to a Mechanism in its constructor **replaces** any that are automatically generated for
       that Mechanism (i.e., those that it creates for itself by default).  If any of those are needed, they must be
       explicitly specified in the list assigned to the **input_states** argument, or the *INPUT_STATES* entry of the
       parameter dictionary in the **params** argument.  The number of InputStates specified must also be equal to
       the number of items in the Mechanism's `variable <Mechanism_Base.variable>` attribute.

.. _InputState_Variable_and_Value:

*InputState's* `variable <InputState.variable>`, `value <InputState.value>` *and Mechanism's* `variable <Mechanism_Base.variable>`
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Each InputState specified in the **input_states** argument of a Mechanism's constructor must correspond to an item of
the Mechanism's `variable <Mechanism_Base.variable>` attribute (see `Mechanism <Mechanism_Variable_and_InputStates>`),
and the `value <InputState.value>` of the InputState must be compatible with that item (that is, have the same number
and type of elements).  By default, this is also true of the InputState's `variable <InputState.variable>` attribute,
since the default `function <InputState.function>` for an InputState is a `LinearCombination`, the purpose of which
is to combine the inputs it receives and possibly modify the combined value (under the influence of any
`ModulatoryProjections <ModulatoryProjection>` it receives), but **not mutate its form**. Therefore, under most
circumstances, both the `variable <InputState.variable>` of an InputState and its `value <InputState.value>` should
match the item of its owner's `variable <Mechanism_Base.variable>` to which the InputState is assigned.

The format of an InputState's `variable <InputState.variable>` can be specified in a variety of ways.  The most
straightforward is in the **variable** argument of its constructor.  More commonly, however, it is determined by
the context in which it is being created, such as the specification for its owner Mechanism's `variable
<Mechanism_Base.variable>` or for the InputState in the Mechanism's **input_states** argument (see `below
<InputState_Forms_of_Specification>` and `Mechanism InputState specification <Mechanism_InputState_Specification>`
for details).


Adding InputStates to a Mechanism after it is created
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

InputStates can also be **added** to a Mechanism, either by creating the InputState on its own, and specifying the
Mechanism in the InputState's **owner** argument, or by using the Mechanism's `add_states <Mechanism_Base.add_states>`
method (see `examples <State_Create_State_Examples>` in State).

    .. _InputState_Add_State_Note:

    .. note::
       Adding InputStates *does not replace* any that the Mechanism generates by default;  rather they are added to the
       Mechanism, and appended to the list of InputStates in its `input_states <Mechanism_Base>` attribute. Importantly,
       the Mechanism's `variable <Mechanism_Base.variable>` attribute is extended with items that correspond to the
       `value <InputState.value>` attribute of each added InputState.  This may affect the relationship of the
       Mechanism's `variable <Mechanism_Base.variable>` to its `function <Mechanism_Base.function>`, as well as the
       number of its `OutputStates <OutputState>` (see `note <Mechanism_Add_InputStates_Note>`).

If the name of an InputState added to a Mechanism is the same as one that already exists, its name is suffixed with a
numerical index (incremented for each InputState with that name; see `Naming`), and the InputState is added to the
list (that is, it will *not* replace ones that already exist).

.. _InputState_Forms_of_Specification:

Forms of Specification
^^^^^^^^^^^^^^^^^^^^^^

InputStates can be specified in a variety of ways, that fall into three broad categories:  specifying an InputState
directly; use of a `State specification dictionary <State_Specification>`; or by specifying one or more Components that
should project to the InputState. Each of these is described below:

    .. _InputState_Direct_Specification:

    **Direct Specification of an InputState**

    * existing **InputState object** or the name of one -- If this is used to specify an InputState in the
      constructor for a Mechanism, its `value <InputState.value>` must be compatible with the corresponding item of
      the owner Mechanism's `variable <Mechanism_Base.variable>` (see `Mechanism InputState specification
      <Mechanism_InputState_Specification>` and `InputState_Compatability_and_Constraints` below).  If the InputState
      belongs to another Mechanism, then an InputState is created along with Projections(s) that `shadow the inputs
      <InputState_Shadow_Inputs>` to the specified InputState.
    ..
    * **InputState class**, **keyword** *INPUT_STATE*, or a **string** -- this creates a default InputState; if used
      to specify an InputState in the constructor for a Mechanism, the item of the owner Mechanism's `variable
      <Mechanism_Base.variable>` to which the InputState is assigned is used as the format for the InputState`s
      `variable <InputState.variable>`; otherwise, the default for the InputState is used.  If a string is specified,
      it is used as the `name <InputState.name>` of the InputState (see `example
      <State_Constructor_Argument_Examples>`).

    .. _InputState_Specification_by_Value:

    * **value** -- this creates a default InputState using the specified value as the InputState's `variable
      <InputState.variable>`; if used to specify an InputState in the constructor for a Mechanism, the format must be
      compatible with the corresponding item of the owner Mechanism's `variable <Mechanism_Base.variable>` (see
      `Mechanism InputState specification <Mechanism_InputState_Specification>`, `example
      <State_Value_Spec_Example>`, and discussion `below <InputState_Compatability_and_Constraints>`).

    .. _InputState_Specification_Dictionary:

    **InputState Specification Dictionary**

    * **InputState specification dictionary** -- this can be used to specify the attributes of an InputState, using
      any of the entries that can be included in a `State specification dictionary <State_Specification>` (see
      `examples <State_Specification_Dictionary_Examples>` in State).  If the dictionary is used to specify an
      InputState in the constructor for a Mechanism, and it includes a *VARIABLE* and/or *VALUE* or entry, the value
      must be compatible with the item of the owner Mechanism's `variable <Mechanism_Base.variable>` to which the
      InputState is assigned (see `Mechanism InputState specification <Mechanism_InputState_Specification>`).

      The *PROJECTIONS* entry can include specifications for one or more States, Mechanisms and/or Projections that
      should project to the InputState (including both `MappingProjections <MappingProjection>` and/or
      `ModulatoryProjections <ModulatoryProjection>`; however, this may be constrained by or have consequences for the
      InputState's `variable <InputState.variable>` (see `InputState_Compatability_and_Constraints`).

      In addition to the standard entries of a `State specification dictionary <State_Specification>`, the dictionary
      can also include either or both of the following entries specific to InputStates:

      * *WEIGHT*:<number>
          the value must be an integer or float, and is assigned as the value of the InputState's `weight
          <InputState.weight>` attribute (see `weight and exponent <InputState_Weights_And_Exponents>`);
          this takes precedence over any specification in the **weight** argument of the InputState's constructor.

      * *EXPONENT*:<number>
          the value must be an integer or float, and is assigned as the value of the InputState's `exponent
          <InputState.exponent>` attribute (see `weight and exponent <InputState_Weights_And_Exponents>`);
          this takes precedence over any specification in the **exponent** argument of the InputState's constructor.

    .. _InputState_Projection_Source_Specification:

    **Specification of an InputState by Components that Project to It**

    COMMENT:
    `examples
      <State_Projections_Examples>` in State)
    COMMENT

    COMMENT:
    ?? PUT IN ITS OWN SECTION ABOVE OR BELOW??
    Projections to an InputState can be specified either as attributes, in the constructor for an
    InputState (in its **projections** argument or in the *PROJECTIONS* entry of an `InputState specification dictionary
    <InputState_Specification_Dictionary>`), or used to specify the InputState itself (using one of the
    `InputState_Forms_of_Specification` described above. See `State Projections <State_Projections>` for additional
    details concerning the specification of
    Projections when creating a State.
    COMMENT

    An InputState can also be specified by specifying one or more States, Mechanisms or Projections that should project
    to it, as described below.  Specifying an InputState in this way creates both the InputState and any of the
    specified or implied Projection(s) to it (if they don't already exist). `MappingProjections <MappingProjection>`
    are assigned to the InputState's `path_afferents <InputState.path_afferents>` attribute, and `GatingProjections
    <GatingProjection>` to its `mod_afferents <InputState.mod_afferents>` attribute. Any of the following can be used
    to specify an InputState by the Components that projection to it (see `below
    <InputState_Compatability_and_Constraints>` for an explanation of the relationship between the `value` of these
    Components and the InputState's `variable <InputState.variable>`):

    * **OutputState, GatingSignal, Mechanism, or list with any of these** -- creates an InputState with Projection(s)
      to it from the specified State(s) or Mechanism(s).  For each Mechanism specified, its `primary OutputState
      <OutputState_Primary>` (or GatingSignal) is used.
    ..
    * **Projection** -- any form of `Projection specification <Projection_Specification>` can be
      used;  creates an InputState and assigns it as the Projection's `receiver <Projection_Base.receiver>`.

    .. _InputState_Tuple_Specification:

    * **InputState specification tuples** -- these are convenience formats that can be used to compactly specify an
      InputState and Projections to it any of the following ways:

        .. _InputState_State_Mechanism_Tuple:

        * **2-item tuple:** *(<State name or list of State names>, <Mechanism>)* -- 1st item must be the name of an
          `OutputState` or `ModulatorySignal`, or a list of such names, and the 2nd item must be the Mechanism to
          which they all belong.  Projections of the relevant types are created for each of the specified States
          (see `State 2-item tuple <State_2_Item_Tuple>` for additional details).

        * **2-item tuple:** *(<value, State specification, or list of State specs>, <Projection specification>)* --
          this is a contracted form of the 4-item tuple described below;

        * **4-item tuple:** *(<value, State spec, or list of State specs>, weight, exponent, Projection specification)*
          -- this allows the specification of State(s) that should project to the InputState, together with a
          specification of the InputState's `weight <InputState.weight>` and/or `exponent <InputState.exponent>`
          attributes of the InputState, and (optionally) the Projection(s) to it.  This can be used to compactly
          specify a set of States that project the InputState, while using the 4th item to determine its variable
          (e.g., using the matrix of the Projection specification) and/or attributes of the Projection(s) to it. Each
          tuple must have at least the following first three items (in the order listed), and can include the fourth:


            * **value, State specification, or list of State specifications** -- specifies either the `variable
              <InputState.variable>` of the InputState, or one or more States that should project to it.  The State
              specification(s) can be a (State name, Mechanism) tuple (see above), and/or include Mechanisms (in which
              case their `primary OutputState <OutputStatePrimary>` is used.  All of the State specifications must be
              consistent with (that is, their `value <State_Base.value>` must be compatible with the `variable
              <Projection_Base.variable>` of) the Projection specified in the fourth item if that is included;

            * **weight** -- must be an integer or a float; multiplies the `value <InputState.value>` of the InputState
              before it is combined with others by the Mechanism's `function <Mechanism.function>` (see
              ObjectiveMechanism for `examples <ObjectiveMechanism_Weights_and_Exponents_Example>`);

            * **exponent** -- must be an integer or float; exponentiates the `value <InputState.value>` of the
              InputState before it is combined with others by the ObjectiveMechanism's `function
              <ObjectiveMechanism.function>` (see ObjectiveMechanism for `examples
              <ObjectiveMechanism_Weights_and_Exponents_Example>`);

            * **Projection specification** (optional) -- `specifies a Projection <Projection_Specification>` that
              must be compatible with the State specification(s) in the 1st item; if there is more than one State
              specified, and the Projection specification is used, all of the States
              must be of the same type (i.e.,either OutputStates or GatingSignals), and the `Projection
              Specification <Projection_Specification>` cannot be an instantiated Projection (since a
              Projection cannot be assigned more than one `sender <Projection_Base.sender>`).

    .. _InputState_Shadow_Inputs:

    * **InputStates of Mechanisms to shadow** -- either of the following can be used to create InputStates that
      receive the same inputs as ("shadow") the ones specified:

      * *InputState or [InputState, ...]* -- each InputState must belong to an existing Mechanism; creates a new
        InputState for each one specified, along with Projections to it that parallel those of the one specified
        (see below).

      * *{SHADOW_INPUTS: <InputState or Mechanism or [<InputState or Mechanism>,...]>}* -- any InputStates specified
        must belong to an existing Mechanism;  creates a new InputState for each one specified, and for each of the
        InputStates belonging to any Mechanisms specified, along with Projections to them that parallel those of the
        one(s) specified (see below).

      For each InputState specified, and all of the InputStates belonging to any Mechanisms specified, a new InputState
      is created along with Projections to it that parallel those received by the corresponding InputState in the
      list.  In other words, for each InputState specified, a new one is created that receives exactly the same inputs
      from the same `senders  <Projection_Base.sender>` as the ones specified.

.. _InputState_Compatability_and_Constraints:

InputState `variable <InputState.variable>`: Compatibility and Constraints
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The `variable <InputState.variable>` of an InputState must be compatible with the item of its owner Mechanism's
`variable <Mechanism_Base.variable>` to which it is assigned (see `Mechanism_Variable_and_InputStates>`). This may
have consequences that must be taken into account when `specifying an InputState by Components that project to it
<InputState_Projection_Source_Specification>`.  These depend on the context in which the specification is made, and
possibly the value of other specifications.  These considerations and how they are handled are described below,
starting with constraints that are given the highest precedence:

  *  **InputState is** `specified in a Mechanism's constructor <Mechanism_InputState_Specification>` and the
    **default_variable** argument for the Mechanism is also specified -- the item of the variable to which the
    `InputState is assigned <Mechanism_Variable_and_InputStates>` is used to determine the InputState's `variable must
    <InputState.variable>`.  Any other specifications of the InputState relevant to its `variable <InputState.variable>`
    must be compatible with this (for example, `specifying it by value <InputState_Specification_by_Value>` or by a
    `MappingProjection` or `OutputState` that projects to it (see `above <InputState_Projection_Source_Specification>`).

    COMMENT:
    ***XXX EXAMPLE HERE
    COMMENT
  ..
  * **InputState is specified on its own**, or the **default_variable** argument of its Mechanism's constructor
    is not specified -- any direct specification of the InputState's `variable <InputState.variable>` is used to
    determine its format (e.g., `specifying it by value <InputState_Specification_by_Value>`, or a *VARIABLE* entry
    in an `InputState specification dictionary <InputState_Specification_Dictionary>`.  In this case, the value of any
    `Components used to specify the InputState <InputState_Projection_Source_Specification>` that are relevant to its
    `variable <InputState.variable>` must be compatible with it (see below).

    COMMENT:
    ***XXX EXAMPLE HERE
    COMMENT
  ..
  * If the InputState's `variable <InputState.variable>` is not constrained by any of the conditions above,
    then its format is determined by the `specification of Components that project to it
    <InputState_Projection_Source_Specification>`:

    * **More than one Component is specified with the same :ref:`value` format** -- that format is used to determine
      the format of the InputState's `variable <InputState.variable>`.

    * **More than one Component is specified with different :ref:`value` formats** -- the InputState's `variable
      <InputState.variable>` is determined by item of the default `variable <Mechanism_Base.variable>` for
      the class of its owner Mechanism.

    * **A single Component is specified** -- its :ref:`value` is used to determine the format of the InputState's
      `variable <InputState.variable>`;  if the Component is a(n):

      * **MappingProjection** -- can be specified by its class, an existing MappingProjection, or a matrix:

        * `MappingProjection` **class** -- a default value is used both the for the InputState's `variable
          <InputState.variable>` and the Projection's `value <Projection_Base.value>` (since the Projection's
          `sender <Projection_Base.sender>` is unspecified, its `initialization is deferred
          <Projection_Deferred_Initialization>`.

        * **Existing MappingProjection** -- then its `value <Projection_Base.value>` determines the
          InputState's `variable <InputState.variable>`.

        * `Matrix specification <Mapping_Matrix_Specification>` -- its receiver dimensionality determines the format
          of the InputState's `variable <InputState.variable>`. For a standard 2d "weight" matrix (i.e., one that maps
          a 1d array from its `sender <Projection_Base.sender>` to a 1d array of its `receiver
          <Projection_Base.receiver>`), the receiver dimensionality is its outer dimension (axis 1, or its number of
          columns).  However, if the `sender <Projection_Base.sender>` has more than one dimension, then the
          dimensionality of the receiver (used for the InputState's `variable <InputState.variable>`) is the
          dimensionality of the matrix minus the dimensionality of the sender's `value <OutputState.value>`
          (see `matrix dimensionality <Mapping_Matrix_Dimensionality>`).

      * **OutputState or ProcessingMechanism** -- the `value <OutputState.value>` of the OutputState (if it is a
        Mechanism, then its `primary OutputState <OutputState_Primary>`) determines the format of the InputState's
        `variable <InputState.variable>`, and a MappingProjection is created from the OutputState to the InputState
        using an `IDENTITY_MATRIX`.  If the InputState's `variable <InputState.variable>` is constrained (as in some
        of the cases above), then a `FULL_CONNECTIVITY_MATRIX` is used which maps the shape of the OutputState's `value
        <OutputState.value>` to that of the InputState's `variable <InputState.variable>`.

      * **GatingProjection, GatingSignal or GatingMechanism** -- any of these can be used to specify an InputState;
        their `value` does not need to be compatible with the InputState's `variable <InputState.variable>`, however
        it does have to be compatible with the `modulatory parameter <Function_Modulatory_Params>` of the InputState's
        `function <InputState.function>`.

.. _InputState_Structure:

Structure
---------

Every InputState is owned by a `Mechanism <Mechanism>`. It can receive one or more `MappingProjections
<MappingProjection>` from other Mechanisms, as well as from the Process or System to which its owner belongs (if it
is the `ORIGIN` Mechanism for that Process or System).  It has the following attributes, that includes ones specific
to, and that can be used to customize the InputState:

* `projections <OutputState.projections>` -- all of the `Projections <Projection>` received by the InputState.

.. _InputState_Afferent_Projections:

* `path_afferents <InputState.path_afferents>` -- `MappingProjections <MappingProjection>` that project to the
  InputState, the `value <MappingProjection.value>`\\s of which are combined by the InputState's `function
  <InputState.function>`, possibly modified by its `mod_afferents <InputState_mod_afferents>`, and assigned to the
  corresponding item of the owner Mechanism's `variable <Mechanism_Base.variable>`.
..
* `mod_afferents <InputState_mod_afferents>` -- `GatingProjections <GatingProjection>` that project to the InputState,
  the `value <GatingProjection.value>` of which can modify the InputState's `value <InputState.value>` (see the
  descriptions of Modulation under `ModulatorySignals <ModulatorySignal_Modulation>` and `GatingSignals
  <GatingSignal_Modulation>` for additional details).  If the InputState receives more than one GatingProjection,
  their values are combined before they are used to modify the `value <InputState.value>` of InputState.

.. _InputState_Variable:

* `variable <InputState.variable>` -- serves as the template for the `value <Projection_Base.value>` of the
  `Projections <Projection>` received by the InputState:  each must be compatible with (that is, match both the
  number and type of elements of) the InputState's `variable <InputState.variable>`. In general, this must also be
  compatible with the item of the owner Mechanism's `variable <Mechanism_Base.variable>` to which the InputState is
  assigned (see `above <InputState_Variable_and_Value>` and `Mechanism InputState
  specification <Mechanism_InputState_Specification>`).

.. _InputState_Function:

* `function <InputState.function>` -- combines the `value <Projection_Base.value>` of all of the
  `Projections <Projection>` received by the InputState, and assigns the result to the InputState's `value
  <InputState.value>` attribute.  The default function is `LinearCombination` that performs an elementwise (Hadamard)
  sums the values. However, the parameters of the `function <InputState.function>` -- and thus the `value
  <InputState.value>` of the InputState -- can be modified by any `GatingProjections <GatingProjection>` received by
  the InputState (listed in its `mod_afferents <InputState.mod_afferents>` attribute.  A custom function can also be
  specified, so long as it generates a result that is compatible with the item of the Mechanism's `variable
  <Mechanism_Base.variable>` to which the `InputState is assigned <Mechanism_InputStates>`.

.. _InputState_Value:

* `value <InputState.value>` -- the result returned by its `function <InputState.function>`,
  after aggregating the value of the `PathProjections <PathwayProjection>` it receives, possibly modified by any
  `GatingProjections <GatingProjection>` received by the InputState. It must be compatible with the
  item of the owner Mechanism's `variable <Mechanism_Base.variable>` to which the `InputState has been assigned
  <Mechanism_InputStates>` (see `above <InputState_Variable_and_Value>` and `Mechanism InputState specification
  <Mechanism_InputState_Specification>`).

.. _InputState_Weights_And_Exponents:

* `weight <InputState.weight>` and `exponent <InputState.exponent>` -- these can be used by the Mechanism to which the
  InputState belongs when that combines the `value <InputState.value>`\\s of its States (e.g., an ObjectiveMechanism
  uses the weights and exponents assigned to its InputStates to determine how the values it monitors are combined by
  its `function <ObjectiveMechanism>`).  The value of each must be an integer or float, and the default is 1 for both.

.. _InputState_Execution:

Execution
---------

An InputState cannot be executed directly.  It is executed when the Mechanism to which it belongs is executed.
When this occurs, the InputState executes any `Projections <Projection>` it receives, calls its `function
<InputState.function>` to combines the values received from any `MappingProjections <MappingProjection>` it receives
(listed in its its `path_afferents  <InputState.path_afferents>` attribute) and modulate them in response to any
`GatingProjections <GatingProjection>` (listed in its `mod_afferents <InputState.mod_afferents>` attribute),
and then assigns the result to the InputState's `value <InputState.value>` attribute. This, in turn, is assigned to
the item of the Mechanism's `variable <Mechanism_Base.variable>` and `input_values <Mechanism_Base.input_values>`
attributes  corresponding to that InputState (see `Mechanism Variable and InputStates
<Mechanism_Variable_and_InputStates>` for additional details).

.. _InputState_Class_Reference:

Class Reference
---------------

"""
import numbers
import warnings

import collections
import numpy as np
import typecheck as tc

from psyneulink.core.components.component import DefaultsFlexibility
from psyneulink.core.components.functions.function import Function
from psyneulink.core.components.functions.transferfunctions import Linear
from psyneulink.core.components.functions.combinationfunctions import CombinationFunction, LinearCombination, Reduce
from psyneulink.core.components.functions.statefulfunctions.memoryfunctions import Buffer
from psyneulink.core.components.states.outputstate import OutputState
from psyneulink.core.components.states.state import StateError, State_Base, _instantiate_state_list, state_type_keywords
from psyneulink.core.globals.context import ContextFlags, handle_external_context
from psyneulink.core.globals.keywords import \
    COMBINE, CONTROL_SIGNAL, EXPONENT, FUNCTION, GATING_SIGNAL, INPUT_STATE, INPUT_STATES, INPUT_STATE_PARAMS, \
    LEARNING_SIGNAL, MAPPING_PROJECTION, MATRIX, MECHANISM, NAME, OPERATION, OUTPUT_STATE, OUTPUT_STATES, OWNER,\
    PARAMS, PROCESS_INPUT_STATE, PRODUCT, PROJECTIONS, PROJECTION_TYPE, REFERENCE_VALUE, \
    SENDER, SIZE, STATE_TYPE, SUM, SYSTEM_INPUT_STATE, VALUE, VARIABLE, WEIGHT
from psyneulink.core.globals.parameters import Parameter
from psyneulink.core.globals.preferences.basepreferenceset import is_pref_set
from psyneulink.core.globals.preferences.preferenceset import PreferenceLevel
from psyneulink.core.globals.utilities import append_type_to_name, is_numeric, iscompatible, kwCompatibilityLength

__all__ = [
    'InputState', 'InputStateError', 'state_type_keywords', 'SHADOW_INPUTS',
]

state_type_keywords = state_type_keywords.update({INPUT_STATE})

# InputStatePreferenceSet = BasePreferenceSet(log_pref=logPrefTypeDefault,
#                                                          reportOutput_pref=reportOutputPrefTypeDefault,
#                                                          verbose_pref=verbosePrefTypeDefault,
#                                                          param_validation_pref=paramValidationTypeDefault,
#                                                          level=PreferenceLevel.TYPE,
#                                                          name='InputStateClassPreferenceSet')

WEIGHT_INDEX = 1
EXPONENT_INDEX = 2

DEFER_VARIABLE_SPEC_TO_MECH_MSG = "InputState variable not yet defined, defer to Mechanism"
SHADOW_INPUTS = 'shadow_inputs'
SHADOW_INPUT_NAME = 'Shadowed input of '

class InputStateError(Exception):
    def __init__(self, error_value):
        self.error_value = error_value

    def __str__(self):
        return repr(self.error_value)


class InputState(State_Base):
    """
    InputState(                                    \
        owner=None,                                \
        variable=None,                             \
        size=None,                                 \
        function=LinearCombination(operation=SUM), \
        combine=None,                              \
        projections=None,                          \
        weight=None,                               \
        exponent=None,                             \
        internal_only=False,                       \
        params=None,                               \
        name=None,                                 \
        prefs=None)

    Subclass of `State <State>` that calculates and represents the input to a `Mechanism <Mechanism>` from one or more
    `PathwayProjections <PathwayProjection>`.

    Arguments
    ---------

    owner : Mechanism
        the Mechanism to which the InputState belongs;  it must be specified or determinable from the context in which
        the InputState is created.

    reference_value : number, list or np.ndarray
        the value of the item of the owner Mechanism's `variable <Mechanism_Base.variable>` attribute to which
        the InputState is assigned; used as the template for the InputState's `value <InputState.value>` attribute.

    variable : number, list or np.ndarray
        specifies the template for the InputState's `variable <InputState.variable>` attribute.

    size : int, list or np.ndarray of ints
        specifies variable as array(s) of zeros if **variable** is not passed as an argument;
        if **variable** is specified, it takes precedence over the specification of **size**.

    function : Function or method : default LinearCombination(operation=SUM)
        specifies the function applied to the variable. The default value combines the `values
        <Projection_Base.value>` of the `Projections <Projection>` received by the InputState.  Any function
        can be assigned, however:  a) it must produce a result that has the same format (number and type of elements)
        as the item of its owner Mechanism's `variable <Mechanism_Base.variable>` to which the InputState has been
        assigned;  b) if it is not a CombinationFunction, it may produce unpredictable results if the InputState
        receives more than one Projection (see `function <InputState.function>`.

    combine : SUM or PRODUCT : default None
        specifies the **operation** argument used by the default `LinearCombination` function, which determines how the
        `value <Projection.value>` of the InputState's `projections <InputState.projections>` are combined.  This is a
        convenience argument, that allows the **operation** to be specified without having to specify the
        LinearCombination function; it assumes that LinearCombination (the default) is used as the InputState's function
        -- if it conflicts with a specification of **function** an error is generated.

    projections : list of Projection specifications
        specifies the `MappingProjection(s) <MappingProjection>` and/or `GatingProjection(s) <GatingProjection>` to be
        received by the InputState, and that are listed in its `path_afferents <InputState.path_afferents>` and
        `mod_afferents <InputState.mod_afferents>` attributes, respectively (see
        `InputState_Compatability_and_Constraints` for additional details).  If **projections** but neither
        **variable** nor **size** are specified, then the `value <Projection.value>` of the Projection(s) or their
        `senders <Projection_Base.sender>` specified in **projections** argument are used to determine the InputState's
        `variable <InputState.variable>`.

    weight : number : default 1
        specifies the value of the `weight <InputState.weight>` attribute of the InputState.

    exponent : number : default 1
        specifies the value of the `exponent <InputState.exponent>` attribute of the InputState.

    internal_only : bool : False
        specifies whether external input is required by the InputState's `owner <InputState.owner>` if its `role
        <Mechanism_Role_In_Processes_And_Systems>` is *EXTERNAL_INPUT*  (see `internal_only <InputState.internal_only>`
        for details).

    params : Dict[param keyword: param value] : default None
        a `parameter dictionary <ParameterState_Specification>` that can be used to specify the parameters for
        the InputState or its function, and/or a custom function and its parameters. Values specified for parameters in
        the dictionary override any assigned to those parameters in arguments of the constructor.

    name : str : default see `name <InputState.name>`
        specifies the name of the InputState; see InputState `name <InputState.name>` for details.

    prefs : PreferenceSet or specification dict : default State.classPreferences
        specifies the `PreferenceSet` for the InputState; see `prefs <InputState.prefs>` for details.


    Attributes
    ----------

    owner : Mechanism
        the Mechanism to which the InputState belongs.

    path_afferents : List[MappingProjection]
        `MappingProjections <MappingProjection>` that project to the InputState
        (i.e., for which it is a `receiver <Projection_Base.receiver>`).

    mod_afferents : List[GatingProjection]
        `GatingProjections <GatingProjection>` that project to the InputState.

    projections : List[Projection]
        all of the `Projections <Projection>` received by the InputState.

    variable : value, list or np.ndarray
        the template for the `value <Projection_Base.value>` of each Projection that the InputState receives,
        each of which must match the format (number and types of elements) of the InputState's
        `variable <InputState.variable>`.  If neither the **variable** or **size** argument is specified, and
        **projections** is specified, then `variable <InputState.variable>` is assigned the `value
        <Projection.value>` of the Projection(s) or its `sender <Projection_Base.sender>`.

    function : Function
        If it is a `CombinationFunction`, it combines the `values <Projection_Base.value>` of the `PathwayProjections
        <PathwayProjection>` (e.g., `MappingProjections <MappingProjection>`) received by the InputState  (listed in
        its `path_afferents <InputState.path_afferents>` attribute), under the possible influence of
        `GatingProjections <GatingProjection>` received by the InputState (listed in its `mod_afferents
        <InputState.mod_afferents>` attribute). The result is assigned to the InputState's `value
        <InputState.value>` attribute. For example, the default (`LinearCombination` with *SUM* as it **operation**)
        performs an element-wise (Hadamard) sum of its Projection `values <Projection_Base.value>`, and assigns to
        `value <InputState.value>` an array that is of the same length as each of the Projection `values
        <Projection_Base.value>`.  If the InputState receives only one Projection, then any other function can be
        applied and it will generate a value that is the same length as the Projection's `value <Projection.value>`.
        However, if the InputState receives more than one Projection and uses a function other than a
        CombinationFunction, a warning is generated and only the `value <Projection.value>` of the first Projection
        list in `path_afferents <InputState.path_afferents>` is used by the function, which may generate unexpected
        results when executing the Mechanism or Composition to which it belongs.

    value : value or ndarray
        the output of the InputState's `function <InputState.function>`, that is assigned to an item of the owner
        Mechanism's `variable <Mechanism_Base.variable>` attribute.


    label : string or number
        the string label that represents the current `value <InputState.value>` of the InputState, according to the
        owner mechanism's `input_labels_dict <Mechanism.input_labels_dict>`. If the current `value <InputState.value>`
        of the InputState does not have a corresponding label, then the numeric `value <InputState.value>` is returned.

    weight : number
        see `weight and exponent <InputState_Weights_And_Exponents>` for description.

    exponent : number
        see `weight and exponent <InputState_Weights_And_Exponents>` for description.

    internal_only : bool
        determines whether input is required for this InputState from `Run` or another `Composition` when the
        InputState's `owner <InputState.owner>` is executed, and its `role <Mechanism_Role_In_Processes_And_Systems>`
        is designated as *EXTERNAL_INPUT*;  if `True`, external input is *not* required or allowed;  otherwise,
        external input is required.

    name : str
        the name of the InputState; if it is not specified in the **name** argument of the constructor, a default is
        assigned by the InputStateRegistry of the Mechanism to which the InputState belongs.  Note that some Mechanisms
        automatically create one or more non-default InputStates, that have pre-specified names.  However, if any
        InputStates are specified in the **input_states** argument of the Mechanism's constructor, those replace those
        InputStates (see `note <Mechanism_Default_State_Suppression_Note>`), and `standard naming conventions <Naming>`
        apply to the InputStates specified, as well as any that are added to the Mechanism once it is created.

        .. note::
            Unlike other PsyNeuLink components, State names are "scoped" within a Mechanism, meaning that States with
            the same name are permitted in different Mechanisms.  However, they are *not* permitted in the same
            Mechanism: States within a Mechanism with the same base name are appended an index in the order of their
            creation.

    prefs : PreferenceSet or specification dict
        the `PreferenceSet` for the InputState; if it is not specified in the **prefs** argument of the
        constructor, a default is assigned using `classPreferences` defined in __init__.py (see :doc:`PreferenceSet
        <LINK>` for details).


    """

    #region CLASS ATTRIBUTES

    componentType = INPUT_STATE
    paramsType = INPUT_STATE_PARAMS

    stateAttributes = State_Base.stateAttributes | {WEIGHT, EXPONENT}

    connectsWith = [OUTPUT_STATE,
                    PROCESS_INPUT_STATE,
                    SYSTEM_INPUT_STATE,
                    LEARNING_SIGNAL,
                    GATING_SIGNAL,
                    CONTROL_SIGNAL
                    ]
    connectsWithAttribute = [OUTPUT_STATES]
    projectionSocket = SENDER
    modulators = [GATING_SIGNAL, CONTROL_SIGNAL]
    canReceive = modulators + [MAPPING_PROJECTION]


    classPreferenceLevel = PreferenceLevel.TYPE
    # Any preferences specified below will override those specified in TYPE_DEFAULT_PREFERENCES
    # Note: only need to specify setting;  level will be assigned to TYPE automatically
    # classPreferences = {
    #     PREFERENCE_SET_NAME: 'InputStateCustomClassPreferences',
    #     PREFERENCE_KEYWORD<pref>: <setting>...}

    # Note: the following enforce encoding as 1D np.ndarrays (one variable/value array per state)
    variableEncodingDim = 1
    valueEncodingDim = 1

    class Parameters(State_Base.Parameters):
        """
            Attributes
            ----------

                combine
                    see `combine <InputState.combine>`

                    :default value: None
                    :type:

                exponent
                    see `exponent <InputState.exponent>`

                    :default value: None
                    :type:

                function
                    see `function <InputState.function>`

                    :default value: `LinearCombination`
                    :type: `Function`

                internal_only
                    see `internal_only <InputState.internal_only>`

                    :default value: False
                    :type: bool

                shadow_inputs
                    specifies whether InputState shadows inputs of another InputState;
                    if not None, must be assigned another InputState

                    :default value: None
                    :type: InputState
                    :read only: True

                weight
                    see `weight <InputState.weight>`

                    :default value: None
                    :type:

        """
        function = Parameter(LinearCombination(operation=SUM), stateful=False, loggable=False)
        weight = Parameter(None, modulable=True)
        exponent = Parameter(None, modulable=True)
        combine = None
        internal_only = Parameter(False, stateful=False, loggable=False, pnl_internal=True)
        shadow_inputs = Parameter(None, stateful=False, loggable=False, read_only=True, pnl_internal=True)

    paramClassDefaults = State_Base.paramClassDefaults.copy()
    paramClassDefaults.update({PROJECTION_TYPE: MAPPING_PROJECTION,
                               MECHANISM: None,     # These are used to specifiy InputStates by projections to them
                               OUTPUT_STATES: None  # from the OutputStates of a particular Mechanism (see docs)
                               })
    #endregion

    @handle_external_context()
    @tc.typecheck
    def __init__(self,
                 owner=None,
                 reference_value=None,
                 variable=None,
                 size=None,
                 function=None,
                 projections=None,
                 combine:tc.optional(tc.enum(SUM,PRODUCT))=None,
                 weight=None,
                 exponent=None,
                 internal_only:bool=False,
                 params=None,
                 name=None,
                 prefs:is_pref_set=None,
                 context=None,
                 **kwargs):

        if variable is None and size is None and projections is not None:
            variable = self._assign_variable_from_projection(variable, size, projections)

        # If combine argument is specified, save it along with any user-specified function for _validate_params()
        # (but don't pass to _assign_args_to_param_dicts, as it is an option not a legitimate InputState parameter)
        if combine:
            self.combine_function_args = (combine, function)

        # Assign args to params and functionParams dicts
        params = self._assign_args_to_param_dicts(function=function,
                                                  weight=weight,
                                                  exponent=exponent,
                                                  internal_only=internal_only,
                                                  shadow_inputs=None,
                                                  params=params)

        # If owner or reference_value has not been assigned, defer init to State._instantiate_projection()
        # if owner is None or (variable is None and reference_value is None and projections is None):
        if owner is None:
            # Temporarily name InputState
            self._assign_deferred_init_name(name, context)
            # Store args for deferred initialization
            self.init_args = locals().copy()
            self.init_args['context'] = context
            self.init_args['name'] = name
            self.init_args['projections'] = projections

            # Flag for deferred initialization
            self.initialization_status = ContextFlags.DEFERRED_INIT
            return

        self.reference_value = reference_value

        # Validate sender (as variable) and params, and assign to variable and paramInstanceDefaults
        # Note: pass name of owner (to override assignment of componentName in super.__init__)
        super(InputState, self).__init__(owner,
                                         variable=variable,
                                         size=size,
                                         projections=projections,
                                         function=function,
                                         params=params,
                                         name=name,
                                         prefs=prefs,
                                         context=context,
                                         )

        if self.name is self.componentName or self.componentName + '-' in self.name:
            self._assign_default_state_name(context=context)

    def _assign_variable_from_projection(self, variable, size, projections):
        """Assign variable to value of Projection in projections
        """
        from psyneulink.core.components.projections.projection import \
            Projection, _parse_connection_specs

        if not isinstance(projections, list):
            projections = [projections]

        # Use only first specification in the list returned, and assume any others are the same size
        #     (which they must be); leave validation of this to _instantiate_projections_to_state
        proj_spec = _parse_connection_specs(InputState, self, projections)[0]

        if isinstance(proj_spec.projection, Projection):
            variable = proj_spec.projection.defaults.value
        elif isinstance(proj_spec.state, OutputState):
            variable = proj_spec.state.defaults.value
        else:
            raise InputStateError("Unrecognized specification for \'{}\' arg of {}".format(PROJECTIONS, self.name))

        return variable

    def _validate_params(self, request_set, target_set=None, context=None):
        """Validate weights and exponents

        This needs to be done here, since paramClassDefault declarations assign None as default
            (so that they can be ignored if not specified here or in the function)
        """

        super()._validate_params(request_set=request_set, target_set=target_set, context=context)

        # Make sure **combine** and **function** args specified in constructor don't conflict
        if hasattr(self, 'combine_function_args'):
            combine, function = self.combine_function_args
            if function:
                owner_name = ""
                if self.owner:
                    owner_name = " for InputState of {}".format(self.owner.name)
                if isinstance(function, LinearCombination):
                    # specification of combine conflicts with operation specified for LinearCombination in function arg
                    if function.operation != combine:
                        raise InputStateError("Specification of {} argument ({}) conflicts with "
                                              "specification of {} ({}) for LinearCombination in {} "
                                              "argument{}".
                                              format(repr(COMBINE), combine.upper(),
                                                     repr(OPERATION),function.operation.upper(),
                                                     repr(FUNCTION), owner_name))
                    else:
                        # LinearFunction has been specified with same operation as specified for combine,
                        # so delete combine_function_args attribute so it is not seen in _instantiate_function
                        # in order to leave function intact (as it may have other parameters specified by user)
                        del self.combine_function_args
                # combine assumes LinearCombination, but Function other than LinearCombination specified for function
                elif isinstance(function, Function):
                    raise InputStateError("Specification of {} argument ({}) conflicts with "
                                          "Function specified in {} argument ({}){}".
                                          format(repr(COMBINE), combine.upper(),
                                                 repr(FUNCTION), function.name, owner_name))
                # combine assumes LinearCombination, but class other than LinearCombination specified for function
                elif isinstance(function, type):
                    if not issubclass(function, LinearCombination):
                        raise InputStateError("Specification of {} argument ({}) conflicts with "
                                              "Function specified in {} argument ({}){}".
                                              format(repr(COMBINE), combine.upper(),
                                                     repr(FUNCTION), function.__name__, owner_name))
                else:
                    raise InputStateError("PROGRAM ERROR: unrecognized specification for function argument ({}){} ".
                                          format(function, owner_name))

        if WEIGHT in target_set and target_set[WEIGHT] is not None:
            if not isinstance(target_set[WEIGHT], (int, float)):
                raise InputStateError("{} parameter of {} for {} ({}) must be an int or float".
                                      format(WEIGHT, self.name, self.owner.name, target_set[WEIGHT]))

        if EXPONENT in target_set and target_set[EXPONENT] is not None:
            if not isinstance(target_set[EXPONENT], (int, float)):
                raise InputStateError("{} parameter of {} for {} ({}) must be an int or float".
                                      format(EXPONENT, self.name, self.owner.name, target_set[EXPONENT]))

    def _validate_against_reference_value(self, reference_value):
        """Validate that State.value is compatible with reference_value

        reference_value is the item of the owner Mechanism's variable to which the InputState is assigned
        """
        match_len_option = {kwCompatibilityLength:False}
        if reference_value is not None and not iscompatible(reference_value, self.defaults.value, **match_len_option):
            name = self.name or ""
            raise InputStateError("Value specified for {} {} of {} ({}) is not compatible with its expected format ({})"
                                  .format(name, self.componentName, self.owner.name, self.defaults.value, reference_value))

    def _instantiate_function(self, function, function_params=None, context=None):
        """If combine option was specified in constructor, assign as operation argument of LinearCombination function"""
        if hasattr(self, 'combine_function_args'):
            function = LinearCombination(operation=self.combine_function_args[0])
            del self.combine_function_args
        super()._instantiate_function(function=function, context=context)
        self._use_1d_variable = False
        if not isinstance(self.function, CombinationFunction):
            self._use_1d_variable = True
            self.function._default_variable_flexibility = DefaultsFlexibility.RIGID
        else:
            self.function._default_variable_flexibility = DefaultsFlexibility.FLEXIBLE

    def _instantiate_projections(self, projections, context=None):
        """Instantiate Projections specified in PROJECTIONS entry of params arg of State's constructor

        Call _instantiate_projections_to_state to assign:
            PathwayProjections to .path_afferents
            ModulatoryProjections to .mod_afferents
        """
        self._instantiate_projections_to_state(projections=projections, context=context)

    def _check_for_duplicate_projections(self, projection):
        """Check if projection is redundant with one in path_afferents of InputState

        Check for any instantiated projection in path_afferents with the same sender as projection
        or one in deferred_init status with sender specification that is the same type as projection.

        Returns redundant Projection if found, otherwise False.
        """

        # FIX: 7/22/19 - CHECK IF SENDER IS SPECIFIED AS MECHANISM AND, IF SO, CHECK ITS PRIMARY_OUTPUT_STATE
        duplicate = next(iter([proj for proj in self.path_afferents
                               if ((proj.sender == projection.sender and proj != projection)
                                   or (proj.initialization_status == ContextFlags.DEFERRED_INIT
                                       and proj.init_args[SENDER] == type(projection.sender)))]), None)
        if duplicate and self.verbosePref or self.owner.verbosePref:
            from psyneulink.core.components.projections.projection import Projection
            warnings.warn(f'{Projection.__name__} from {projection.sender.name}  {projection.sender.__class__.__name__}'
                          f' of {projection.sender.owner.name} to {self.name} {self.__class__.__name__} of '
                          f'{self.owner.name} already exists; will ignore additional one specified ({projection.name}).')
        return duplicate

    def _parse_function_variable(self, variable, context=None):
        variable = super()._parse_function_variable(variable, context)
        try:
            if self._use_1d_variable and variable.ndim > 1:
                return np.array(variable[0])
        except AttributeError:
            pass
        return variable

    def _get_fallback_variable(self, context=None):
        """
            Call self.function with self._path_proj_values

            If variable is None there are no active PathwayProjections in the Composition being run,
            return None so that it is ignored in execute method (i.e., not combined with base_value)
        """
        # Check for Projections that are active in the Composition being run
        path_proj_values = [
            proj.parameters.value._get(context)
            for proj in self.path_afferents
            if self.afferents_info[proj].is_active_in_composition(context.composition)
        ]

        if len(path_proj_values) > 0:
            return np.asarray(path_proj_values)
        else:
            return None

    def _get_primary_state(self, mechanism):
        return mechanism.input_state

    @tc.typecheck
    def _parse_state_specific_specs(self, owner, state_dict, state_specific_spec):
        """Get weights, exponents and/or any connections specified in an InputState specification tuple

        Tuple specification can be:
            (state_spec, connections)
            (state_spec, weights, exponents, connections)

        See State._parse_state_specific_spec for additional info.
.
        Returns:
             - state_spec:  1st item of tuple if it is a numeric value;  otherwise None
             - params dict with WEIGHT, EXPONENT and/or PROJECTIONS entries if any of these was specified.

        """
        # FIX: ADD FACILITY TO SPECIFY WEIGHTS AND/OR EXPONENTS FOR INDIVIDUAL OutputState SPECS
        #      CHANGE EXPECTATION OF *PROJECTIONS* ENTRY TO BE A SET OF TUPLES WITH THE WEIGHT AND EXPONENT FOR IT
        #      THESE CAN BE USED BY THE InputState's LinearCombination Function
        #          (AKIN TO HOW THE MECHANISM'S FUNCTION COMBINES InputState VALUES)
        #      THIS WOULD ALLOW AN ADDITIONAL HIERARCHICAL LEVEL FOR NESTING ALGEBRAIC COMBINATION OF INPUT VALUES
        #      TO A MECHANISM
        from psyneulink.core.components.projections.projection import Projection, _parse_connection_specs

        params_dict = {}
        state_spec = state_specific_spec

        if isinstance(state_specific_spec, dict):
            # FIX: 10/3/17 - CHECK HERE THAT, IF MECHANISM ENTRY IS USED, A VARIABLE, WEIGHT AND/OR EXPONENT ENTRY
            # FIX:                       IS APPLIED TO ALL THE OutputStates SPECIFIED IN OUTPUT_STATES
            # FIX:                       UNLESS THEY THEMSELVES USE A State specification dict WITH ANY OF THOSE ENTRIES
            # FIX:           USE ObjectiveMechanism EXAMPLES
            # if MECHANISM in state_specific_spec:
            #     if OUTPUT_STATES in state_specific_spec
            if SIZE in state_specific_spec:
                if (VARIABLE in state_specific_spec or
                        any(key in state_dict and state_dict[key] is not None for key in {VARIABLE, SIZE})):
                    raise InputStateError("PROGRAM ERROR: SIZE specification found in state_specific_spec dict "
                                          "for {} specification of {} when SIZE or VARIABLE is already present in its "
                                          "state_specific_spec dict or state_dict".format(self.__name__, owner.name))
                state_dict.update({VARIABLE:np.zeros(state_specific_spec[SIZE])})
                del state_specific_spec[SIZE]
                return state_dict, state_specific_spec
            return None, state_specific_spec

        elif isinstance(state_specific_spec, tuple):

            # GET STATE_SPEC AND ASSIGN PROJECTIONS_SPEC **********************************************************

            tuple_spec = state_specific_spec

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
                                         format(InputState.__name__, owner.name, state_spec,
                                                REFERENCE_VALUE, reference_value))
                    projections_spec = tuple_spec[1]

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
                    # Parse the value of all of the Projections to get/validate variable for InputState
                    variable = []
                    for projection_spec in params_dict[PROJECTIONS]:
                        # FIX: 10/3/17 - PUTTING THIS HERE IS A HACK...
                        # FIX:           MOVE TO _parse_state_spec UNDER PROCESSING OF ProjectionTuple SPEC
                        # FIX:           USING _get_state_for_socket
                        # from psyneulink.core.components.projections.projection import _parse_projection_spec

                        # Try to get matrix for projection
                        try:
                            sender_dim = np.array(projection_spec.state.value).ndim
                        except AttributeError as e:
                            if (isinstance(projection_spec.state, type) or
                                     projection_spec.state.initialization_status == ContextFlags.DEFERRED_INIT):
                                continue
                            else:
                                raise StateError("PROGRAM ERROR: indeterminate value for {} "
                                                 "specified to project to {} of {}".
                                                 format(projection_spec.state.name, self.__name__, owner.name))

                        projection = projection_spec.projection
                        if isinstance(projection, dict):
                            # Don't try to get MATRIX from projection without checking,
                            #    since projection is a defaultDict,
                            #    which will add a matrix entry and assign it to None if it is not there
                            if MATRIX in projection:
                                matrix = projection[MATRIX]
                            else:
                                matrix = None
                        elif isinstance(projection, Projection):
                            if projection.initialization_status == ContextFlags.DEFERRED_INIT:
                                continue
                            # possible needs to be projection.defaults.matrix?
                            matrix = projection.matrix
                        else:
                            raise InputStateError("Unrecognized Projection specification for {} of {} ({})".
                                                  format(self.name, owner.name, projection_spec))

                        # Determine length of value of projection
                        if matrix is None:
                            # If a reference_value has been specified, it presumably represents the item of the
                            #    owner Mechanism's default_variable to which the InputState corresponds,
                            #    so use that to constrain the InputState's variable
                            if state_dict[REFERENCE_VALUE] is not None:
                                variable.append(state_dict[REFERENCE_VALUE])
                                continue
                            # If matrix has not been specified, no worries;
                            #    variable_item can be determined by value of sender
                            sender_shape = np.array(projection_spec.state.value).shape
                            variable_item = np.zeros(sender_shape)
                            # If variable_item HASN'T been specified, or it is same shape as any previous ones,
                            #     use sender's value
                            if ((VARIABLE not in state_dict or state_dict[VARIABLE] is None) and
                                    (not variable or variable_item.shape == variable[0].shape)):
                                # state_dict[VARIABLE] = variable
                                variable.append(variable_item)
                            # If variable HAS been assigned, make sure value is the same for this sender
                            elif np.array(state_dict[VARIABLE]).shape != variable_item.shape:
                                # If values for senders differ, assign None so that State's default is used
                                variable = None
                                # No need to check any more Projections
                                break

                        # Remove dimensionality of sender OutputState, and assume that is what receiver will receive
                        else:
                            proj_val_shape = matrix.shape[sender_dim :]
                            # state_dict[VARIABLE] = np.zeros(proj_val_shape)
                            variable.append(np.zeros(proj_val_shape))
                    # Sender's value has not been defined or senders have values of different lengths,
                    if not variable:
                        # If reference_value was provided, use that as the InputState's variable
                        #    (i.e., assume its function won't transform it)
                        if REFERENCE_VALUE in state_dict and state_dict[REFERENCE_VALUE] is not None:
                            state_dict[VARIABLE] = state_dict[REFERENCE_VALUE]
                        # Nothing to use as variable, so raise exception and allow it to be handled "above"
                        else:
                            raise AttributeError(DEFER_VARIABLE_SPEC_TO_MECH_MSG)
                    else:
                        state_dict[VARIABLE] = variable

                except InputStateError:
                    raise InputStateError("Tuple specification in {} specification dictionary "
                                          "for {} ({}) is not a recognized specification for one or more "
                                          "{}s, {}s, or {}s that project to it".
                                          format(InputState.__name__,
                                                 owner.name,
                                                 projections_spec,
                                                 'Mechanism',
                                                 OutputState.__name__,
                                                 Projection.__name__))

            # GET WEIGHT AND EXPONENT IF SPECIFIED ***************************************************************

            if len(tuple_spec) == 2:
                pass

            # Tuple is (spec, weights, exponents<, afferent_source_spec>),
            #    for specification of weights and exponents,  + connection(s) (afferent projection(s)) to InputState
            elif len(tuple_spec) in {3, 4}:

                weight = tuple_spec[WEIGHT_INDEX]
                exponent = tuple_spec[EXPONENT_INDEX]

                if weight is not None and not isinstance(weight, numbers.Number):
                    raise InputStateError("Specification of the weight ({}) in tuple of {} specification dictionary "
                                          "for {} must be a number".format(weight, InputState.__name__, owner.name))
                params_dict[WEIGHT] = weight

                if exponent is not None and not isinstance(exponent, numbers.Number):
                    raise InputStateError("Specification of the exponent ({}) in tuple of {} specification dictionary "
                                          "for {} must be a number".format(exponent, InputState.__name__, owner.name))
                params_dict[EXPONENT] = exponent

            else:
                raise StateError("Tuple provided as state_spec for {} of {} ({}) must have either 2, 3 or 4 items".
                                 format(InputState.__name__, owner.name, tuple_spec))

        elif state_specific_spec is not None:
            raise InputStateError("PROGRAM ERROR: Expected tuple or dict for {}-specific params but, got: {}".
                                  format(self.__class__.__name__, state_specific_spec))

        return state_spec, params_dict

    def _parse_self_state_type_spec(self, owner, input_state, context=None):
        """Return InputState specification dictionary with projections that shadow inputs to input_state

        Called by _parse_state_spec if InputState specified for a Mechanism belongs to a different Mechanism
        """

        if not isinstance(input_state, InputState):
            raise InputStateError("PROGRAM ERROR: "
                                  "InputState._parse_self_state_type called with non-InputState specification ({})".
                                  format(input_state))

        sender_output_states = [p.sender for p in input_state.path_afferents]
        state_spec = {NAME: SHADOW_INPUT_NAME + input_state.owner.name,
                      VARIABLE: np.zeros_like(input_state.variable),
                      STATE_TYPE: InputState,
                      PROJECTIONS: sender_output_states,
                      PARAMS: {SHADOW_INPUTS: input_state},
                      OWNER: owner}
        return state_spec

    @staticmethod
    def _state_spec_allows_override_variable(spec):
        """
        Returns
        -------
            True - if **spec** outlines a spec for creating an InputState whose variable can be
                overridden by a default_variable or size argument
            False - otherwise

            ex: specifying an InputState with a Mechanism allows overriding
        """
        from psyneulink.core.components.mechanisms.mechanism import Mechanism

        if isinstance(spec, Mechanism):
            return True
        if isinstance(spec, collections.abc.Iterable):
            # generally 2-4 tuple spec, but allows list spec
            for item in spec:
                if isinstance(item, Mechanism):
                    return True
                # handles tuple spec where first item of tuple is itself a (name, Mechanism) tuple
                elif (
                    isinstance(item, collections.abc.Iterable)
                    and len(item) >= 2
                    and isinstance(item[1], Mechanism)
                ):
                    return True

        return False

    @property
    def pathway_projections(self):
        return self.path_afferents

    @pathway_projections.setter
    def pathway_projections(self, assignment):
        self.path_afferents = assignment

    @property
    def socket_width(self):
        return self.defaults.variable.shape[-1]

    @property
    def socket_template(self):
        return np.zeros(self.socket_width)

    @property
    def label(self):
        return self.get_label()

    def get_label(self, context=None):
        try:
            label_dictionary = self.owner.input_labels_dict
        except AttributeError:
            label_dictionary = {}
        return self._get_value_label(label_dictionary, self.owner.input_states, context=context)

    @property
    def position_in_mechanism(self):
        if hasattr(self, "owner"):
            if self.owner is not None:
                return self.owner.get_input_state_position(self)
            else:
                return None
        return None

    @staticmethod
    def _get_state_function_value(owner, function, variable):
        """Put InputState's variable in a list if its function is LinearCombination and variable is >=2d

        InputState variable must be embedded in a list so that LinearCombination (its default function)
        returns a variable that is >=2d intact (rather than as arrays to be combined);
        this is normally done in state._update() (and in State._instantiate-function), but that
        can't be called by _parse_state_spec since the InputState itself may not yet have been instantiated.

        """
        import inspect

        if (
                (
                    (inspect.isclass(function) and issubclass(function, LinearCombination))
                    or isinstance(function, LinearCombination)
                )
                and isinstance(variable, np.matrix)
        ):
            variable = [variable]

        # if function is None, use State's default function
        function = function or InputState.defaults.function

        return State_Base._get_state_function_value(owner=owner, function=function, variable=variable)


def _instantiate_input_states(owner, input_states=None, reference_value=None, context=None):
    """Call State._instantiate_state_list() to instantiate ContentAddressableList of InputState(s)

    Create ContentAddressableList of InputState(s) specified in paramsCurrent[INPUT_STATES]

    If input_states is not specified:
        - use owner.input_states as list of InputState specifications
        - if owner.input_states is empty, user owner.defaults.variable to create a default InputState

    When completed:
        - self.input_states contains a ContentAddressableList of one or more input_states
        - self.input_state contains the `primary InputState <InputState_Primary>`:  first or only one in input_states
        - paramsCurrent[INPUT_STATES] contains the same ContentAddressableList (of one or more input_states)
        - each InputState corresponds to an item in the variable of the owner's function
        - the value of all of the input_states is stored in a list in input_value
        - if there is only one InputState, it is assigned the full value

    Note: State._instantiate_state_list()
              parses self.defaults.variable (2D np.array, passed in reference_value)
              into individual 1D arrays, one for each input state

    (See State._instantiate_state_list() for additional details)

    Returns list of instantiated InputStates
    """

    # This allows method to be called by Mechanism.add_input_states() with set of user-specified input_states,
    #    while calls from init_methods continue to use owner.input_states (i.e., InputState specifications
    #    assigned in the **input_states** argument of the Mechanism's constructor)
    input_states = input_states or owner.input_states

    # Parse any SHADOW_INPUTS specs into actual InputStates to be shadowed
    if input_states is not None:
        input_states = _parse_shadow_inputs(owner, input_states)

    state_list = _instantiate_state_list(owner=owner,
                                         state_list=input_states,
                                         state_types=InputState,
                                         state_param_identifier=INPUT_STATE,
                                         reference_value=reference_value if reference_value is not None
                                                                         else owner.defaults.variable,
                                         reference_value_name=VALUE,
                                         context=context)

    # Call from Mechanism.add_states, so add to rather than assign input_states (i.e., don't replace)
    if context.source & (ContextFlags.METHOD | ContextFlags.COMMAND_LINE):
        owner.input_states.extend(state_list)
    else:
        owner._input_states = state_list

    # Assign value of require_projection_in_composition
    for state in owner._input_states:
        # Assign True for owner's primary InputState and the value has not already been set in InputState constructor
        if state.require_projection_in_composition is None and owner.input_state == state:
            state.parameters.require_projection_in_composition._set(True, context)

    # Check that number of input_states and their variables are consistent with owner.defaults.variable,
    #    and adjust the latter if not
    variable_item_is_OK = False
    for i, input_state in enumerate(owner.input_states):
        try:
            variable_item_is_OK = iscompatible(owner.defaults.variable[i], input_state.value)
            if not variable_item_is_OK:
                break
        except IndexError:
            variable_item_is_OK = False
            break

    if not variable_item_is_OK:
        old_variable = owner.defaults.variable
        owner.defaults.variable = owner._handle_default_variable(default_variable=[state.value for state in owner.input_states])

        if owner.verbosePref:
            warnings.warn(
                "Variable for {} ({}) has been adjusted to match number and format of its input_states: ({})".format(
                    old_variable,
                    append_type_to_name(owner),
                    owner.defaults.variable,
                )
            )

    return state_list

def _parse_shadow_inputs(owner, input_states):
    """Parses any {SHADOW_INPUTS:[InputState or Mechaism,...]} items in input_states into InputState specif. dict."""

    input_states_to_shadow_specs=[]
    for spec_idx, spec in enumerate(input_states):
        # If {SHADOW_INPUTS:[InputState or Mechaism,...]} is found:
        if isinstance(spec, dict) and SHADOW_INPUTS in spec:
            input_states_to_shadow_in_spec=[]
            # For each item in list of items to shadow specified in that entry:
            for item in list(spec[SHADOW_INPUTS]):
                from psyneulink.core.components.mechanisms.mechanism import Mechanism
                # If an InputState was specified, just used that
                if isinstance(item, InputState):
                    input_states_to_shadow_in_spec.append(item)
                # If Mechanism was specified, use all of its InputStates
                elif isinstance(item, Mechanism):
                    input_states_to_shadow_in_spec.extend(item.input_states)
                else:
                    raise InputStateError("Specification of {} in for {} arg of {} must be a {} or {}".
                                          format(repr(SHADOW_INPUTS), repr(INPUT_STATES), owner.name,
                                                 Mechanism.__name__, InputState.__name__))
            input_states_to_shadow_specs.append((spec_idx, input_states_to_shadow_in_spec))

    # If any SHADOW_INPUTS specs were found in input_states, replace them with actual InputStates to be shadowed
    if input_states_to_shadow_specs:
        for item in input_states_to_shadow_specs:
            idx = item[0]
            del input_states[idx]
            input_states[idx:idx] = item[1]
        # Update owner's variable based on full set of InputStates specified
        owner.defaults.variable, _ = owner._handle_arg_input_states(input_states)

    return input_states
