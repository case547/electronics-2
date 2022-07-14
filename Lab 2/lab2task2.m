%% Signal generation and capture with PyBench

clear
ports = serialportlist;
pb = PyBench(ports(end));

% Set parameters
f = 440;
fs = 8000;
pb = pb.set_sig_freq(f);
pb = pb.set_samp_freq(fs);
pb = pb.set_max_v(3.0);
pb = pb.set_min_v(0.5);
pb = pb.set_duty_cycle(50);

% Generate signal
pb.square()

%% Spectra exploration

% Capture N samples
N = 1000;
samples = pb.get_block(N);
data = samples - mean(samples); % nullify DC offset

% Plot data
figure(1);
plot(data(1:200),'o'); % plot circles
hold on
plot(data(1:200)); % plot line
xlabel('Sample number');
ylabel('Sample voltage (V)');
title('Captured signal');
hold off

% Find spectrum
figure(2);
plot_spec(data,fs);