# Princeton University licenses this file to You under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.  You may obtain a copy of the License at:
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.


# **************************************  DefaultControlMechanism ************************************************

"""

The DefaultControlMechanism is created for a `System` if no other controller type is specified. The
DefaultControlMechanism creates an `ControlSignal` for each `ControlProjection` it is assigned, and uses
`defaultControlAllocation` as the `value <ControlSignal.value>` for the ControlSignal.  By default,
`defaultControlAllocation` =  1, so that ControlProjections from the DefaultControlMechanism have no effect on their
parameters.  However, it can be used to uniformly control the parameters that receive ControlProjections from it,
by manually changing the value of `defaultControlAllocation`.  See `ControlMechanism <ControlMechanism>` for additional
details of how ControlMechanism are created, executed and their attributes.

COMMENT:
   ADD LINK FOR defaultControlAllocation

    TEST FOR defaultControlAllocation:  |defaultControlAllocation|

    ANOTHER TEST FOR defaultControlAllocation:  :py:print:`defaultControlAllocation`

    AND YET ANOTHER TEST FOR defaultControlAllocation:  :py:print:|defaultControlAllocation|

    LINK TO DEFAULTS: :doc:`Defaults`
COMMENT


"""

import numpy as np
import typecheck as tc

from psyneulink.core.components.mechanisms.modulatory.control.controlmechanism import ControlMechanism
from psyneulink.core.components.mechanisms.processing.objectivemechanism import ObjectiveMechanism
from psyneulink.core.globals.defaults import defaultControlAllocation
from psyneulink.core.globals.keywords import CONTROL, FUNCTION, FUNCTION_PARAMS, INPUT_STATES, INTERCEPT, MODULATION, NAME, OBJECTIVE_MECHANISM, SLOPE
from psyneulink.core.globals.preferences.basepreferenceset import is_pref_set
from psyneulink.core.globals.preferences.preferenceset import PreferenceLevel
from psyneulink.core.globals.utilities import ContentAddressableList

__all__ = [
    'DefaultControlMechanism', 'DefaultControlMechanismError'
]


class DefaultControlMechanismError(Exception):
    def __init__(self, error_value):
        self.error_value = error_value


