function plot_spec(sig, fs)
% Plots the frequency spectrum of sig
    magnitude = abs(fft(sig));
    N = length(sig);
    df = fs/N;
    f = 0:df:fs/2;
    Y = magnitude(1:length(f));
    plot(f, 2*Y/N)
    xlabel('\fontsize{14}Frequency (Hz)');
    ylabel('\fontsize{14}Magnitude');
    title('\fontsize{16}Spectrum');