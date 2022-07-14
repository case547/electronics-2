clear all
close all
ports = serialportlist;
pb = PyBench(ports(end));

%% Testing accelerometer

N = 500;    % each graph is 500 time points
end_time = 10.0;    % initial guess of time axis range

while true
    % Plot axes first
    figure(1)
    clf(1)
    axis([0 end_time -90 90]);
    title('Accelerometer Pitch & Roll Angles', 'FontSize', 16);
    ylabel('Angle (deg)', 'FontSize', 14);
    xlabel('Time (sec)', 'FontSize', 14);
    grid on; hold on;
    tic;
    
    % Read and plot accelerometer data
    for i = 1:N
        [p, r] = pb.get_accel();    % in radians
        timestamp = toc;
        pitch = p*180/pi;
        roll = r*180/pi;
        plot(timestamp, pitch, '.b');   % plot pitch in blue
        plot(timestamp, roll, '.r');    % plot roll in red
        pause(0.001);   % needed by Matlab plot function
    end
    end_time = toc; % use actual time range from now on
end