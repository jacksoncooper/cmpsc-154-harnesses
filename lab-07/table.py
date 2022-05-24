import pytest

import pyrtl as rtl

import ucsbcs154_lab7_predtable as table

def vestigial_state(inputs):
    inputs[table.fetch_pc] = 0
    inputs[table.update_branch_pc] = 0
    return inputs

class TestIsolatedPredictor:
    def test_starts_predicting_not_taken(self):
        go = rtl.Simulation()
        assert go.inspect('pred_taken') == 0

    def test_repeatedly_predict_taken_from_confident_not_taken(self):
        go = rtl.Simulation()

        assert go.inspect('pred_taken') == 0

        go.step(vestigial_state({
            table.update_prediction: 1,
            table.update_branch_taken: 1
        }))
        assert go.inspect('pred_taken') == 0

        go.step(vestigial_state({
            table.update_prediction: 1,
            table.update_branch_taken: 1
        }))
        assert go.inspect('pred_taken') == 1

        go.step(vestigial_state({
            table.update_prediction: 1,
            table.update_branch_taken: 1
        }))
        assert go.inspect('pred_taken') == 1

        # Test confidence only provides one wrong guess of buffer.

        for _ in range(16):
            go.step(vestigial_state({
                table.update_prediction: 1,
                table.update_branch_taken: 1
            }))
            assert go.inspect('pred_taken') == 1

        go.step(vestigial_state({
            table.update_prediction: 1,
            table.update_branch_taken: 0
        }))
        assert go.inspect('pred_taken') == 1

        go.step(vestigial_state({
            table.update_prediction: 1,
            table.update_branch_taken: 0
        }))
        assert go.inspect('pred_taken') == 0

    def test_repeatedly_predict_not_taken_from_confident_taken(self):
        go = rtl.Simulation()

        assert go.inspect('pred_taken') == 0

        go.step(vestigial_state({
            table.update_prediction: 1,
            table.update_branch_taken: 1
        }))
        assert go.inspect('pred_taken') == 0

        go.step(vestigial_state({
            table.update_prediction: 1,
            table.update_branch_taken: 1
        }))
        assert go.inspect('pred_taken') == 1

        go.step(vestigial_state({
            table.update_prediction: 1,
            table.update_branch_taken: 1
        }))
        assert go.inspect('pred_taken') == 1

        # Should be in the confident taken state.

        go.step(vestigial_state({
            table.update_prediction: 1,
            table.update_branch_taken: 0
        }))
        assert go.inspect('pred_taken') == 1

        go.step(vestigial_state({
            table.update_prediction: 1,
            table.update_branch_taken: 0
        }))
        assert go.inspect('pred_taken') == 0

        go.step(vestigial_state({
            table.update_prediction: 1,
            table.update_branch_taken: 0
        }))
        assert go.inspect('pred_taken') == 0

        # Test confidence only provides one wrong guess of buffer.

        for _ in range(16):
            go.step(vestigial_state({
                table.update_prediction: 1,
                table.update_branch_taken: 0
            }))
            assert go.inspect('pred_taken') == 0

        go.step(vestigial_state({
            table.update_prediction: 1,
            table.update_branch_taken: 1
        }))
        assert go.inspect('pred_taken') == 0

        go.step(vestigial_state({
            table.update_prediction: 1,
            table.update_branch_taken: 1
        }))
        assert go.inspect('pred_taken') == 1

    def test_thrash_between_unconfident_states(self):
        go = rtl.Simulation()

        assert go.inspect('pred_taken') == 0

        go.step(vestigial_state({
            table.update_prediction: 1,
            table.update_branch_taken: 1
        }))
        assert go.inspect('pred_taken') == 0

        for _ in range(16):
            go.step(vestigial_state({
                table.update_prediction: 1,
                table.update_branch_taken: 1
            }))
            assert go.inspect('pred_taken') == 1

            go.step(vestigial_state({
                table.update_prediction: 1,
                table.update_branch_taken: 0
            }))
            assert go.inspect('pred_taken') == 0

    def test_prediction_control_bit_prevents_internal_state_from_updating(self):
        go = rtl.Simulation()

        assert go.inspect('pred_taken') == 0

        go.step(vestigial_state({
            table.update_prediction: 1,
            table.update_branch_taken: 1
        }))
        assert go.inspect('pred_taken') == 0

        go.step(vestigial_state({
            table.update_prediction: 0,
            table.update_branch_taken: 1
        }))
        assert go.inspect('pred_taken') == 0

        go.step(vestigial_state({
            table.update_prediction: 0,
            table.update_branch_taken: 1
        }))
        assert go.inspect('pred_taken') == 0

        go.step(vestigial_state({
            table.update_prediction: 1,
            table.update_branch_taken: 0
        }))
        assert go.inspect('pred_taken') == 0

class TestParallelPredictors:
    def test_predictors_have_separate_state(self):
        go = rtl.Simulation()

        assert go.inspect('pred_taken') == 0

        go.step({
            table.update_branch_pc: 4,
            table.fetch_pc: 4,
            table.update_prediction: 1,
            table.update_branch_taken: 1,
        })
        assert go.inspect('pred_taken') == 0

        go.step({
            table.update_branch_pc: 4,
            table.fetch_pc: 4,
            table.update_prediction: 1,
            table.update_branch_taken: 1,
        })
        assert go.inspect('pred_taken') == 1

        go.step({
            table.update_branch_pc: 12,
            table.fetch_pc: 12,
            table.update_prediction: 1,
            table.update_branch_taken: 0,
        })
        assert go.inspect('pred_taken') == 0

        assert go.inspect_mem(table.pred_state) == {0b001: 0b10, 0b011: 0b00}
