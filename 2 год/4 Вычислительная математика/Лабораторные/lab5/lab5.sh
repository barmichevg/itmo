#!/usr/bin/env bash

set -u
export LC_NUMERIC=C
export BC_LINE_LENGTH=0

SCALE=16
EPS="0.000001"
N=0
HAS_FUNCTION=0
FUNCTION_ID=0
FUNCTION_GNUPLOT=""

X=()
Y=()

declare -A D

bc_calc() {
    echo "scale=$SCALE; $*" | bc -l
}

bc_bool() {
    echo "$*" | bc -l
}

normalize_number() {
    echo "${1/,/.}"
}

is_number() {
    [[ "$1" =~ ^[-+]?[0-9]+([.][0-9]+)?$ || "$1" =~ ^[-+]?[.][0-9]+$ ]]
}

fact() {
    local n=$1
    local r=1
    local i
    for ((i=2; i<=n; i++)); do
        r=$((r * i))
    done
    echo "$r"
}

pause() {
    echo
    read -r -p "Нажмите Enter, чтобы продолжить..." _
}

check_dependencies() {
    local ok=1
    command -v bc >/dev/null 2>&1 || { echo "Не найден GNU bc."; ok=0; }
    command -v gnuplot >/dev/null 2>&1 || { echo "Не найден gnuplot."; }
    [[ $ok -eq 1 ]] || exit 1
}

clear_data() {
    X=()
    Y=()
    D=()
    N=0
    HAS_FUNCTION=0
    FUNCTION_ID=0
    FUNCTION_GNUPLOT=""
}

validate_data() {
    if (( N < 2 )); then
        echo "Ошибка: нужно минимум 2 точки."
        return 1
    fi

    local i cmp
    for ((i=1; i<N; i++)); do
        cmp=$(bc_bool "${X[$i]} > ${X[$((i-1))]}")
        if [[ "$cmp" != "1" ]]; then
            echo "Ошибка: значения x должны идти строго по возрастанию и не повторяться."
            return 1
        fi
    done
    return 0
}

is_uniform_grid() {
    if (( N < 2 )); then
        return 1
    fi

    local h curr err ok i
    h=$(bc_calc "${X[1]} - ${X[0]}")
    for ((i=2; i<N; i++)); do
        curr=$(bc_calc "${X[$i]} - ${X[$((i-1))]}")
        err=$(bc_calc "if (($curr - $h) < 0) -($curr - $h) else ($curr - $h)")
        ok=$(bc_bool "$err <= $EPS")
        if [[ "$ok" != "1" ]]; then
            return 1
        fi
    done
    return 0
}

read_keyboard() {
    clear_data
    local n xi yi i
    read -r -p "Введите количество точек: " n
    if ! [[ "$n" =~ ^[0-9]+$ ]]; then
        echo "Ошибка: количество точек должно быть целым числом."
        return 1
    fi

    N=$n
    echo "Введите пары x y через пробел:"
    for ((i=0; i<N; i++)); do
        read -r -p "[$i] x y: " xi yi
        xi=$(normalize_number "$xi")
        yi=$(normalize_number "$yi")
        if ! is_number "$xi" || ! is_number "$yi"; then
            echo "Ошибка: x и y должны быть числами."
            return 1
        fi
        X[$i]="$xi"
        Y[$i]="$yi"
    done

    validate_data
}

read_file_data() {
    clear_data
    local path line xi yi
    read -r -p "Введите путь к .txt файлу: " path
    if [[ ! -f "$path" ]]; then
        echo "Ошибка: файл не найден."
        return 1
    fi

    while read -r line || [[ -n "$line" ]]; do
        line="${line%%#*}"
        [[ -z "${line// /}" ]] && continue
        read -r xi yi _ <<< "$line"
        xi=$(normalize_number "$xi")
        yi=$(normalize_number "$yi")
        if ! is_number "$xi" || ! is_number "$yi"; then
            echo "Ошибка в строке файла: $line"
            return 1
        fi
        X[$N]="$xi"
        Y[$N]="$yi"
        N=$((N + 1))
    done < "$path"

    validate_data
}

