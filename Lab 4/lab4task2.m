clear
close all
ports = serialportlist;
pb = PyBench(ports(end));

%% 3D display of roll and pitch angles

model = IMU_3D();   % create IMU 3D visualisation object
N = 50;
tic;
gx = 0; gy = 0;
fig1 = figure(1);

while true
    for i = 1:N
        [p, r] = pb.get_accel();
        [x, y, z] = pb.get_gyro();
        dt = toc;
        tic;
        gx = max(min(gx+x*dt, pi/2), -pi/2);
        gy = max(min(gy+y*dt, pi/2), -pi/2);
        clf(fig1);
        subplot(2,1,1);
        model.draw(fig1, p, r, 'Accelerometer');
        subplot(2,1,2);
        model.draw(fig1, gy, gx, 'Gyroscope');
        pause (0.0001);
    end
end