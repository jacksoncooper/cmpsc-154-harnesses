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
                1: 0x012A4020, # add $t0, $t1, $t2
                2: 0x01095820, # add $t3, $t0, $t1
            }
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        for cycle in range(7):
            go.step({})

        expect_memory(go.inspect_mem(cpu.rf), {t0: 12, t1: 7, t2: 5, t3: 19})

    def test_type_one_b_hazard(self):
        memory = {
            cpu.rf:    {t1: 7, t2: 5},
            cpu.i_mem: {
                1: 0x012A4020, # add $t0, $t1, $t2
                2: 0x01285820, # add $t3, $t1, $t0
            }
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        for cycle in range(7):
            go.step({})

        expect_memory(go.inspect_mem(cpu.rf), {t0: 12, t1: 7, t2: 5, t3: 19})

    def test_type_one_a_and_one_b_hazard(self):
        memory = {
            cpu.rf:    {t1: 7, t2: 5},
            cpu.i_mem: {
                1: 0x012A4020, # add $t0, $t1, $t2
                2: 0x01085820, # add $t3, $t0, $t0
            }
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        for cycle in range(7):
            go.step({})

        expect_memory(go.inspect_mem(cpu.rf), {t0: 12, t1: 7, t2: 5, t3: 24})

    def test_type_one_a_hazard_with_zero_forward(self):
        memory = {
            cpu.rf:    {t1: 7, t2: 5},
            cpu.i_mem: {
                1: 0x012A0020, # add $zero, $t1, $t2
                2: 0x00095820, # add $t3, $zero, $t1
            }
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        for cycle in range(7):
            go.step({})

        expect_memory(go.inspect_mem(cpu.rf), {t1: 7, t2: 5, t3: 7})

    def test_type_one_b_hazard_with_zero_forward(self):
        memory = {
            cpu.rf:    {t1: 7, t2: 5},
            cpu.i_mem: {
                1: 0x01205820, # add $zero, $t1, $t2
                2: 0x00095820, # add $t3, $t1, $zero
            }
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        for cycle in range(7):
            go.step({})

        expect_memory(go.inspect_mem(cpu.rf), {t1: 7, t2: 5, t3: 7})

    def test_type_one_a_hazard_with_forward_to_type_immediate(self):
        memory = {
            cpu.rf:    {t1: 7, t2: 5},
            cpu.i_mem: {
                1: 0x012A4020, # add $t0, $t1, $t2
                2: 0x210B0005, # addi $t3, $t0, 5
            }
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        for cycle in range(7):
            go.step({})

        expect_memory(go.inspect_mem(cpu.rf), {t0: 12, t1: 7, t2: 5, t3: 17})

    def test_type_one_a_hazard_with_zero_forward_and_forward_to_type_immediate(self):
        memory = {
            cpu.rf:    {t1: 7, t2: 5},
            cpu.i_mem: {
                1: 0x012A0020, # add $zero, $t1, $t2
                2: 0x200B0005, # addi $t3, $zero, 5
            }
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        for cycle in range(7):
            go.step({})

        expect_memory(go.inspect_mem(cpu.rf), {t1: 7, t2: 5, t3: 5})

    def test_do_not_forward_without_register_write(self):
        # Not sure how to test, because SW and BEQ do not change their operands,
        # and so forwarding from `rs` and `rt` is benign.
        pass

    def test_type_one_a_hazard_with_forward_from_immediate(self):
        memory = {
            cpu.rf:    {t1: 5},
            cpu.i_mem: {
                1: 0x34080007, # ori $t0, $zero, 7
                2: 0x01094020, # add $t0, $t0, $t1
            }
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        for cycle in range(7):
            go.step({})

        expect_memory(go.inspect_mem(cpu.rf), {t0: 12, t1: 5})

    def test_type_one_a_hazard_with_zero_forward_and_forward_from_immediate(self):
        memory = {
            cpu.rf:    {t1: 5},
            cpu.i_mem: {
                1: 0x34000007, # ori $zero, $zero, 7
                2: 0x00094020, # add $t0, $zero, $t1
            }
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        for cycle in range(7):
            go.step({})

        expect_memory(go.inspect_mem(cpu.rf), {t0: 5, t1: 5})

    def test_type_one_a_hazard_with_forward_to_immediate_and_forward_from_immediate(self):
        memory = {
            cpu.rf:    {t1: 5},
            cpu.i_mem: {
                1: 0x35280008, # ori $t0, $t1, 8
                2: 0x21080000, # addi $t0, $t0, 0
            }
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        for cycle in range(7):
            go.step({})

        expect_memory(go.inspect_mem(cpu.rf), {t0: 13, t1: 5})

    def test_load_word_does_not_forward_from_execute_memory(self):
        memory = {
            cpu.rf:    {t1: 28},
            cpu.d_mem: {28: 0xaabbccdd},
            cpu.i_mem: {
                1: 0x8D280000, # lw $t0, 0($t1)
                2: 0x01094020, # add $t0, $t0, $t1
            }
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        for cycle in range(7):
            go.step({})

        expect_memory(go.inspect_mem(cpu.rf), {t0: 0xaabbccf9, t1: 28})

    def test_forward_does_not_clobber_immediate(self):
        # Trying to test if the immediate multiplexer is in the right place.

        memory = {
            cpu.rf:    {t1: 6},
            cpu.i_mem: {
                1: 0x35280001, # ori $t0, $t1, 1
                2: 0x20080009, # addi $t0, $zero, 9
            }
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        for cycle in range(7):
            go.step({})

        expect_memory(go.inspect_mem(cpu.rf), {t0: 9, t1: 6})

class TestMemoryHazard:
    def test_type_two_a_hazard(self):
        memory = {
            cpu.rf:    {t1: 7, t2: 5},
            cpu.i_mem: {
                1: 0x012A4024, # and $t0, $t1, $t2
                2: 0x00000020, # no-op: add $zero $zero $zero
                3: 0x01005820, # add $t3, $t0, $zero
            }
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        for cycle in range(8):
            go.step({})

        expect_memory(go.inspect_mem(cpu.rf), {t0: 5, t1: 7, t2: 5, t3: 5})

    def test_type_two_b_hazard(self):
        memory = {
            cpu.rf:    {t1: 7, t2: 5},
            cpu.i_mem: {
                1: 0x012A4024, # and $t0, $t1, $t2
                2: 0x00000020, # no-op: add $zero $zero $zero
                3: 0x00085820, # add $t3, $zero, $t0
            }
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        for cycle in range(8):
            go.step({})

        expect_memory(go.inspect_mem(cpu.rf), {t0: 5, t1: 7, t2: 5, t3: 5})

    def test_type_two_a_and_two_b_hazard(self):
        memory = {
            cpu.rf:    {t1: 7, t2: 5},
            cpu.i_mem: {
                1: 0x012A4024, # and $t0, $t1, $t2
                2: 0x00000020, # no-op: add $zero $zero $zero
                3: 0x01085820, # add $t3, $t0, $t0
            }
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        for cycle in range(8):
            go.step({})

        expect_memory(go.inspect_mem(cpu.rf), {t0: 5, t1: 7, t2: 5, t3: 10})

    def test_type_two_a_hazard_with_zero_forward(self):
        memory = {
            cpu.rf:    {t1: 7, t2: 5},
            cpu.i_mem: {
                1: 0x012A0024, # and $zero, $t1, $t2
                2: 0x00000020, # no-op: add $zero $zero $zero
                3: 0x00085820, # add $t3, $zero, $t0
            }
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        for cycle in range(8):
            go.step({})

        expect_memory(go.inspect_mem(cpu.rf), {t1: 7, t2: 5, t3: 0})

    def test_type_two_b_hazard_with_zero_forward(self):
        memory = {
            cpu.rf:    {t1: 7, t2: 5},
            cpu.i_mem: {
                1: 0x012A0024, # and $zero, $t1, $t2
                2: 0x00000020, # no-op: add $zero $zero $zero
                3: 0x01005820, # add $t3, $t0, $zero
            }
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        for cycle in range(8):
            go.step({})

        expect_memory(go.inspect_mem(cpu.rf), {t1: 7, t2: 5, t3: 0})

    def test_type_two_a_hazard_with_forward_to_immediate(self):
        memory = {
            cpu.rf:    {t1: 7, t2: 5},
            cpu.i_mem: {
                1: 0x012A4020, # add $t0, $t1, $t2
                2: 0x00000020, # no-op: add $zero $zero $zero
                3: 0x210B0009, # addi $t3, $t0, 9
            }
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        for cycle in range(8):
            go.step({})

        expect_memory(go.inspect_mem(cpu.rf), {t0: 12, t1: 7, t2: 5, t3: 21})

    def test_do_not_forward_without_register_write(self):
        # Not sure how to test, because SW and BEQ do not change their operands,
        # and so forwarding from `rs` and `rt` is benign.
        pass

    def test_forward_from_execute_memory_takes_priority(self):
        memory = {
            cpu.rf:    {t1: 7, t2: 5},
            cpu.i_mem: {
                1: 0x012A4020, # add $t0, $t1, $t2
                2: 0x01094020, # add $t0, $t0, $t1
                3: 0x01094020, # add $t0, $t0, $t1
            }
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        for cycle in range(8):
            go.step({})

        expect_memory(go.inspect_mem(cpu.rf), {t0: 26, t1: 7, t2: 5})

    def test_type_one_a_hazard_and_two_b_hazard(self):
        memory = {
            cpu.rf:    {t3: 9, t4: 7},
            cpu.i_mem: {
                1: 0x000B4020, # add $t0, $zero, $t3
                2: 0x000C4820, # add $t1, $zero, $t4
                3: 0x01285020, # add $t2, $t1, $t0
            }
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        for cycle in range(8):
            go.step({})

        expect_memory(go.inspect_mem(cpu.rf), {t0: 9, t1: 7, t2: 16, t3: 9, t4: 7})

    def test_type_one_b_hazard_and_two_a_hazard(self):
        memory = {
            cpu.rf:    {t3: 9, t4: 7},
            cpu.i_mem: {
                1: 0x000B4020, # add $t0, $zero, $t3
                2: 0x000C4820, # add $t1, $zero, $t4
                3: 0x01095020, # add $t2, $t0, $t1
            }
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        for cycle in range(8):
            go.step({})

        expect_memory(go.inspect_mem(cpu.rf), {t0: 9, t1: 7, t2: 16, t3: 9, t4: 7})

    def test_load_stall_and_type_two_a_hazard(self):
        memory = {
            cpu.rf:    {t0: 48, t3: 8},
            cpu.d_mem: {48: 42},
            cpu.i_mem: {
                1: 0x8D090000, # lw $t1, 0($t0)
                2: 0x012B5020, # add $t2, $t1, $t3
            }
        }

        go = rtl.Simulation(
            register_value_map = {cpu.pc: 0},
            memory_value_map = memory
        )
        
        for cycle in range(7):
            go.step({})

        expect_memory(go.inspect_mem(cpu.rf), {t0: 48, t1: 42, t2: 50, t3: 8})

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
            memory_value_map = memory
        )

        for i in range(500):
            go.step({})
        
        expect_memory(go.inspect_mem(cpu.rf), {t0: 655360, t1: 65336, t2: 718696, t3: 1, t4: 1})

    def test_all_consecutive_with_bad_host(self):
        memory = {
            cpu.rf: {a3: 1024},
            cpu.d_mem: {1024: 16, 1028: 0x1234002b},
            cpu.i_mem: {
                0: 0x8ce80000, 1: 0x21080001, 2: 0x01204820, 3: 0x00005020,
                4: 0x200b0020, 5: 0x00006020, 6: 0x218c0001, 7: 0x0168502a,
                8: 0x114c0004, 9: 0x01294820, 10: 0x21290001, 11: 0x21080001,
                12: 0x1000fffa, 13: 0x8ced0004, 14: 0x012d7024, 15: 0x21ef002a,
                16: 0x11cf0001, 17: 0x10000004, 18: 0x00004020, 19: 0x3c086f79,
                20: 0x35086573, 21: 0x10000003, 22: 0x00004020, 23: 0x3c086f68,
                24: 0x35086e6f, 25: 0xace80008, 26: 0x1000ffff
            }
        }

        go = rtl.Simulation(
            memory_value_map = memory
        )

        for i in range(500):
            go.step({})
        
        expect_memory(go.inspect_mem(cpu.rf), {
            t0: 0x6f686e6f, t1: 0x0000ffff, t2: 1, t3: 32, t4: 1,
            t5: 0x1234002b, t6: 43, t7: 42,
            a3: 1024
        })

        expect_memory(go.inspect_mem(cpu.d_mem), {
            1024: 16, 1028: 0x1234002b, 1032: 0x6f686e6f
        })

    def test_all_consecutive_with_good_host(self):
        memory = {
            cpu.rf: {a3: 1024},
            cpu.d_mem: {1024: 16, 1028: 0x1234002a},
            cpu.i_mem: {
                0: 0x8ce80000, 1: 0x21080001, 2: 0x01204820, 3: 0x00005020,
                4: 0x200b0020, 5: 0x00006020, 6: 0x218c0001, 7: 0x0168502a,
                8: 0x114c0004, 9: 0x01294820, 10: 0x21290001, 11: 0x21080001,
                12: 0x1000fffa, 13: 0x8ced0004, 14: 0x012d7024, 15: 0x21ef002a,
                16: 0x11cf0001, 17: 0x10000004, 18: 0x00004020, 19: 0x3c086f79,
                20: 0x35086573, 21: 0x10000003, 22: 0x00004020, 23: 0x3c086f68,
                24: 0x35086e6f, 25: 0xace80008, 26: 0x1000ffff
            }
        }

        go = rtl.Simulation(
            memory_value_map = memory
        )

        for i in range(500):
            go.step({})
        
        expect_memory(go.inspect_mem(cpu.rf), {
            t0: 0x6f796573, t1: 0x0000ffff, t2: 1, t3: 32, t4: 1,
            t5: 0x1234002a, t6: 42, t7: 42,
            a3: 1024
        })

        expect_memory(go.inspect_mem(cpu.d_mem), {
            1024: 16, 1028: 0x1234002a, 1032: 0x6f796573
        })

