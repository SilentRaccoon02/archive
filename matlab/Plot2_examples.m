%%
clear;
x = 0:0.001:0.1;
y = log(sin(pi./x));
plot(x, y, 'LineWidth', 1.2);
grid on;
title ('y = ln(sin(pi/x))');

%%
clear;
phi = 0:0.001:2*pi;
r = sin(phi)./phi;
y = r.*sin(phi);
x = r.*cos(phi);
plot(x, y, 'LineWidth', 1.2);
grid on;
title ('r = sin(φ)/φ');
