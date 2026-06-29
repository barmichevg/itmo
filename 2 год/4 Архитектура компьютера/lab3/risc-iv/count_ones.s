.data
input_addr:      .word  0x80
output_addr:     .word  0x84

.text
.org 0x90

_start:
    lui      sp, 0x1

    lui      t0, %hi(input_addr)
    addi     t0, t0, %lo(input_addr)
    lw       t1, 0(t0)
    lw       a0, 0(t1)

    jal      ra, count_ones

    lui      t0, %hi(output_addr)
    addi     t0, t0, %lo(output_addr)
    lw       t1, 0(t0)
    sw       a0, 0(t1)

    halt


count_ones:
    addi     sp, sp, -16
    sw       ra, 12(sp)
    sw       s0, 8(sp)
    sw       s1, 4(sp)
    sw       s2, 0(sp)

    mv       s0, a0
    addi     s1, zero, 0
    addi     s2, zero, 32

count_ones_loop:
    beqz     s2, count_ones_done

    mv       a0, s0
    jal      ra, count_ones_get_lsb
    add      s1, s1, a0

    mv       a0, s0
    jal      ra, count_ones_shift_right_1
    mv       s0, a0

    addi     s2, s2, -1
    j        count_ones_loop

count_ones_done:
    mv       a0, s1

    lw       s2, 0(sp)
    lw       s1, 4(sp)
    lw       s0, 8(sp)
    lw       ra, 12(sp)
    addi     sp, sp, 16
    jr       ra


count_ones_get_lsb:
    addi     t0, zero, 1
    and      a0, a0, t0
    jr       ra


count_ones_shift_right_1:
    addi     t0, zero, 1
    srl      a0, a0, t0
    jr       ra