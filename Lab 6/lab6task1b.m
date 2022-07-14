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
num_taps = 20   % set number of taps
for i=num_taps:N
    tap = 0;    % initialise tap value
    for j=0:num_taps-1
        tap = tap + x(i-j); % incrementally add to tap variable 
    end
    y(i) = tap/num_taps;    % set y(i) to be mean of tap sum
end

% Play the original then filtered sound
sound(x, fs)
disp('Playing original - press enter when finished')
pause;
sound(y, fs)
disp('Playing filtered music')

% Plot filtered signal
figure(2);
plot(y);
xlabel('Sample no');
ylabel('Signal (v)');
title('Stay Alive Music - Filtered')