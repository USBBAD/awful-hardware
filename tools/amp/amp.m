function z = amp(deviation, startfreq, stopfreq, mode, paramfile)

% define the step size for frequency vector
% adder is the step for arithmetic series (mode = 1)
% multiplr is the step for geometric series (mode = 2)
adder = (10-1)/deviation;
multiplr = 10^(1/deviation);

% determine the exponent k for the highest desired frequency
k = 0;
while 10^k < stopfreq
k = k + 1;
end; % while

% a buffer where the component values 
% are read from a parameter file
RCLvalues = [];
PLOTBUF = [];

% open parameter file, read it line by line,
% and store values to RCLvalues buffer
fid = fopen(paramfile, 'r');
tline = fgetl(fid);
disp(tline);
while 1
tline = fgetl(fid);
if ( ischar(tline) && length(tline) > 1 )
disp(tline);
A = sscanf(tline, '%g');
RCLvalues = [RCLvalues A];
else
break;
endif;
end; % while
RCLvalues
fclose(fid);

% the outmost loop is determined by 
% the amount of rows in the parameter file.
% This way it is possible to vary component values
% and compare results.
for varied = 1:size(RCLvalues,2)

VCC = RCLvalues(1,varied);
VBE = RCLvalues(2,varied);
RB1 = RCLvalues(3,varied);
RB2 = RCLvalues(4,varied);
RC  = RCLvalues(5,varied);
RE  = RCLvalues(6,varied);
RL  = RCLvalues(7,varied);
RS  = RCLvalues(8,varied);
CB  = RCLvalues(9,varied);
CE  = RCLvalues(10,varied);
CC  = RCLvalues(11,varied);
B1  = RCLvalues(12,varied);

% calculate the quiescent values to define 
% transistor parameters gm and rpi1
IBQ = (VCC*RB2/(RB1 + RB2) - VBE)/(RB1*RB2/(RB1+RB2) + (B1 + 1)*RE)
ICQ = B1*IBQ
V4 = VCC - RC*ICQ
gm = ICQ/0.025
rpi1 = B1/gm

% define empty arrays for the calculated transfer function values
H=[];
X=[];
% begin from frequency of 1 Hz
f = 1;

% loop through all the frequency decades 10, 100, 1000, etc.
% according to the exponent k
for j = 0:k
% loop through the specific decade, e.g. 10, 20, 30, 40, ... 90.
while f <= (10^(j+1) - adder)

if (f >= (startfreq - 0.00001) && f <= stopfreq)

% frequency to angular frequency conversion
w = f*2*pi;

% the numerator matrix (determinant), solve for column 5
os=[((1/RS)+i*w*CB) -(i*w*CB) 0 0 (1/RS); ...
    -(i*w*CB) (i*w*CB+(1/RB1)+(1/RB2)+(1/rpi1)) -(1/rpi1) 0 0; ...
    0 -((B1+1)/rpi1) (((B1+1)/rpi1)+(1/RE)+i*w*CE) 0 0; ...
    0 (B1/rpi1) -(B1/rpi1) (i*w*CC+(1/RC)) 0; ...
    0 0 0 -(i*w*CC) 0];

% the denominator matrix (determinant)
nim=[((1/RS)+i*w*CB) -(i*w*CB) 0 0 0; ...
    -(i*w*CB) (i*w*CB+(1/RB1)+(1/RB2)+(1/rpi1)) -(1/rpi1) 0 0; ...
    0 -((B1+1)/rpi1) (((B1+1)/rpi1)+(1/RE)+i*w*CE) 0 0; ...
    0 (B1/rpi1) -(B1/rpi1) (i*w*CC+(1/RC)) -(i*w*CC); ...
    0 0 0 -(i*w*CC) (i*w*CC+(1/RL))];

% store the transfer function values to H
% and frequency values to X
H = [H 20*log10(abs(det(os)/det(nim)))];
X = [X f]; 
endif;

% advance frequency according to the chosen mode
% (arithmetic) or (geometric)
if (mode == 1)
f = f + adder*10^j;
else
f = f*multiplr;
endif; % mode

end; % while
end; % for
PLOTBUF = [PLOTBUF X' H'];
end; % for varied

% save the data for plotting later with gnuplot
% ngspice generates similar data file, 
% so comparison and plotting against that is simple.
save -ascii ampplot_octa.data PLOTBUF

% handle the Octave specific plotting here
figure (3)
semilogx(X, PLOTBUF(1:end,2:2:6),'LineWidth',3);
set(gca,'FontSize',14)
set(gca,'YTick',[10*(floor(min(H)/10) - 1):10:10*(ceil(max(H)/10) + 1)]);
legend('1','2','3')
xlabel('frequency [Hz]');
ylabel('magnitude of voltage ratio [dB]');
grid on;
grid minor on;

