# Written by github.com/jacksoncooper.

# Distinguishes the host in a network given:

#  - The size of the subnet mask at 0($a3).
#  - An Internet address at 4($a3).

# Tells you if the host is number 42 in ASCII in 8($a3).

.text

main:
    # add $a0, $zero, $zero        # For testing before loading to the CPU.
    # add $a1, $zero, $zero        # 18.52.0.0/16
                                   #   ^       ^
                                   #  $a1     $a0
    # addi $a0, $a0, 16

    # lui $a1, 0x1234
    # addi $a1, 0x002a

    # add $a3, $zero, $sp

    # sw $a0, 0($a3)
    # sw $a1, 4($a3)

    # ---

    lw $t0, 0($a3)               # $t0 := The length of the subnet mask, the fill index.
    addi $t0, $t0, 1
    add $t1, $t1, $zero          # $t1 := The subnet mask to be made.
    add $t2, $zero, $zero        # $t2 := The fill flag.
    addi $t3, $zero, 32          # $t3 := The bitwidth of an IPv4 address.
    add $t4, $zero, $zero        # $t4 := The constant 1.
    addi $t4, $t4, 1

fill_ones:
    slt $t2, $t3, $t0
    beq $t2, $t4, done_fill_ones

    add $t1, $t1, $t1            # Shift the subnet mask left and add one.
    addi $t1, $t1, 1

    addi $t0, $t0, 1
    beq $zero, $zero, fill_ones
done_fill_ones:

lw $t5, 4($a3)                   # $t5 := The Internet address from memory.
and $t6, $t1, $t5                # $t6 := The host number.

addi $t7, $t7, 42                # t7 := The expected host.
beq $t6, $t7, host_is_forty_two
beq $zero, $zero, host_is_not_forty_two

host_is_forty_two: 
    add $t0, $zero, $zero        # 0x6f796573 (ASCII oyes) for success.
    lui $t0, 0x6f79
    ori $t0, $t0, 0x6573
beq $zero, $zero, write_ascii

host_is_not_forty_two:
    add $t0, $zero, $zero        # 0x6f686e6f (ASCII ohno) for failure.
    lui $t0, 0x6f68
    ori $t0, $t0, 0x6e6f

write_ascii:
    sw $t0, 8($a3)               # t0 := Exhausted temporaries, use t0 for out.

exit:
    beq $zero, $zero, exit
