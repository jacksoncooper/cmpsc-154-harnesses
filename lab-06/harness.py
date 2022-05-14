import pytest

import pyrtl as rtl

import ucsbcs154_lab6_forward as cpu

v0 = 2
a0, a1, a2, a3 = 4, 5, 6, 7
t0, t1, t2, t3, t4, t5, t6, t7 = 8, 9, 10, 11, 12, 13, 14, 15

def expect_memory(actual, expected):
    # The memory must have the same number of addresses with assigned values.
    assert len(actual) == len(expected)

    # The memory must have the the same values at those addresses.
    for address, value in expected.items():
        assert address in actual and actual[address] == value

    # inspect() excludes addresses that ... have not been assigned a value?

    # address_space = set(range(0, pow(2, address_width)))
    # unused = address_space - set(expected.keys())

    # for address in unused:
    #     assert not actual[address]

class TestExecuteHazard:
    def test_type_one_a_hazard(self):
        memory = {
            cpu.rf:    {t1: 7, t2: 5},
            cpu.i_mem: {
                4: 0x012A4020, # add $t0, $t1, $t2
                8: 0x01095820, # add $t3, $t0, $t1
            }
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        for cycle in range(12):
            go.step({})

        expect_memory(go.inspect_mem(cpu.rf), {t0: 12, t1: 7, t2: 5, t3: 19})

    def test_type_one_b_hazard(self):
        memory = {
            cpu.rf:    {t1: 7, t2: 5},
            cpu.i_mem: {
                4: 0x012A4020, # add $t0, $t1, $t2
                8: 0x01285820, # add $t3, $t1, $t0
            }
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        for cycle in range(12):
            go.step({})

        expect_memory(go.inspect_mem(cpu.rf), {t0: 12, t1: 7, t2: 5, t3: 19})

    def test_type_one_a_and_one_b_hazard(self):
        memory = {
            cpu.rf:    {t1: 7, t2: 5},
            cpu.i_mem: {
                4: 0x012A4020, # add $t0, $t1, $t2
                8: 0x01085820, # add $t3, $t0, $t0
            }
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        for cycle in range(12):
            go.step({})

        expect_memory(go.inspect_mem(cpu.rf), {t0: 12, t1: 7, t2: 5, t3: 24})

    def test_type_one_a_hazard_with_zero_forward(self):
        memory = {
            cpu.rf:    {t1: 7, t2: 5},
            cpu.i_mem: {
                4: 0x012A0020, # add $zero, $t1, $t2
                8: 0x00095820, # add $t3, $zero, $t1
            }
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        for cycle in range(12):
            go.step({})

        expect_memory(go.inspect_mem(cpu.rf), {t1: 7, t2: 5, t3: 7})