class DefaultControlMechanism(ControlMechanism):
    """Subclass of `ControlMechanism <ControlMechanism>` that implements a DefaultControlMechanism.

    COMMENT:
        Description:
            Implements default source of control signals, with one inputState and outputState for each.
            Uses defaultControlAllocation as input(s) and pass value(s) unchanged to outputState(s) and
            ControlProjection(s)

            Every ControlProjection is assigned this Mechanism as its sender by default (i.e., unless a sender is
                explicitly specified in its constructor).

            An inputState and outputState is created for each ControlProjection assigned:
                the inputState is assigned the
                :py:constant:`defaultControlAllocation <Defaults.defaultControlAllocation>` value;
                when the DefaultControlMechanism executes, it simply assigns the same value to the ControlProjection.

            Class attributes:
                + componentType (str): System Default Mechanism
                + paramClassDefaults (dict):
                    + FUNCTION: Linear
    COMMENT
    """

    componentType = "DefaultControlMechanism"

    classPreferenceLevel = PreferenceLevel.SUBTYPE
    # classPreferenceLevel = PreferenceLevel.TYPE

    # Any preferences specified below will override those specified in TYPE_DEFAULT_PREFERENCES
    # Note: only need to specify setting;  level will be assigned to Type automatically
    # classPreferences = {
    #     PREFERENCE_SET_NAME: 'DefaultControlMechanismCustomClassPreferences',
    #     PREFERENCE_KEYWORD<pref>: <setting>...}

    from psyneulink.core.components.functions.transferfunctions import Linear
    paramClassDefaults = ControlMechanism.paramClassDefaults.copy()
    paramClassDefaults.update({FUNCTION:Linear,
                               FUNCTION_PARAMS:{SLOPE:1, INTERCEPT:0},
                               OBJECTIVE_MECHANISM:None,
                               MODULATION:None,
                               })

    @tc.typecheck
    def __init__(self,
                 # default_variable=None,
                 # size=None,
                 system=None,
                 objective_mechanism:tc.optional(tc.any(ObjectiveMechanism, list))=None,
                 control_signals:tc.optional(list)=None,
                 params=None,
                 name=None,
                 prefs:is_pref_set=None,
                 function=None,
                 **kwargs
                 ):

        super(DefaultControlMechanism, self).__init__(
                # default_variable=default_variable,
                # size=size,
                objective_mechanism=objective_mechanism,
                control_signals=control_signals,
                function=function,
                params=params,
                name=name,
                prefs=prefs,

                **kwargs)

    def _instantiate_input_states(self, context=None):
        """Instantiate input_value attribute

        Instantiate input_states and monitored_output_states attributes (in case they are referenced)
            and assign any OutputStates that project to the input_states to monitored_output_states

        IMPLEMENTATION NOTE:  At present, these are dummy assignments, simply to satisfy the requirements for
                              subclasses of ControlMechanism;  in the future, an _instantiate_objective_mechanism()
                              method should be implemented that also implements an _instantiate_monitored_output_states
                              method, and that can be used to add OutputStates/Mechanisms to be monitored.
        """

        if not hasattr(self, INPUT_STATES):
            self._input_states = None
        elif self.input_states:
            for input_state in self.input_states:
                for projection in input_state.path_afferents:
                    self.monitored_output_states.append(projection.sender)

    def _instantiate_control_signal(self, control_signal, context=None):
        """Instantiate requested ControlSignal, ControlProjection and associated InputState
        """
        from psyneulink.core.components.states.parameterstate import ParameterState

        if isinstance(control_signal, dict):
            if CONTROL in control_signal:
                projection = control_signal[CONTROL][0]
                input_name = 'DefaultControlAllocation for ' + projection.receiver.name + '_ControlSignal'
            elif NAME in control_signal:
                input_name = 'DefaultControlAllocation for ' + control_signal[NAME] + '_ControlSignal'

        elif isinstance(control_signal, tuple):
            input_name = 'DefaultControlAllocation for ' + control_signal[0] + '_ControlSignal'

        elif isinstance(control_signal, ParameterState):
            input_name = 'DefaultControlAllocation for ' + control_signal.name + '_ControlSignal'

        else:
            raise DefaultControlMechanismError("control signal ({}) was not a dict, tuple, or ParameterState".
                                               format(control_signal))

        # Instantiate input_states and control_allocation attribute for control_signal allocations
        self._instantiate_default_input_state(input_name, [defaultControlAllocation], context=context)
        self.control_allocation = self.input_values

        # Call super to instantiate ControlSignal
        # Note: any params specified with ControlProjection for the control_signal
        #           should be in PARAMS entry of dict passed in control_signal arg
        control_signal = super()._instantiate_control_signal(control_signal=control_signal, context=context)

    def _instantiate_default_input_state(self, input_state_name, input_state_value, context=None):
        """Instantiate inputState for ControlMechanism

        NOTE: This parallels ObjectMechanism._instantiate_input_state_for_monitored_state()
              It is implemented here to spare having to instantiate a "dummy" (and superfluous) ObjectiveMechanism
              for the sole purpose of creating input_states for each value of defaultControlAllocation to assign
              to the ControlProjections.

        Extend self.defaults.variable by one item to accommodate new inputState
        Instantiate the inputState using input_state_name and input_state_value
        Update self.input_state and self.input_states

        Args:
            input_state_name (str):
            input_state_value (2D np.array):
            context:

        Returns:
            input_state (InputState):

        """

        # First, test for initialization conditions:

        # This is for generality (in case, for any subclass in the future, variable is assigned to None on init)
        if self.defaults.variable is None:
            self.defaults.variable = np.atleast_2d(input_state_value)

        # If there is a single item in self.defaults.variable, it could be the one assigned on initialization
        #     (in order to validate ``function`` and get its return value as a template for value);
        #     in that case, there should be no input_states yet, so pass
        #     (i.e., don't bother to extend self.defaults.variable): it will be used for the new inputState
        elif len(self.defaults.variable) == 1:
            if self.input_states:
                self.defaults.variable = np.append(self.defaults.variable, np.atleast_2d(input_state_value), 0)
            else:
                # If there are no input_states, this is the usual initialization condition;
                # Pass to create a new inputState that will be assigned to existing the first item of self.defaults.variable
                pass
        # Other than on initialization (handled above), it is a PROGRAM ERROR if
        #    the number of input_states is not equal to the number of items in self.defaults.variable
        elif len(self.defaults.variable) != len(self.input_states):
            raise DefaultControlMechanismError(
                "PROGRAM ERROR:  The number of input_states ({}) does not match "
                "the number of items found for the variable attribute ({}) of {}"
                "when creating {}".format(
                    len(self.input_states),
                    len(self.defaults.variable),
                    self.name,
                    input_state_name,
                )
            )

        # Extend self.defaults.variable to accommodate new inputState
        else:
            self.defaults.variable = np.append(self.defaults.variable, np.atleast_2d(input_state_value), 0)

        variable_item_index = self.defaults.variable.size-1

        # Instantiate inputState
        from psyneulink.core.components.states.state import _instantiate_state
        from psyneulink.core.components.states.inputstate import InputState
        input_state = _instantiate_state(owner=self,
                                         state_type=InputState,
                                         name=input_state_name,
                                         reference_value=np.array(self.defaults.variable[variable_item_index]),
                                         reference_value_name='Default control allocation',
                                         params=None,
                                         context=context)

        #  Update inputState and input_states
        if self.input_states:
            self._input_states[input_state.name] = input_state
        else:
            from psyneulink.core.components.states.state import State_Base
            self._input_states = ContentAddressableList(component_type=State_Base,
                                                        list=[input_state],
                                                        name=self.name+'.input_states')

        # self.input_value = [state.value for state in self.input_states]

        return input_state
