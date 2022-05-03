import pytest
import cpu

t0, t1, t2 = 8, 9, 10

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

### ADD ###

class TestAdd:
    def test_add_different_operands_and_destination_is_not_operand(self):
        memory = {
            cpu.rf:    {t1: 7, t2: 5},
            cpu.i_mem: {0 : 0x012A4020}
        }

        go = cpu.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        go.step({})
        expect_memory(go.inspect_mem(cpu.rf), {t0: 12, t1: 7, t2: 5})
        expect_memory(go.inspect_mem(cpu.d_mem), {})

    def test_add_does_not_react_to_overflow(self):
        memory = {
            cpu.rf:    {t1: 0x80000000, t2: 0x80000000},
            cpu.i_mem: {0: 0x012A4020}
        }

        go = cpu.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        go.step({})
        expect_memory(go.inspect_mem(cpu.rf), {t0: 0, t1: 0x80000000, t2: 0x80000000})
        expect_memory(go.inspect_mem(cpu.d_mem), {})

### AND ###

class TestAnd:
    def test_and_different_operands_and_destination_is_not_operand(self):
        memory = {
            cpu.rf:    {t1: 7, t2: 5},
            cpu.i_mem: {0 : 0x012A4024}
        }

        go = cpu.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        go.step({})
        expect_memory(go.inspect_mem(cpu.rf), {t0: 5, t1: 7, t2: 5})
        expect_memory(go.inspect_mem(cpu.d_mem), {})

### ADDI ###

class TestAddI:
    def test_addi_different_operand_and_destination(self):
        memory = {
            cpu.rf:    {t1: 7},
            cpu.i_mem: {0 : 0x21280005}
        }

        go = cpu.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        go.step({})
        expect_memory(go.inspect_mem(cpu.rf), {t0: 12, t1: 7})
        expect_memory(go.inspect_mem(cpu.d_mem), {})

    def test_addi_different_operand_and_destination_with_arithmetic_extension(self):
        memory = {
            cpu.rf:    {t1: 7},
            cpu.i_mem: {0 : 0x2128FFFB}
        }

        go = cpu.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        go.step({})
        expect_memory(go.inspect_mem(cpu.rf), {t0: 2, t1: 7})
        expect_memory(go.inspect_mem(cpu.d_mem), {})
