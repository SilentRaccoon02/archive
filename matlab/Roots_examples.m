%%
clear;
a = 1;
x = fzero(@(x)x.^2-a,0.5);
disp(x);

%%
clear;
a = -3;
b = 3;
m = 100;
x = linspace(a, b, m);
f = 'x.^2+2*x-1-sin(x)';
plot(x , eval(f), x , 0*x, ':');
hold on;
grid on;
z = ginput(1);
[zr, fr] = fzero(f, z(1));
plot(zr, fr, '.r', 'MarkerSize', 20);
plot(z(1), z(2), '.k', 'MarkerSize', 20);

%%
clear;
syms x;
Eq = x*x+2*x-1-sin(x);
a = solve(Eq);
disp(a);
