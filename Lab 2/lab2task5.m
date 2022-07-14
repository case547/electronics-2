% Analyse two drum beats

clear
[sig fs] = audioread('two_drums.wav');
sound(sig, fs)

% Plot signal
figure(1);
clf;
plot(sig);
xlabel('Sample no')
ylabel('Signal (V)');
title('Two Drums');

% Divide signal into segments and find energy of each
T = 0.02;
N = fs*T;
E = [];

for i=1:N:length(sig)-N+1
    seg = sig(i:i+N-1);
    E = [E seg'*seg];
end

% Plot energy graph and peak values
figure(2);
clf;
x = 1:length(E);
plot(x, E)
xlabel('Segment number');
ylabel('Energy');
title('Energy and Peak Values')
hold on
% Find local maxima
[pks locs] = findpeaks(E);
plot(locs, pks, 'x');
hold off

% Plot energy spectrum
figure(3)
plot_spec(E - mean(E), 1/T);