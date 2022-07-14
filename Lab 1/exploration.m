amp = 1;
f = 400;
fs = 3200;

T = 0.02;
dt = 1/fs;
t = 0:dt:T;

figure
hold on

for n=1:2:7
    a_n = 2*amp/(n*pi)*sin(n*pi/2);
    func = func + a_n*cos(n*f*t);
    plot(func(1:200));
end
        