% Transient behaviour of Bulb board
clear all
clf
ports = serialportlist;
pb = PyBench(ports(end));
% Set parameters
fs = 100;
pb = pb.set_samp_freq(fs);
x_min = 1.0;
x_max = 1.5;
N = 500;
% Capture step response
pb.dc(x_min);           % initialise bulb value
pause(1);
pb.dc(x_max)            % rising step
rise = pb.get_block(N);
pb.dc(x_min)            % falling step
fall = pb.get_block(N);
data = [rise' fall'];
% Plotting
clf
plot(data)
xlabel('Sample number');
ylabel('Output (V)');
title('Experimental Step Response');