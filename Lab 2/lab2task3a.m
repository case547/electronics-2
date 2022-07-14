% Capture and ananlyse microphone signal

clear
ports = serialportlist;
pb = PyBench(ports(end));

% Set sampling freq
fs = 8000;
pb = pb.set_samp_freq(fs);

% Capture N samples
N = 1000;
samples = pb.get_mic(N);
data = samples - mean(samples);

% Plot data
figure(1);
clf
plot(data);
xlabel('Sample number');
ylabel('Sample voltage (V)');
title('Captured signal');

% Find and plot spectrum
figure(2);
plot_spec(data, fs)

% Repeat capture and plot spectrum
while true
    samples = pb.get_mic(N);
    data = samples - mean(samples);
    figure(2);
    clf
    plot_spec(data, fs);
end