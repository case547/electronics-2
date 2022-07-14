clear
close all
ports = serialportlist;
pb = PyBench(ports(end));

%% Testing gyroscope

N = 500;    % each graph is 500 time points
end_time = 10.0;    % initial guess of time axis range
gx = 0; gy = 0; % initialise angles gy pitch, gx roll

while true
    % Plot axes first
    figure(1)
    clf(1)
    axis([0 end_time -90 90]);
    title('Gyroscope Pitch & Roll Angles', 'FontSize', 16);
    ylabel('Angle (deg)', 'FontSize', 14);
    xlabel('Time (sec)', 'FontSize', 14);
    grid on; hold on;
    timestamp = 0;
    tic;

    % Read gyroscope data
    for i = 1:N
        [x, y, z] = pb.get_gyro();  % angular rate in rad/sec
        dt = toc;   % elapsed time (incremental delta(t) since last tic)
        tic;
        timestamp = timestamp + dt;
        
        % Accumulate gx and gy, and limit to +/- pi/2
        gx = max(min(gx+x*dt, pi/2), -pi/2);
        gy = max(min(gy+y*dt, pi/2), -pi/2);
        
        plot(timestamp, gy*180/pi, '.b');   % plot pitch in blue
        plot(timestamp, gx*180/pi, '.r');    % plot roll in red
        pause(0.001);   % needed by Matlab plot function
    end
    end_time = timestamp;   % use actual time range from now on
end