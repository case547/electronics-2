function [sig] = sine_gen(amp, f, fs, T)
% Generate a sine wave of amplitude amp, frequency f with sampling
% frequency fs for duration T

    dt = 1/fs;
    t = 0:dt:T;
    sig = amp*sin(2*pi*f*t);