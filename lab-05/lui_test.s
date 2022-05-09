

.text

main:
    lui $t0, 10             #t0 = 655360
    lui $t1, 1              #t1 = 65536
    addi $t1, $t1, -200      #t1 = 65336
    and $t2, $t2, $zero     #t2 = 0
    and $t3, $t3, $zero     #t3 = 0
    addi $t4, $zero, 1      #t4 = 1

loop:
    beq $t3, $t4, exit

    add $t2, $t2, $t1       #t2 = t2 + t1
    slt $t3, $t0, $t2

    beq $zero, $zero, loop

exit:
    beq $zero, $zero, exit
