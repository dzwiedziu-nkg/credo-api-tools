# set terminal pngcairo  transparent enhanced font "arial,10" fontscale 1.0 size 600, 400
set terminal png size 6565,200

set output 'credo-data-export/brix.png'
set xdata time
set format x "%d %H:%M:%S" timedate
set timefmt "%Y-%m-%d_%H:%M:%S"
unset key
set style increment default
set offsets 0.5, 1.5, 0.2, 0.2
set xtics  norangelimit
set xtics   ()
set ytics  norangelimit
set ytics   ()
set xtics  font ",10" norotate
set ytics  font ",10" norotate
set notitle
set xrange [ * : * ] noreverse writeback
set x2range [ * : * ] noreverse writeback
set yrange [ * : * ] noreverse writeback
set y2range [ * : * ] noreverse writeback
set zrange [ * : * ] noreverse writeback
set cbrange [ * : * ] noreverse writeback
set rrange [ * : * ] noreverse writeback
fulltime(col) = strftime("%Y-%m-%d %H:%M:%S",column(col))
parttime(col) = strftime("%H:%M:%.3S",column(col))
## Last datafile plotted: "-"
plot 'credo-data-export/credocut.plot' using 1:2
