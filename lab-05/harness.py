import pytest

import pyrtl as rtl

import cpu

v0, t0, t1, t2, t3, t4 = 2, 8, 9, 10, 11, 12

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
            cpu.i_mem: {0: 0x012A4020}
        }

        go = rtl.Simulation(
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

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        go.step({})
        expect_memory(go.inspect_mem(cpu.rf), {t0: 0, t1: 0x80000000, t2: 0x80000000})
        expect_memory(go.inspect_mem(cpu.d_mem), {})

    def test_add_does_not_clobber_zero_register(self):
        memory = {
            cpu.rf:    {t1: 7, t2: 5},
            cpu.i_mem: {0: 0x012A0020}
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        go.step({})
        expect_memory(go.inspect_mem(cpu.rf), {t1: 7, t2: 5})
        expect_memory(go.inspect_mem(cpu.d_mem), {})

### AND ###

class TestAnd:
    def test_and_different_operands_and_destination_is_not_operand(self):
        memory = {
            cpu.rf:    {t1: 7, t2: 5},
            cpu.i_mem: {0: 0x012A4024}
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        go.step({})
        expect_memory(go.inspect_mem(cpu.rf), {t0: 5, t1: 7, t2: 5})
        expect_memory(go.inspect_mem(cpu.d_mem), {})

### ADDI ###

class TestAddImmediate:
    def test_addi_different_operand_and_destination(self):
        memory = {
            cpu.rf:    {t1: 7},
            cpu.i_mem: {0: 0x21280005}
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        go.step({})
        expect_memory(go.inspect_mem(cpu.rf), {t0: 12, t1: 7})
        expect_memory(go.inspect_mem(cpu.d_mem), {})

    def test_addi_different_operand_and_destination_with_arithmetic_extension(self):
        memory = {
            cpu.rf:    {t1: 7},
            cpu.i_mem: {0: 0x2128FFFB}
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        go.step({})
        expect_memory(go.inspect_mem(cpu.rf), {t0: 2, t1: 7})
        expect_memory(go.inspect_mem(cpu.d_mem), {})

    def test_addi_does_not_clobber_zero_register(self):
        memory = {
            cpu.rf:    {t1: 7},
            cpu.i_mem: {0: 0x21200005}
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        go.step({})
        expect_memory(go.inspect_mem(cpu.rf), {t1: 7})
        expect_memory(go.inspect_mem(cpu.d_mem), {})

### LUI ###

class TestLoadUpperImmediate:
    def test_lui(self):
        memory = {
            cpu.rf:    {t0: 0xabcdeeee},
            cpu.i_mem: {0: 0x3C081234}
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        go.step({})
        expect_memory(go.inspect_mem(cpu.rf), {t0: 0x12340000})
        expect_memory(go.inspect_mem(cpu.d_mem), {})

### ORI ###

class TestOrImmediate:
    def test_ori_different_operand_and_destination(self):
        memory = {
            cpu.rf:    {t1: 0x11111},
            cpu.i_mem: {0: 0x21280202}
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        go.step({})
        expect_memory(go.inspect_mem(cpu.rf), {t0: 0x11313, t1: 0x11111})
        expect_memory(go.inspect_mem(cpu.d_mem), {})

### SLT ###

class TestSetOnLessThan:
    def test_slt_with_positive_larger_second_operand_and_destination_is_not_operand(self):
        memory = {
            cpu.rf:    {t1: 5, t2: 7},
            cpu.i_mem: {0: 0x012A402A}
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        go.step({})
        expect_memory(go.inspect_mem(cpu.rf), {t0: 1, t1: 5, t2: 7})
        expect_memory(go.inspect_mem(cpu.d_mem), {})

    def test_slt_with_positive_smaller_second_operand_and_destination_is_not_operand(self):
        memory = {
            cpu.rf:    {t1: 7, t2: 5},
            cpu.i_mem: {0: 0x012A402A}
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        go.step({})
        expect_memory(go.inspect_mem(cpu.rf), {t0: 0, t1: 7, t2: 5})
        expect_memory(go.inspect_mem(cpu.d_mem), {})

    def test_slt_with_negative_second_operand_and_destination_is_not_operand(self):
        memory = {
            cpu.rf:    {t1: 5, t2: 0xffff_fff9},
            cpu.i_mem: {0: 0x012A402A}
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        go.step({})
        expect_memory(go.inspect_mem(cpu.rf), {t0: 0, t1: 5, t2: 0xffff_fff9})
        expect_memory(go.inspect_mem(cpu.d_mem), {})

    def test_slt_with_negative_first_operand_and_destination_is_not_operand(self):
        memory = {
            cpu.rf:    {t1: 0xffff_fff9, t2: 5},
            cpu.i_mem: {0: 0x012A402A}
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        go.step({})
        expect_memory(go.inspect_mem(cpu.rf), {t0: 1, t1: 0xffff_fff9, t2: 5})
        expect_memory(go.inspect_mem(cpu.d_mem), {})

    def test_slt_with_negative_larger_second_operand_and_destination_is_not_operand(self):
        memory = {
            cpu.rf:    {t1: 0xffff_fff9, t2: 0xffff_fffb},
            cpu.i_mem: {0: 0x012A402A}
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        go.step({})
        expect_memory(go.inspect_mem(cpu.rf), {t0: 1, t1: 0xffff_fff9, t2: 0xffff_fffb})
        expect_memory(go.inspect_mem(cpu.d_mem), {})

    def test_slt_with_negative_smaller_second_operand_and_destination_is_not_operand(self):
        memory = {
            cpu.rf:    {t1: 0xffff_fffb, t2: 0xffff_fff9},
            cpu.i_mem: {0: 0x012A402A}
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        go.step({})
        expect_memory(go.inspect_mem(cpu.rf), {t0: 0, t1: 0xffff_fffb, t2: 0xffff_fff9})
        expect_memory(go.inspect_mem(cpu.d_mem), {})

### LW ###

class TestLoadWord:
    def test_lw_with_positive_offset_and_destination_is_not_operand(self):
        memory = {
            cpu.rf:    {t1: 6},
            cpu.d_mem: {10: 0xabcdeeee},
            cpu.i_mem: {0: 0x8D280004}
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        go.step({})
        expect_memory(go.inspect_mem(cpu.rf), {t0: 0xabcdeeee, t1: 6})
        expect_memory(go.inspect_mem(cpu.d_mem), {10: 0xabcdeeee})

    def test_lw_with_negative_offset_and_destination_is_not_operand(self):
        memory = {
            cpu.rf:    {t1: 6},
            cpu.d_mem: {2: 0xabcdeeee},
            cpu.i_mem: {0: 0x8D28FFFC}
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        go.step({})
        expect_memory(go.inspect_mem(cpu.rf), {t0: 0xabcdeeee, t1: 6})
        expect_memory(go.inspect_mem(cpu.d_mem), {2: 0xabcdeeee})

### SW ###

class TestStoreWord:
    def test_sw_with_negative_offset_and_destination_is_not_operand(self):
        memory = {
            cpu.rf:    {t0: 0xabcdeeee, t1: 6},
            cpu.i_mem: {0: 0xAD28FFFC}
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        go.step({})
        expect_memory(go.inspect_mem(cpu.rf), {t0: 0xabcdeeee, t1: 6})
        expect_memory(go.inspect_mem(cpu.d_mem), {2: 0xabcdeeee})

### BEQ ###

class TestBranchOnEqual:
    def test_beq_with_negative_offset_and_skipped_branch(self):
        memory = {
            cpu.rf:    {t0: 5, t1: 6},
            cpu.i_mem: {0: 0x1109FFFC}
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 3},
            memory_value_map = memory
        )
        
        go.step({})
        go.step({})

        assert go.inspect('pc') == 4
        expect_memory(go.inspect_mem(cpu.rf), {t0: 5, t1: 6})

    def test_beq_with_negative_offset_and_taken_branch(self):
        memory = {
            cpu.rf:    {t0: 5, t1: 5},
            cpu.i_mem: {0: 0x1109FFFC}
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 3},
            memory_value_map = memory
        )
        
        go.step({})
        go.step({})

        assert go.inspect('pc') == 4
        expect_memory(go.inspect_mem(cpu.rf), {t0: 5, t1: 5})

### Programs ###

class TestConsecutiveInstructions:
    def test_instructor_sample_test(self):
        memory = {
            cpu.i_mem: {
                0: 0x01004024, 1: 0x01204824, 2: 0x2129000a, 3: 0x11090006,
                4: 0x01405024, 5: 0x8d4b0000, 6: 0x216b0001, 7: 0xad4b0000,
                8: 0x21080001, 9: 0x1000fff9, 10: 0x8c020000, 11: 0x1042fffe
            }
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )

        for i in range(500):
            go.step({})
        
        expect_memory(go.inspect_mem(cpu.rf), {t0: 10, t1: 10, t2: 0, t3: 10, v0: 10})
        expect_memory(go.inspect_mem(cpu.d_mem), {0: 10})
    
    def test_lui_program(self):
        memory = {
            cpu.i_mem: {
                0: 0x3C08000A, 1: 0x3C090001, 2: 0x2129FF38, 3: 0x01405024,
                4: 0x01605824, 5: 0x200C0001, 6: 0x116C0003, 7: 0x01495020,
                8: 0x010A582A, 9: 0x1000FFFC, 10: 0x1000FFFF
            }
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )

        for i in range(500):
            go.step({})
        
        expect_memory(go.inspect_mem(cpu.rf), {t0: 655360, t1: 65336, t2: 718696, t3: 1, t4: 1})
