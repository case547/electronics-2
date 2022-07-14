clear
[sig fs] = audioread('bgs.wav');

% Add noise to music
x = sig + 0.2*rand(size(sig));

% Plot signal
figure(1);
clf;
plot(x);
xlabel('Sample number');
ylabel('Signal (V)');
title("Stayin' Alive");

% Filter music with moving average filter
N = size(x);
for i=4:N
    y(i) = (x(i)+ x(i-1)+x(i-2)+x(i-3))/4;
end
y(1) = x(1)/4;
y(2) = (x(2)+x(1))/4;
y(3) = (x(3)+x(2)+x(1))/4;

% Play the original then filtered sound
sound(x, fs)
disp('Playing original - press enter when finished')
pause;
sound(y, fs)
disp('Playing filtered music')