eval_function() {
    local x=$1
    case "$FUNCTION_ID" in
        1) bc_calc "s($x)" ;;
        2) bc_calc "c($x)" ;;
        3) bc_calc "$x * $x + 2 * $x + 1" ;;
        4) bc_calc "e($x)" ;;
        5) bc_calc "l($x)" ;;
        6) bc_calc "sqrt($x)" ;;
        7) bc_calc "$x / (1 + $x * $x)" ;;
        *) echo "0" ;;
    esac
}

generate_by_function() {
    clear_data
    local a b n h xi yi i
    echo "Выберите функцию:"
    echo "1) sin(x)"
    echo "2) cos(x)"
    echo "3) x^2 + 2*x + 1"
    echo "4) exp(x)"
    echo "5) log(x)"
    echo "6) sqrt(x)"
    echo "7) x / (1 + x^2)"
    read -r -p "Номер функции: " FUNCTION_ID

    case "$FUNCTION_ID" in
        1) FUNCTION_GNUPLOT="sin(x)" ;;
        2) FUNCTION_GNUPLOT="cos(x)" ;;
        3) FUNCTION_GNUPLOT="x**2 + 2*x + 1" ;;
        4) FUNCTION_GNUPLOT="exp(x)" ;;
        5) FUNCTION_GNUPLOT="log(x)" ;;
        6) FUNCTION_GNUPLOT="sqrt(x)" ;;
        7) FUNCTION_GNUPLOT="x / (1 + x**2)" ;;
        *) echo "Ошибка: такой функции нет."; return 1 ;;
    esac

    read -r -p "Введите начало интервала a: " a
    read -r -p "Введите конец интервала b: " b
    read -r -p "Введите количество точек n: " n
    a=$(normalize_number "$a")
    b=$(normalize_number "$b")

    if ! is_number "$a" || ! is_number "$b" || ! [[ "$n" =~ ^[0-9]+$ ]] || (( n < 2 )); then
        echo "Ошибка: некорректные параметры."
        return 1
    fi

    if [[ "$(bc_bool "$b > $a")" != "1" ]]; then
        echo "Ошибка: должно быть b > a."
        return 1
    fi

    if [[ "$FUNCTION_ID" == "5" && "$(bc_bool "$a > 0")" != "1" ]]; then
        echo "Ошибка: для log(x) интервал должен быть больше 0."
        return 1
    fi

    if [[ "$FUNCTION_ID" == "6" && "$(bc_bool "$a >= 0")" != "1" ]]; then
        echo "Ошибка: для sqrt(x) интервал должен быть неотрицательным."
        return 1
    fi

    N=$n
    HAS_FUNCTION=1
    h=$(bc_calc "($b - $a) / ($N - 1)")
    for ((i=0; i<N; i++)); do
        xi=$(bc_calc "$a + $h * $i")
        yi=$(eval_function "$xi")
        X[$i]="$xi"
        Y[$i]="$yi"
    done

    validate_data
}

build_differences() {
    local i k last val
    D=()
    for ((i=0; i<N; i++)); do
        D["0,$i"]="${Y[$i]}"
    done

    for ((k=1; k<N; k++)); do
        last=$((N - k))
        for ((i=0; i<last; i++)); do
            val=$(bc_calc "${D["$((k-1)),$((i+1))"]} - ${D["$((k-1)),$i"]}")
            D["$k,$i"]="$val"
        done
    done
}

print_source_table() {
    local i
    echo
    echo "Исходная таблица:"
    printf "%4s %15s %15s\n" "i" "x_i" "y_i"
    for ((i=0; i<N; i++)); do
        printf "%4d %15.10f %15.10f\n" "$i" "${X[$i]}" "${Y[$i]}"
    done
}

