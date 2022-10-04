%% 1_a
clear;
u = 0.1;
a = 0;
b = 2*pi;
x = linspace(a, b, 100);
F = @(x)exp(-u*x.*x).*cos(x.*x);
y = F(x);
plot(x, y);
hold on;
grid on;
xr = ginput(2);
[x_min, y_min] = fminbnd(F, xr(1, 1), xr(2, 1));
plot(x_min, y_min, 'r.', 'MarkerSize', 20);
plot(xr(1, 1), xr(1, 2), 'k.', 'MarkerSize', 10);
plot(xr(2, 1), xr(2, 2), 'k.', 'MarkerSize', 10);
line([xr(1, 1) xr(2, 1)], [xr(1, 2)  xr(2, 2)], 'Color', 'Black')

%% 1_b
clear;
a = 0;
b = 2*pi/3;
a1 = 1;
b1 = 2;
x = linspace(a, b, 100);
F = @(x)1./((a1.*cos(x)+b1.*sin(x)).^2);
y = F(x);
plot(x, y);
hold on;
grid on;
xr = ginput(2);
[x_min, y_min] = fminbnd(F, xr(1, 1), xr(2, 1));
plot(x_min, y_min, 'r.', 'MarkerSize', 20);
plot(xr(1, 1), xr(1, 2), 'k.', 'MarkerSize', 10);
plot(xr(2, 1), xr(2, 2), 'k.', 'MarkerSize', 10);
line([xr(1, 1) xr(2, 1)], [xr(1, 2)  xr(2, 2)], 'Color', 'Black')

%% 1_c
clear;
a = 0;
b = 4;
x = linspace(a, b, 100);
F = @(x)2-abs(x).*exp(1).^(-abs(x-1));
y = F(x);
plot(x, y);
hold on;
grid on;
xr = ginput(2);
[x_min, y_min] = fminbnd(F, xr(1, 1), xr(2, 1));
plot(x_min, y_min, 'r.', 'MarkerSize', 20);
plot(xr(1, 1), xr(1, 2), 'k.', 'MarkerSize', 10);
plot(xr(2, 1), xr(2, 2), 'k.', 'MarkerSize', 10);
line([xr(1, 1) xr(2, 1)], [xr(1, 2)  xr(2, 2)], 'Color', 'Black')

%% 1_d

%% 1_e

%% 2_a
clear;
xr = [0 -0.2; 1 -0.2];
global par_a;
hold on;
grid on;
for par_a = 1:1:8
x = linspace(0, 1, 100);
y = fun_a(x);
plot(x, y);
[x_min, y_min] = fminbnd(@fun_a, xr(1, 1), xr(2, 1));
plot(x_min, y_min, 'r.', 'MarkerSize', 20);
end
plot(xr(1, 1), xr(1, 2), 'k.', 'MarkerSize', 10);
plot(xr(2, 1), xr(2, 2), 'k.', 'MarkerSize', 10);
line([xr(1, 1) xr(2, 1)], [xr(1, 2)  xr(2, 2)], 'Color', 'Black');

%% 2_b
clear;
xr = [0 0.1; 1 0.1];
global par_b1;
global par_b2;
hold on;
grid on;
par_bM = linspace(1, 0, 8);
for par_b = 1:1:8
    par_b1 = par_b;
    par_b2 = par_bM(par_b);
    x = linspace(0, 1, 100);
    y = fun_b(x);
    plot(x, y);
    [x_min, y_min] = fminbnd(@fun_b, xr(1, 1), xr(2, 1));
    plot(x_min, y_min, 'r.', 'MarkerSize', 20);
end
plot(xr(1, 1), xr(1, 2), 'k.', 'MarkerSize', 10);
plot(xr(2, 1), xr(2, 2), 'k.', 'MarkerSize', 10);
line([xr(1, 1) xr(2, 1)], [xr(1, 2)  xr(2, 2)], 'Color', 'Black');

%% 2_c
clear;
xr = [0 0.1; 1 0.1];
global par_c1;
global par_c2;
hold on;
grid on;
par_cM = linspace(1, 0, 8);
for par_c = 1:1:8
    par_c1 = par_c;
    par_c2 = par_cM(par_c);
    x = linspace(0, 1, 100);
    y = fun_c(x);
    plot(x, y);
    [x_min, y_min] = fminbnd(@fun_c, xr(1, 1), xr(2, 1));
    plot(x_min, y_min, 'r.', 'MarkerSize', 20);
end
plot(xr(1, 1), xr(1, 2), 'k.', 'MarkerSize', 10);
plot(xr(2, 1), xr(2, 2), 'k.', 'MarkerSize', 10);
line([xr(1, 1) xr(2, 1)], [xr(1, 2)  xr(2, 2)], 'Color', 'Black');

%% 3
clear;
u = 0.1;
a = 0;
b = 2*pi;
x = linspace(a, b, 100);
F = @(x)exp(-u*x.*x).*cos(x.*x);
y = F(x);
plot(x, y);
hold on;
grid on;
xr = ginput(1);
[x_min, y_min] = fminsearch(F, xr(1)) ;
plot(x_min, y_min, 'r.', 'MarkerSize', 20);
plot(xr(1, 1), xr(1, 2), 'k.', 'MarkerSize', 20);

%% 4
clear;
u = 0.1;
a = 0;
b = 2*pi;
x = linspace(a, b, 100);
F = exp(-u*x.*x).*cos(x.*x);
TF = islocalmin(F);
plot(x, F);
hold on;
grid on;
plot(x(TF), F(TF), 'r.', 'MarkerSize', 20);

%% 5

%% 6

%%
function f = fun_a(x)
global par_a;
f = (x.^par_a).*log(x);
end

function f = fun_b(x)
global par_b1;
global par_b2;
f = (x.^(par_b1)).*(exp(1).^(-par_b2.*x));
end

function f = fun_c(x)
global par_c1;
global par_c2;
f = (x.^(par_c1)).*((1-x).^par_c2);
end