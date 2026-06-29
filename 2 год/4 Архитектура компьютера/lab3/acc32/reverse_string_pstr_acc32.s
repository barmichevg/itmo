    .data
    .org             0x23
len_ptr:          .word  0x00
start_input_ptr:  .word  0x1F
buffer_ptr:       .word  0x01
start_ptr:        .word  0x1F
input_addr:       .word  0x80
output_addr:      .word  0x84
const_1:          .word  0x01
const_4:          .word  0x04
stop_letter:      .word  0x0A
maskFF:           .word  0x000000FF
mask00:           .word  0xFFFFFF00
str_len:          .word  0x00
temp:             .word  0x00

    .text
    .org             0x90
_start:

read_cycle:
    load           input_addr
    load_acc

    sub            stop_letter
    beqz           calc_len
    add            stop_letter

    store          temp

    load           start_input_ptr
    beqz           over

    load           start_input_ptr
    load_acc
    and            mask00
    or             temp
    store_ind      start_input_ptr

    load           start_input_ptr
    sub            const_1
    store          start_input_ptr

    jmp            read_cycle


calc_len:
    load           start_ptr
    sub            start_input_ptr
    store          str_len

copy_and_out:
    load           start_input_ptr
    sub            start_ptr
    beqz           write_len

    load           start_input_ptr
    add            const_1
    store          start_input_ptr

    load           start_input_ptr
    load_acc
    and            maskFF
    store          temp

    store_ind      output_addr

    load           buffer_ptr
    load_acc
    and            mask00
    or             temp
    store_ind      buffer_ptr

    load           buffer_ptr
    add            const_1
    store          buffer_ptr

    jmp            copy_and_out


write_len:
    load           str_len
    store          temp

    load           len_ptr
    load_acc
    and            mask00
    or             temp
    store_ind      len_ptr

fill_tail:
    load           buffer_ptr
    sub            start_ptr
    bgt            end

    load_imm       0x5f5f5f5f
    store_ind      buffer_ptr

    load           buffer_ptr
    add            const_4
    store          buffer_ptr

    jmp            fill_tail


over:
    load_imm       0xCCCCCCCC
    store_ind      output_addr

end:
    halt