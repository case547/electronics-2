% Plot theoretical freq. resp of Bulb Board
f = (0:0.1:20);
D = [0.038 1.19 43 1000];       % specify denominator coeffients
s = 1i*2*pi*f;                  % s = jw
G = 1000./abs(polyval(D,s));    % calculate polynomial G(s)
Gdb = 20*log10(G);              % gain in dB
figure;
plot(f, Gdb);
xlabel('Frequency (Hz)');
ylabel('Gain(db)');
title('Theoretical Frequency Response');