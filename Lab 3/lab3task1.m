clear
ports = serialportlist;
pb = PyBench(ports(end));
disp('PyBench obj created');

data = [];

for x=0.4:0.05:1.8
    pb.dc(x);
    pause(1);
    y = pb.get_one();
    intensity = [x, y];
    data = [data; intensity];
end

pb.dc(0);

figure;
plot(data(:,1), data(:,2));
title('Bulb Board Characterisation');
xlabel('x\_dc (V)');
ylabel('y\_dc (V)');