print_difference_table() {
    local i k
    echo
    echo "Таблица конечных разностей:"
    printf "%4s %12s %12s" "i" "x_i" "y_i"
    for ((k=1; k<N; k++)); do
        printf " %12s" "Δ^$k y"
    done
    echo

    for ((i=0; i<N; i++)); do
        printf "%4d %12.6f %12.6f" "$i" "${X[$i]}" "${D["0,$i"]}"
        for ((k=1; k<N; k++)); do
            if [[ -n "${D["$k,$i"]+x}" ]]; then
                printf " %12.6f" "${D["$k,$i"]}"
            else
                printf " %12s" ""
            fi
        done
        echo
    done
}

lagrange_eval() {
    local x=$1
    local res="0"
    local term factor i j

    for ((i=0; i<N; i++)); do
        term="${Y[$i]}"
        for ((j=0; j<N; j++)); do
            if (( i != j )); then
                factor=$(bc_calc "($x - ${X[$j]}) / (${X[$i]} - ${X[$j]})")
                term=$(bc_calc "$term * $factor")
            fi
        done
        res=$(bc_calc "$res + $term")
    done

    echo "$res"
}

newton_eval() {
    local x=$1

    if ! is_uniform_grid; then
        echo "nan"
        return 1
    fi

    local h mid use_forward t res prod term k idx
    h=$(bc_calc "${X[1]} - ${X[0]}")
    mid=$(bc_calc "(${X[0]} + ${X[$((N-1))]}) / 2")
    use_forward=$(bc_bool "$x <= $mid")

    if [[ "$use_forward" == "1" ]]; then
        t=$(bc_calc "($x - ${X[0]}) / $h")
        res="${Y[0]}"
        prod="1"
        for ((k=1; k<N; k++)); do
            prod=$(bc_calc "$prod * ($t - ($k - 1))")
            term=$(bc_calc "$prod / $(fact "$k") * ${D["$k,0"]}")
            res=$(bc_calc "$res + $term")
        done
        echo "$res"
    else
        idx=$((N - 1))
        t=$(bc_calc "($x - ${X[$idx]}) / $h")
        res="${Y[$idx]}"
        prod="1"
        for ((k=1; k<N; k++)); do
            prod=$(bc_calc "$prod * ($t + ($k - 1))")
            term=$(bc_calc "$prod / $(fact "$k") * ${D["$k,$((N-k-1))"]}")
            res=$(bc_calc "$res + $term")
        done
        echo "$res"
    fi
}

gauss_eval() {
    local x=$1

    if ! is_uniform_grid; then
        echo "nan"
        return 1
    fi

    local h center t res direction k idx min_off max_off off prod term
    h=$(bc_calc "${X[1]} - ${X[0]}")
    center=$((N / 2))
    t=$(bc_calc "($x - ${X[$center]}) / $h")
    res="${Y[$center]}"

    if [[ "$(bc_bool "$t >= 0")" == "1" ]]; then
        direction="forward"
    else
        direction="backward"
    fi

    for ((k=1; k<N; k++)); do
        prod="1"

        if [[ "$direction" == "forward" ]]; then
            idx=$((center - k / 2))
            min_off=$((-(k / 2)))
            max_off=$(((k + 1) / 2 - 1))
        else
            idx=$((center - (k + 1) / 2))
            min_off=$((-((k - 1) / 2)))
            max_off=$((k / 2))
        fi

        if (( idx < 0 || idx > N - k - 1 )); then
            break
        fi

        for ((off=min_off; off<=max_off; off++)); do
            prod=$(bc_calc "$prod * ($t + ($off))")
        done

        term=$(bc_calc "$prod / $(fact "$k") * ${D["$k,$idx"]}")
        res=$(bc_calc "$res + $term")
    done

    echo "$res"
}

lagrange_gnuplot_expr() {
    local expr=""
    local i j term

    for ((i=0; i<N; i++)); do
        term="(${Y[$i]})"
        for ((j=0; j<N; j++)); do
            if (( i != j )); then
                term="$term*((x-(${X[$j]}))/((${X[$i]})-(${X[$j]})))"
            fi
        done

        if [[ -z "$expr" ]]; then
            expr="$term"
        else
            expr="$expr + $term"
        fi
    done

    echo "$expr"
}

