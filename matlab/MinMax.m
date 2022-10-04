%%
clear;
global par T;
par = 0.1;
a = 0;
b = 2*pi;
x = linspace(a, b, 100);
y = fun_min(x);
plot(x,y);
hold on;
grid on;
title (T);
xr = ginput(2);
[x_min, y_min] = fminbnd(@fun_min, xr(1, 1), xr(2, 1));
plot(x_min, y_min, 'r.', 'MarkerSize', 20);
plot(xr(1, 1), xr(1, 2), 'k.', 'MarkerSize', 10);
plot(xr(2, 1), xr(2, 2), 'k.', 'MarkerSize', 10);
line([xr(1, 1) xr(2, 1)], [xr(1, 2)  xr(2, 2)], 'Color', 'Black')

%%
function f = fun_min(x)
global par T;
f = exp(-par*x.*x).*cos(x.*x);
T = ['exp(-mu*x^2)*cos(x^2)'];
end
