This archive contains an Octave/Matlab file (amp.m)
and the corresponding parameter file (params3.txt).
These files together can be used for calculating the frequency response
of a basic bipolar junction transistor amplifier.
The parameter file can contain any number of rows
to examine the effects of changing the value of some specific component.
Currently changes in the collector resistor RC are investigated.
The function is run in Octave with a command:  amp(9,10,100000,1,'params3.txt')
where the first parameter defines how many points are evaluated within one frequency decade,
the second parameter defines the starting frequency in hertz,
the third parameter defines the end frequency in hertz,
the fourth parameter chooses to advance the frequency as an
arithmetic series (1) or a geometric series (2).
The fifth parameter defines the name of the parameter file,
which is assumed to reside in the same directory as the amp.m file.
