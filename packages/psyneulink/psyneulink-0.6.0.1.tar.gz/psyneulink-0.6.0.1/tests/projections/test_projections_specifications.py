import psyneulink as pnl
import numpy as np
import pytest

import psyneulink.core.components.functions.distributionfunctions
import psyneulink.core.components.functions.statefulfunctions.integratorfunctions
import psyneulink.core.components.functions.transferfunctions


class TestProjectionSpecificationFormats:

    def test_multiple_modulatory_projection_specs(self):

        M = pnl.DDM(name='MY DDM')
        C = pnl.ControlMechanism(control_signals=[{pnl.PROJECTIONS: [M.parameter_states[
                                                                         psyneulink.core.components.functions.distributionfunctions.DRIFT_RATE],
                                                                     M.parameter_states[
                                                                         psyneulink.core.components.functions.distributionfunctions.THRESHOLD]]}])
        G = pnl.GatingMechanism(gating_signals=[{pnl.PROJECTIONS: [M.output_states[pnl.DECISION_VARIABLE],
                                                                     M.output_states[pnl.RESPONSE_TIME]]}])
        assert len(C.control_signals)==1
        assert len(C.control_signals[0].efferents)==2
        assert M.parameter_states[
                   psyneulink.core.components.functions.distributionfunctions.DRIFT_RATE].mod_afferents[0] == C.control_signals[0].efferents[0]
        assert M.parameter_states[
                   psyneulink.core.components.functions.distributionfunctions.THRESHOLD].mod_afferents[0] == C.control_signals[0].efferents[1]
        assert len(G.gating_signals)==1
        assert len(G.gating_signals[0].efferents)==2
        assert M.output_states[pnl.DECISION_VARIABLE].mod_afferents[0]==G.gating_signals[0].efferents[0]
        assert M.output_states[pnl.RESPONSE_TIME].mod_afferents[0]==G.gating_signals[0].efferents[1]

    def test_multiple_modulatory_projections_with_state_name(self):

        M = pnl.DDM(name='MY DDM')
        C = pnl.ControlMechanism(control_signals=[{'DECISION_CONTROL':[M.parameter_states[
                                                                           psyneulink.core.components.functions.distributionfunctions.DRIFT_RATE],
                                                                       M.parameter_states[
                                                                           psyneulink.core.components.functions.distributionfunctions.THRESHOLD]]}])
        G = pnl.GatingMechanism(gating_signals=[{'DDM_OUTPUT_GATE':[M.output_states[pnl.DECISION_VARIABLE],
                                                                    M.output_states[pnl.RESPONSE_TIME]]}])
        assert len(C.control_signals)==1
        assert C.control_signals[0].name=='DECISION_CONTROL'
        assert len(C.control_signals[0].efferents)==2
        assert M.parameter_states[
                   psyneulink.core.components.functions.distributionfunctions.DRIFT_RATE].mod_afferents[0] == C.control_signals[0].efferents[0]
        assert M.parameter_states[
                   psyneulink.core.components.functions.distributionfunctions.THRESHOLD].mod_afferents[0] == C.control_signals[0].efferents[1]
        assert len(G.gating_signals)==1
        assert G.gating_signals[0].name=='DDM_OUTPUT_GATE'
        assert len(G.gating_signals[0].efferents)==2
        assert M.output_states[pnl.DECISION_VARIABLE].mod_afferents[0]==G.gating_signals[0].efferents[0]
        assert M.output_states[pnl.RESPONSE_TIME].mod_afferents[0]==G.gating_signals[0].efferents[1]

    def test_multiple_modulatory_projections_with_mech_and_state_name_specs(self):

        M = pnl.DDM(name='MY DDM')
        C = pnl.ControlMechanism(control_signals=[{pnl.MECHANISM: M,
                                                   pnl.PARAMETER_STATES: [
                                                       psyneulink.core.components.functions.distributionfunctions.DRIFT_RATE,

                                                       psyneulink.core.components.functions.distributionfunctions.THRESHOLD]}])
        G = pnl.GatingMechanism(gating_signals=[{pnl.MECHANISM: M,
                                                 pnl.OUTPUT_STATES: [pnl.DECISION_VARIABLE, pnl.RESPONSE_TIME]}])
        assert len(C.control_signals)==1
        assert len(C.control_signals[0].efferents)==2
        assert M.parameter_states[
                   psyneulink.core.components.functions.distributionfunctions.DRIFT_RATE].mod_afferents[0] == C.control_signals[0].efferents[0]
        assert M.parameter_states[
                   psyneulink.core.components.functions.distributionfunctions.THRESHOLD].mod_afferents[0] == C.control_signals[0].efferents[1]
        assert len(G.gating_signals)==1
        assert len(G.gating_signals[0].efferents)==2
        assert M.output_states[pnl.DECISION_VARIABLE].mod_afferents[0]==G.gating_signals[0].efferents[0]
        assert M.output_states[pnl.RESPONSE_TIME].mod_afferents[0]==G.gating_signals[0].efferents[1]

    def test_mapping_projection_with_mech_and_state_name_specs(self):
         R1 = pnl.TransferMechanism(output_states=['OUTPUT_1', 'OUTPUT_2'])
         R2 = pnl.TransferMechanism(default_variable=[[0],[0]],
                                    input_states=['INPUT_1', 'INPUT_2'])
         T = pnl.TransferMechanism(input_states=[{pnl.MECHANISM: R1,
                                                  pnl.OUTPUT_STATES: ['OUTPUT_1', 'OUTPUT_2']}],
                                   output_states=[{pnl.MECHANISM:R2,
                                                   pnl.INPUT_STATES: ['INPUT_1', 'INPUT_2']}])
         assert len(R1.output_states)==2
         assert len(R2.input_states)==2
         assert len(T.input_states)==1
         for input_state in T.input_states:
             for projection in input_state.path_afferents:
                 assert projection.sender.owner is R1
         assert len(T.output_states)==1
         for output_state in T.output_states:
             for projection in output_state.efferents:
                 assert projection.receiver.owner is R2

    def test_mapping_projection_using_2_item_tuple_with_list_of_state_names(self):

        T1 = pnl.TransferMechanism(name='T1', input_states=[[0,0],[0,0,0]])
        T2 = pnl.TransferMechanism(name='T2',
                                   output_states=[(['InputState-0','InputState-1'], T1)])
        assert len(T2.output_states)==1
        assert T2.output_states[0].efferents[0].receiver.name == 'InputState-0'
        assert T2.output_states[0].efferents[0].matrix.shape == (1,2)
        assert T2.output_states[0].efferents[1].receiver.name == 'InputState-1'
        assert T2.output_states[0].efferents[1].matrix.shape == (1,3)

    def test_mapping_projection_using_2_item_tuple_and_3_item_tuples_with_index_specs(self):

        T1 = pnl.TransferMechanism(name='T1', input_states=[[0,0],[0,0,0]])
        T2 = pnl.TransferMechanism(name='T2',
                                   input_states=['a','b','c'],
                                   output_states=[(['InputState-0','InputState-1'], T1),
                                                  ('InputState-0', (pnl.OWNER_VALUE, 2), T1),
                                                  (['InputState-0','InputState-1'], 1, T1)])
        assert len(T2.output_states)==3
        assert T2.output_states[0].efferents[0].receiver.name == 'InputState-0'
        assert T2.output_states[0].efferents[0].matrix.shape == (1,2)
        assert T2.output_states[0].efferents[1].receiver.name == 'InputState-1'
        assert T2.output_states[0].efferents[1].matrix.shape == (1,3)
        assert T2.output_states[1].owner_value_index == 2
        assert T2.output_states[2].owner_value_index == 1

    def test_2_item_tuple_from_control_signal_to_parameter_state(self):

        D = pnl.DDM(name='D')

        # Single name
        C = pnl.ControlMechanism(control_signals=[(
                                                  psyneulink.core.components.functions.distributionfunctions.DRIFT_RATE, D)])
        assert C.control_signals[0].name == 'D[drift_rate] ControlSignal'
        assert C.control_signals[0].efferents[0].receiver.name == 'drift_rate'

        # List of names
        C = pnl.ControlMechanism(control_signals=[([
                                                       psyneulink.core.components.functions.distributionfunctions.DRIFT_RATE,
                                                       psyneulink.core.components.functions.distributionfunctions.THRESHOLD], D)])
        assert C.control_signals[0].name == 'D[drift_rate, threshold] ControlSignal'
        assert C.control_signals[0].efferents[0].receiver.name == 'drift_rate'
        assert C.control_signals[0].efferents[1].receiver.name == 'threshold'

    def test_2_item_tuple_from_parameter_state_to_control_signals(self):

        C = pnl.ControlMechanism(control_signals=['a','b'])
        D = pnl.DDM(name='D3',
                     function=psyneulink.core.components.functions.distributionfunctions.DriftDiffusionAnalytical(drift_rate=(3, C),
                                                                                                                  threshold=(2,C.control_signals['b']))
                    )
        assert D.parameter_states[
                   psyneulink.core.components.functions.distributionfunctions.DRIFT_RATE].mod_afferents[0].sender == C.control_signals[0]
        assert D.parameter_states[
                   psyneulink.core.components.functions.distributionfunctions.THRESHOLD].mod_afferents[0].sender == C.control_signals[1]

    def test_2_item_tuple_from_gating_signal_to_output_states(self):

        D4 = pnl.DDM(name='D4')

        # Single name
        G = pnl.GatingMechanism(gating_signals=[(pnl.DECISION_VARIABLE, D4)])
        assert G.gating_signals[0].name == 'D4[DECISION_VARIABLE] GatingSignal'
        assert G.gating_signals[0].efferents[0].receiver.name == 'DECISION_VARIABLE'

        # List of names
        G = pnl.GatingMechanism(gating_signals=[([pnl.DECISION_VARIABLE, pnl.RESPONSE_TIME], D4)])
        assert G.gating_signals[0].name == 'D4[DECISION_VARIABLE, RESPONSE_TIME] GatingSignal'
        assert G.gating_signals[0].efferents[0].receiver.name == 'DECISION_VARIABLE'
        assert G.gating_signals[0].efferents[1].receiver.name == 'RESPONSE_TIME'

    def test_2_item_tuple_from_input_and_output_states_to_gating_signals(self):

        G = pnl.GatingMechanism(gating_signals=['a','b'])
        T = pnl.TransferMechanism(name='T',
                     input_states=[(3,G)],
                     output_states=[(2,G.gating_signals['b'])]
                                  )
        assert T.input_states[0].mod_afferents[0].sender==G.gating_signals[0]
        assert T.output_states[0].mod_afferents[0].sender==G.gating_signals[1]

    def test_formats_for_control_specification_for_mechanism_and_function_params(self):

        control_spec_list = [
            pnl.CONTROL,
            pnl.CONTROL_SIGNAL,
            pnl.CONTROL_PROJECTION,
            pnl.ControlSignal,
            pnl.ControlSignal(),
            pnl.ControlProjection,
            "CP_OBJECT",
            pnl.ControlMechanism,
            pnl.ControlMechanism(),
            pnl.ModulatoryMechanism,
            (0.3, pnl.CONTROL),
            (0.3, pnl.CONTROL_SIGNAL),
            (0.3, pnl.CONTROL_PROJECTION),
            (0.3, pnl.ControlSignal),
            (0.3, pnl.ControlSignal()),
            (0.3, pnl.ControlProjection),
            (0.3, "CP_OBJECT"),
            (0.3, pnl.ControlMechanism),
            (0.3, pnl.ControlMechanism()),
            (0.3, pnl.ModulatoryMechanism)
        ]
        for i, ctl_tuple in enumerate([j for j in zip(control_spec_list, reversed(control_spec_list))]):
            C1, C2 = ctl_tuple

            # This shenanigans is to avoid assigning the same instantiated ControlProjection more than once
            if C1 is 'CP_OBJECT':
                C1 = pnl.ControlProjection()
            elif isinstance(C1, tuple) and C1[1] is 'CP_OBJECT':
                C1 = (C1[0], pnl.ControlProjection())
            if C2 is 'CP_OBJECT':
                C2 = pnl.ControlProjection()
            elif isinstance(C2, tuple) and C2[1] is 'CP_OBJECT':
                C2 = (C2[0], pnl.ControlProjection())

            R = pnl.RecurrentTransferMechanism(noise=C1,
                                               function=psyneulink.core.components.functions.transferfunctions.Logistic(gain=C2))
            assert R.parameter_states[pnl.NOISE].mod_afferents[0].name in \
                   'ControlProjection for RecurrentTransferMechanism-{}[noise]'.format(i)
            assert R.parameter_states[pnl.GAIN].mod_afferents[0].name in \
                   'ControlProjection for RecurrentTransferMechanism-{}[gain]'.format(i)

    def test_formats_for_gating_specification_of_input_and_output_states(self):

        gating_spec_list = [
            pnl.GATING,
            pnl.GATING_SIGNAL,
            pnl.GATING_PROJECTION,
            pnl.GatingSignal,
            pnl.GatingSignal,
            pnl.GatingSignal(),
            pnl.GatingProjection,
            "GP_OBJECT",
            pnl.GatingMechanism,
            pnl.ModulatoryMechanism,
            pnl.GatingMechanism(),
            (0.3, pnl.GATING),
            (0.3, pnl.GATING_SIGNAL),
            (0.3, pnl.GATING_PROJECTION),
            (0.3, pnl.GatingSignal),
            (0.3, pnl.GatingSignal()),
            (0.3, pnl.GatingProjection),
            (0.3, "GP_OBJECT"),
            (0.3, pnl.GatingMechanism),
            (0.3, pnl.ModulatoryMechanism),
            (0.3, pnl.GatingMechanism())
        ]
        for i, gating_tuple in enumerate([j for j in zip(gating_spec_list, reversed(gating_spec_list))]):
            G1, G2 = gating_tuple

            # This shenanigans is to avoid assigning the same instantiated ControlProjection more than once
            if G1 is 'GP_OBJECT':
                G1 = pnl.GatingProjection()
            elif isinstance(G1, tuple) and G1[1] is 'GP_OBJECT':
                G1 = (G1[0], pnl.GatingProjection())
            if G2 is 'GP_OBJECT':
                G2 = pnl.GatingProjection()
            elif isinstance(G2, tuple) and G2[1] is 'GP_OBJECT':
                G2 = (G2[0], pnl.GatingProjection())

            T = pnl.TransferMechanism(name='T-GATING-{}'.format(i),
                                      input_states=[G1],
                                      output_states=[G2])
            assert T.input_states[0].mod_afferents[0].name in \
                   'GatingProjection for T-GATING-{}[InputState-0]'.format(i)

            assert T.output_states[0].mod_afferents[0].name in \
                   'GatingProjection for T-GATING-{}[OutputState-0]'.format(i)

        with pytest.raises(pnl.ProjectionError) as error_text:
            T1 = pnl.ProcessingMechanism(name='T1', input_states=[pnl.ModulatoryMechanism()])
        assert 'Primary OutputState of ModulatoryMechanism-0 (ControlSignal-0) ' \
               'cannot be used as a sender of a Projection to InputState of T1' in error_text.value.args[0]

        with pytest.raises(pnl.ProjectionError) as error_text:
            T2 = pnl.ProcessingMechanism(name='T2', output_states=[pnl.ModulatoryMechanism()])
        assert 'Primary OutputState of ModulatoryMechanism-1 (ControlSignal-0) ' \
               'cannot be used as a sender of a Projection to OutputState of T2' in error_text.value.args[0]


    # KDM: this is a good candidate for pytest.parametrize
    def test_masked_mapping_projection(self):

        t1 = pnl.TransferMechanism(size=2)
        t2 = pnl.TransferMechanism(size=2)
        proj = pnl.MaskedMappingProjection(sender=t1,
                                    receiver=t2,
                                    matrix=[[1,2],[3,4]],
                                    mask=[[1,0],[0,1]],
                                    mask_operation=pnl.ADD
                                    )
        p = pnl.Process(pathway=[t1, proj, t2])
        val = p.execute(input=[1,2])
        assert np.allclose(val, [[8, 12]])

        t1 = pnl.TransferMechanism(size=2)
        t2 = pnl.TransferMechanism(size=2)
        proj = pnl.MaskedMappingProjection(sender=t1,
                                    receiver=t2,
                                    matrix=[[1,2],[3,4]],
                                    mask=[[1,0],[0,1]],
                                    mask_operation=pnl.MULTIPLY
                                    )
        p = pnl.Process(pathway=[t1, proj, t2])
        val = p.execute(input=[1,2])
        assert np.allclose(val, [[1, 8]])

        t1 = pnl.TransferMechanism(size=2)
        t2 = pnl.TransferMechanism(size=2)
        proj = pnl.MaskedMappingProjection(sender=t1,
                                    receiver=t2,
                                    mask=[[1,2],[3,4]],
                                    mask_operation=pnl.MULTIPLY
                                    )
        p = pnl.Process(pathway=[t1, proj, t2])
        val = p.execute(input=[1,2])
        assert np.allclose(val, [[1, 8]])

    def test_masked_mapping_projection_mask_conficts_with_matrix(self):

        with pytest.raises(pnl.MaskedMappingProjectionError) as error_text:

            t1 = pnl.TransferMechanism(size=2)
            t2 = pnl.TransferMechanism(size=2)
            pnl.MaskedMappingProjection(sender=t1,
                                        receiver=t2,
                                        mask=[[1,2,3],[4,5,6]],
                                        mask_operation=pnl.MULTIPLY
                                        )
        assert "Shape of the 'mask'" in str(error_text.value)
        assert "((2, 3)) must be the same as its 'matrix' ((2, 2))" in str(error_text.value)

    # FIX 7/22/15 [JDC] - REPLACE WITH MORE ELABORATE TESTS OF DUPLICATE PROJECTIONS:
    #                     SAME FROM OUTPUTSTATE;  SAME TO INPUT STATE
    #                     TEST ERROR MESSAGES GENERATED BY VARIOUS _check_for_duplicates METHODS
    # def test_duplicate_projection_detection_and_warning(self):
    #
    #     with pytest.warns(UserWarning) as record:
    #         T1 = pnl.TransferMechanism(name='T1')
    #         T2 = pnl.TransferMechanism(name='T2')
    #         T3 = pnl.TransferMechanism(name='T3')
    #         T4 = pnl.TransferMechanism(name='T4')
    #
    #         MP1 = pnl.MappingProjection(sender=T1,receiver=T2,name='MP1')
    #         MP2 = pnl.MappingProjection(sender=T1,receiver=T2,name='MP2')
    #         pnl.proc(T1,MP1,T2,T3)
    #         pnl.proc(T1,MP2,T2,T4)
    #
    #     # hack to find a specific warning (other warnings may be generated by the Process construction)
    #     correct_message_found = False
    #     for warning in record:
    #         if "that already has an identical Projection" in str(warning.message):
    #             correct_message_found = True
    #             break
    #
    #     assert len(T2.afferents)==1
    #     assert correct_message_found

    def test_duplicate_projection_creation_error(self):

        from psyneulink.core.components.projections.projection import DuplicateProjectionError
        with pytest.raises(DuplicateProjectionError) as record:
            T1 = pnl.TransferMechanism(name='T1')
            T2 = pnl.TransferMechanism(name='T2')
            pnl.MappingProjection(sender=T1,receiver=T2,name='MP1')
            pnl.MappingProjection(sender=T1,receiver=T2,name='MP2')
        assert 'Attempt to assign Projection to InputState-0 of T2 that already has an identical Projection.' \
               in record.value.args[0]

