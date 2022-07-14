%  Perform automatic measurement of frequency response G(s) 

clear
ports = serialportlist;
pb = PyBench(ports(end));

max_x = 1.55;
min_x = 1.45;
pb = pb.set_max_v(max_x);
pb = pb.set_min_v(min_x);

pb = pb.set_samp_freq(100);
N = 300;

x_p2p = max_x - min_x;

for i=1:19
    f_sig = i;
    pb = pb.set_sig_freq(f_sig);
    pb.sine();
    pause(2)
    
    y = pb.get_block(N);
    
    y_p2p = max(y) - min(y);
    G_dB = 20*log10(y_p2p/x_p2p);
    
    x_data(i) = f_sig;
    y_data(i) = G_dB;
end

plot(x_data,y_data,'o')
hold on
plot(x_data,y_data)
xlabel('Frequency (Hz)');
ylabel('Gain (db)');
title('Measured Frequency Response');