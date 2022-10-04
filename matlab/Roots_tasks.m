%% 3_a
clear;
a = -3;
b = 3;
m = 100;
x = linspace(a, b, m);
f = 'sin(exp(1).^x)';
plot(x , eval(f), x , 0*x, ':');
hold on;
grid on;
z = ginput(1);
[zr, fr] = fzero(f, z(1));
plot(zr, fr, '.r', 'MarkerSize', 20);
plot(z(1), z(2), '.k', 'MarkerSize', 20);

%% 3_b
clear;
a = 0;
b = 2*pi;
m = 100;
x = linspace(a, b, m);
f = 'sin(x.*(1-x))';
plot(x , eval(f), x , 0*x, ':');
hold on;
grid on;
z = ginput(1);
[zr, fr] = fzero(f, z(1));
plot(zr, fr, '.r', 'MarkerSize', 20);
plot(z(1), z(2), '.k', 'MarkerSize', 20);

%% 3_c
clear;
a = 0;
b = 4*pi;
m = 100;
x = linspace(a, b, m);
f = 'x.*sin(x)-cos(x)';
plot(x , eval(f), x , 0*x, ':');
hold on;
grid on;
z = ginput(1);
[zr, fr] = fzero(f, z(1));
plot(zr, fr, '.r', 'MarkerSize', 20);
plot(z(1), z(2), '.k', 'MarkerSize', 20);

%% 3_d
clear;
a = pi/2;
b = 3*pi;
m = 100;
x = linspace(a, b, m);
f = 'sin(x).^2+(1/2-1./x).*cos(x)-1/2';
plot(x , eval(f), x , 0*x, ':');
hold on;
grid on;
z = ginput(1);
[zr, fr] = fzero(f, z(1));
plot(zr, fr, '.r', 'MarkerSize', 20);
plot(z(1), z(2), '.k', 'MarkerSize', 20);

%% 3_e
clear;
a = -2*pi;
b = 6*pi;
m = 100;
x = linspace(a, b, m);
f = '5.*exp(1).^(-0.1.*x).*sin(x)-0.1.*x';
plot(x , eval(f), x , 0*x, ':');
hold on;
grid on;
z = ginput(1);
[zr, fr] = fzero(f, z(1));
plot(zr, fr, '.r', 'MarkerSize', 20);
plot(z(1), z(2), '.k', 'MarkerSize', 20);

%% 4
clear;
root1 = fzero(@(x)x.^2+1, 1i);
root2 = fzero(@(x)x.^2+1, -1i);
syms x;
f = x^2+1;
solve1 = solve(f);
disp(root1);
disp(root2);
disp(solve1);

%% 5
clear;
a = -1;
b = 1;
m = 100;
x = linspace(a, b, m);
f = 'x.^2-exp(1).^(0.001+x.^2)';
plot(x , eval(f));
syms x;
f = x-exp(1)^(0.001+x^2);
solve1 = solve(f);
disp(solve1);

%% Метод Ньютона
clear;
a = -10;
b = 10;
m = 100;
x = linspace(a, b, m);
h = 1;
iter = 100;
eps = 0.01;
f = '1+x.*sin(x)';
plot(x , eval(f), x , 0*x, ':');
z = ginput(1);
hold on;
F = @(x)1+x.*sin(x);
DF = @(x)sin(x)+x.*cos(x);
x0 = z(1)+a;
x1 = z(1)+b;
Xi = (x0+x1)/2; 
Yo = F(x0);
i = 0;
while abs(Yo) > eps && i < iter
    Xiplus = Xi - F(Xi)/DF(Xi);
    Xi = Xiplus;
    Y = F(Xiplus);
    i = i+1;
end
plot(z(1), z(2), '.k', 'MarkerSize', 20);
plot(Xiplus, Y, '.r', 'MarkerSize', 20);
grid on;
