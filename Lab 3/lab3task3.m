% Measure system gain at frquency f_sig

clear all
ports = serialportlist;
pb = PyBench(ports(end));

% Generate sine wave at sig_freq Hz
max_x = 1.55;
min_x = 1.45;
f_sig = 5.0;
pb = pb.set_sig_freq(f_sig);
pb = pb.set_max_v(max_x);
pb = pb.set_min_v(min_x);
pb.sine();
pause(2)

% Capture output y(t)
pb = pb.set_samp_freq(100);
N = 300;
y = pb.get_block(N);

% Plot signal
plot(y);
xlabel('Sample no.');
ylabel('Output voltage');
title('Bulb Box output (V)');

% Compute gain
x_p2p = max_x - min_x;
y_p2p = max(y) - min(y);
G = y_p2p/x_p2p
G_dB = 20*log10(y_p2p/x_p2p)