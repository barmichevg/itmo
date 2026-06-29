.data
input_addr:      .word  0x80
output_addr:     .word  0x84

n_var:           .word  0
total:           .word  0
ten:             .word  10
overflow_value:  .word  0xCCCCCCCC

.text
.org 0x90

_start:
    @p input_addr b!
    @b

    abs32
    sum_digits

    @p output_addr b!
    !b
    halt


abs32:
    dup
    -if abs_nonnegative

    inv lit 1 +

    dup
    -if abs_done

    drop
    @p output_addr b!
    @p overflow_value
    !b
    halt

abs_nonnegative:
abs_done:
    ;


sum_digits:
    !p n_var
    lit 0
    !p total

sum_loop:
    @p n_var
    if sum_finish

    @p n_var
    divide10

    !p n_var

    @p total
    +
    !p total

    sum_loop ;

sum_finish:
    @p total
    ;


divide10:
    a!
    lit ten
    b!

    lit 0
    lit 0

    lit 31 >r
divide10_loop:
    +/
    next divide10_loop
    ;