set terminal pngcairo size 900,600 enhanced font 'Arial,11'
set output 'plots/plot.png'
set samples 80
set grid
set xlabel 'x'
set ylabel 'y'
set title 'Интерполяция функции'
set key left top
set xrange [1:5]
p(x) = (1)*((x-(2))/((1)-(2)))*((x-(3))/((1)-(3)))*((x-(4))/((1)-(4)))*((x-(5))/((1)-(5))) + (2)*((x-(1))/((2)-(1)))*((x-(3))/((2)-(3)))*((x-(4))/((2)-(4)))*((x-(5))/((2)-(5))) + (3)*((x-(1))/((3)-(1)))*((x-(2))/((3)-(2)))*((x-(4))/((3)-(4)))*((x-(5))/((3)-(5))) + (4)*((x-(1))/((4)-(1)))*((x-(2))/((4)-(2)))*((x-(3))/((4)-(3)))*((x-(5))/((4)-(5))) + (5)*((x-(1))/((5)-(1)))*((x-(2))/((5)-(2)))*((x-(3))/((5)-(3)))*((x-(4))/((5)-(4)))
plot 'data/input.txt' using 1:2 with points pointtype 7 pointsize 1.3 title 'Узлы интерполяции', p(x) with lines linewidth 2 title 'Интерполяционный многочлен'
