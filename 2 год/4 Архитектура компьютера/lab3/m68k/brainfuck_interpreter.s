.data
input_addr:      .word 0x80
output_addr:     .word 0x84

memory_size:     .word 0x1000
code_len:        .word 0

.org 0x90
code_buf:        .word 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
bracket_table:   .word 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
cells:           .word 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0

.text
.org 0x300

_start:
    movea.l memory_size, A7         ; A7 = вершина стека
    movea.l (A7), A7

    movea.l input_addr, A0          ; A0 = адрес входного порта
    movea.l (A0), A0

    movea.l output_addr, A1         ; A1 = адрес выходного порта
    movea.l (A1), A1

    movea.l code_buf, A2            ; A2 = адрес буфера программы
    movea.l cells, A3               ; A3 = адрес массива ячеек
    movea.l bracket_table, A5       ; A5 = таблица парных скобок

    jsr read_program_line
    jsr run_program

    halt


read_program_line:
    link A6, -4
    clr.l D3                        ; D3 = длина программы
    clr.l -4(A6)                    ; -4(A6) = баланс скобок

read_program_line_loop:         ; цикл чтения программы
    cmp.l 64, D3
    bge overflow_handler

    clr.l D0
    move.b (A0), D0                 ; D0 = текущий байт

    cmp.b 10, D0
    beq read_program_line_done      ; проверка строка программы закончилась '\n'

    cmp.b '[', D0
    beq read_store_open             ; если '['

    cmp.b ']', D0
    beq read_store_close            ; если ']'

    move.b D0, 0(A2,D3)
    add.l 1, D3
    jmp read_program_line_loop      ; остальные символы сохраняем в буфер.

read_store_open:                ; обработка '['
    move.l D3, -(A7)
    move.l -4(A6), D6
    add.l 1, D6
    move.l D6, -4(A6)
    move.b D0, 0(A2,D3)
    add.l 1, D3
    jmp read_program_line_loop

read_store_close:               ; обработка ']'
    move.l -4(A6), D6
    sub.l 1, D6
    move.l D6, -4(A6)
    bmi read_error_drain
    move.l (A7)+, D7
    move.b D0, 0(A2,D3)
    move.b D3, 0(A5,D7)
    move.b D7, 0(A5,D3)
    add.l 1, D3
    jmp read_program_line_loop

read_program_line_done:         ; завершает чтение строки
    move.l -4(A6), D6
    cmp.l 0, D6
    bne error_handler
    movea.l code_len, A4
    move.l D3, (A4)
    unlk A6
    rts


read_error_drain:               ; если ошибка найдена во время чтения, дочитывает остаток строки до \n
    clr.l D0

read_error_drain_loop:
    move.b (A0), D0
    cmp.b 10, D0
    bne read_error_drain_loop
    jmp error_handler


run_program:
    clr.l D1                        ; D1 = указатель на текущую команду
    clr.l D2                        ; D2 = указатель на текущую ячейку

run_loop:                       ; Берёт команду из code_buf и передаёт обработчику
    cmp.l D3, D1
    bge run_done

    clr.l D0
    move.b 0(A2,D1), D0             ; D0 = текущая команда

    cmp.b '+', D0
    beq cmd_plus
    cmp.b '-', D0
    beq cmd_minus
    cmp.b '>', D0
    beq cmd_right
    cmp.b '<', D0
    beq cmd_left
    cmp.b '.', D0
    beq cmd_dot
    cmp.b ',', D0
    beq cmd_comma
    cmp.b '[', D0
    beq cmd_lbracket
    cmp.b ']', D0
    beq cmd_rbracket

    jmp error_handler


cmd_right:                      ; '>' - сдвинуть указатель данных вправо
    add.l 4, D2
    cmp.l 120, D2
    bge error_handler
    jmp run_next

cmd_left:                       ; '<' - сдвинуть указатель данных влево
    sub.l 4, D2
    bmi error_handler
    jmp run_next

cmd_plus:                       ; '+' - увеличить текущую 32-битную ячейку на 1
    move.l 0(A3,D2), D4
    add.l 1, D4
    bvs overflow_handler
    move.l D4, 0(A3,D2)
    jmp run_next

cmd_minus:                      ; '-' - уменьшить текущую 32-битную ячейку на 1
    move.l 0(A3,D2), D4
    sub.l 1, D4
    bvs overflow_handler
    move.l D4, 0(A3,D2)
    jmp run_next

cmd_dot:                        ; '.' - вывести младший байт текущей ячейки
    move.l 0(A3,D2), D4
    move.b D4, (A1)
    jmp run_next

cmd_comma:                      ; ',' - прочитать байт из входа и записать его в младший байт текущей ячейки
    move.l 0(A3,D2), D4
    and.l 0xFFFFFF00, D4
    clr.l D0
    move.b (A0), D0
    and.l 0x000000FF, D0
    or.l D0, D4
    move.l D4, 0(A3,D2)
    jmp run_next

cmd_lbracket:                   ; '[' - если текущая ячейка == 0, перепрыгнуть к парной ']'
    move.l 0(A3,D2), D4
    cmp.l 0, D4
    bne run_next

    clr.l D7
    move.b 0(A5,D1), D7
    move.l D7, D1
    jmp run_next

cmd_rbracket:                   ; ']' - если текущая ячейка != 0, прыгнуть назад к парной '['
    move.l 0(A3,D2), D4
    cmp.l 0, D4
    beq run_next

    clr.l D7
    move.b 0(A5,D1), D7
    move.l D7, D1
    jmp run_next

run_next:
    add.l 1, D1
    jmp run_loop

run_done:
    rts


error_handler:                  ; обработчик ошибок
    move.l -1, D0
    move.l D0, (A1)
    halt

overflow_handler:               ; обработчик переполнения
    move.l 0xCCCCCCCC, D0
    move.l D0, (A1)
    halt