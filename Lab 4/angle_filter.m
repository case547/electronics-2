clear all
close all
ports = serialportlist;
pb = PyBench(ports(end));

%% Complementary filter effects

N = 500;
gx = 0; gy = 0;                 % gyro initial angles
angle_x = 0; angle_y = 0;       % combined angle using filter
alpha = 0.7; beta = 1-alpha;    % weight factors
end_time = 10;

while true
    % Plot axes first
    figure(1)
    clf(1)
    axis([0 end_time -90 90]);
    title('Gyroscope Pitch & Roll Angles', 'FontSize', 16);
    ylabel('Angle (deg)', 'FontSize', 14);
    xlabel('Time (sec)', 'FontSize', 14);
    grid on; hold on;
    tic;
    
    for i = 1:N
        [p, r] = pb.get_accel();
        [x, y, z] = pb.get_gyro();
        dt = toc;
        tic;
        % Integration for gyro angles
        gx = max(min(gx+x*dt, pi/2), -pi/2);
        gy = max(min(gy+y*dt, pi/2), -pi/2);
        
        % Complementary filtered angles
        angle_x = alpha*(angle_x + x*dt) + beta*r;
        angle_y = alpha*(angle_y + y*dt) + beta*p;
        
        plot(dt, angle_y, '.b');    % plot filtered pitch in blue
        plot(dt, angle_x, '.r');    % plot filtered roll in red
        
        pause (0.001);
    end
    end_time = toc;
end