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
plot_spec_dB(data, fs)

% Create a Hamming window
window = hamming(length(data));
while true
    samples = pb.get_mic(N);
    data = samples - mean(samples);
    clf;
    plot_spec_dB(data,fs);
    hold on
    plot_spec_dB(data.*window,fs);
end