write_input_file() {
    mkdir -p data plots
    local i

    : > data/input.txt
    for ((i=0; i<N; i++)); do
        printf "%s %s\n" "${X[$i]}" "${Y[$i]}" >> data/input.txt
    done
}

plot_graph() {
    if ! command -v gnuplot >/dev/null 2>&1; then
        echo "gnuplot не найден. График не построен."
        return 0
    fi

    write_input_file
    local poly_expr
    poly_expr=$(lagrange_gnuplot_expr)

    cat > data/plot_script.gp <<EOF_GP
set terminal pngcairo size 900,600 enhanced font 'Arial,11'
set output 'plots/plot.png'
set samples 80
set grid
set xlabel 'x'
set ylabel 'y'
set title 'Интерполяция функции'
set key left top
set xrange [${X[0]}:${X[$((N-1))]}]
p(x) = $poly_expr
EOF_GP

    if (( HAS_FUNCTION == 1 )); then
        cat >> data/plot_script.gp <<EOF_GP
f(x) = $FUNCTION_GNUPLOT
plot 'data/input.txt' using 1:2 with points pointtype 7 pointsize 1.3 title 'Узлы интерполяции', p(x) with lines linewidth 2 title 'Интерполяционный многочлен', f(x) with lines dashtype 2 linewidth 2 title 'Исходная функция'
EOF_GP
    else
        cat >> data/plot_script.gp <<EOF_GP
plot 'data/input.txt' using 1:2 with points pointtype 7 pointsize 1.3 title 'Узлы интерполяции', p(x) with lines linewidth 2 title 'Интерполяционный многочлен'
EOF_GP
    fi

    gnuplot data/plot_script.gp
    echo "График сохранён: plots/plot.png"
}

solve_current_data() {
    local xq lag new gauss dln dlg
    if ! validate_data; then
        return 1
    fi

    build_differences
    print_source_table
    print_difference_table

    read -r -p "Введите точку интерполяции X: " xq
    xq=$(normalize_number "$xq")
    if ! is_number "$xq"; then
        echo "Ошибка: X должен быть числом."
        return 1
    fi

    echo
    echo "Результаты:"
    lag=$(lagrange_eval "$xq")
    printf "Многочлен Лагранжа:                P(%s) = %.10f\n" "$xq" "$lag"

    if is_uniform_grid; then
        new=$(newton_eval "$xq")
        gauss=$(gauss_eval "$xq")
        printf "Ньютон с конечными разностями:     P(%s) = %.10f\n" "$xq" "$new"
        printf "Многочлен Гаусса:                  P(%s) = %.10f\n" "$xq" "$gauss"

        dln=$(bc_calc "if (($lag - $new) < 0) -($lag - $new) else ($lag - $new)")
        dlg=$(bc_calc "if (($lag - $gauss) < 0) -($lag - $gauss) else ($lag - $gauss)")
        printf "|Лагранж - Ньютон| = %.10f\n" "$dln"
        printf "|Лагранж - Гаусс|  = %.10f\n" "$dlg"
    else
        echo "Сетка неравномерная: Ньютон с конечными разностями и Гаусс не применяются."
    fi

    plot_graph
}

main_menu() {
    while true; do
        echo
        echo "ЛР №5. Интерполяция функции"
        echo "1) Ввести таблицу с клавиатуры"
        echo "2) Загрузить таблицу из файла"
        echo "3) Сформировать таблицу по функции"
        echo "0) Выход"
        read -r -p "Выберите пункт: " choice

        case "$choice" in
            1) read_keyboard && solve_current_data; pause ;;
            2) read_file_data && solve_current_data; pause ;;
            3) generate_by_function && solve_current_data; pause ;;
            0) exit 0 ;;
            *) echo "Неизвестный пункт меню." ;;
        esac
    done
}

check_dependencies
main_menu