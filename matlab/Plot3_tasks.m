%% 0_1
clear;
t = (0:0.05:6*pi);
x = sin(t);
y = 3*cos(t);
plot3(x, y, t, 'b');
hold on;
line([-1,-1], [-7*pi, (40-7*pi)], [0, 20], 'LineStyle', '--', 'Color', 'k');
plot3(-1, 0, 7*pi/2, '.k', 'MarkerSize', 20);
hold off;
grid on;

%% 0_2
clear;
n = input('n = ');
t1 = pi*(-n:5:n)/n;
t2 = (pi/2)*(-n:5:n)'/n;
X = cos(t2)*cos(t1);
Y = cos(t2)*sin(t1);
E = ones(size(t1));
Z = sin(t2)*E;
plot3(X, Y, Z, 'b');
grid on;
title('Сфера');

%% 0_3
clear;
Lx = linspace(-pi, pi, 40);
Ly = linspace(-pi, pi, 50);
[X, Y] = meshgrid(Lx, Ly);
Z = F(X, Y);
surf(X, Y, Z);
grid on;

%% 1
clear;
XY = [-10, 10, -10, 10];
ezsurf(@F2, XY);

%% 2_a
clear;
x = -10:0.1:10;
y = -10:0.1:10;
a = 1;
[X, Y] = meshgrid(x,y);
Z = a*sin(sqrt(X.^2+Y.^2))./sqrt(X.^2+Y.^2);
subplot(2, 1, 1);
plot3(X, Y, Z);
title('plot3');
grid on;
subplot(2, 1, 2);
mesh(X, Y, Z);
title('mesh');
grid on;

%% 2_b
clear;
x = -10:0.1:10;
y = -10:0.1:10;
[X, Y] = meshgrid(x,y);
Z = -X.*sin(X)-Y.*cos(Y);
subplot(2, 1, 1);
plot3(X, Y, Z);
title('plot3');
grid on;
subplot(2, 1, 2);
mesh(X, Y, Z);
title('mesh');
grid on;

%% 3_a
clear;
x = -5:0.1:5;
y = -5:0.1:5;
a = 1;
[X, Y] = meshgrid(x,y);
Z = a.*X.*exp(1).^(-X.^2-Y.^2);
subplot(2, 2, 1);
mesh(X, Y, Z);
title('mesh');
grid on;
subplot(2, 2, 2);
surf(X, Y, Z);
title('surf');
grid on;
subplot(2, 2, 3);
surfc(X, Y, Z);
title('surfc');
grid on;

%% 3_h
clear;
u = 0:0.1:2*pi;
v = -pi/2:0.1:pi/2;
a = 1;
b = 1;
[U, V] = meshgrid(u, v);
X = a.*cos(U).*cos(V);
Y = a.*sin(U).*cos(V);
Z = b.*sin(V);
mesh(X, Y, Z);
title('Эллипсоид вращения')
grid on;

%% 3_n
clear;
u = 0:0.1:2*pi;
v = -1/2:0.1:1/2;
[U, V] = meshgrid(u, v);
X = (1+V.*cos(U./2)).*cos(U);
Y = (1+V.*cos(U./2)).*sin(U);
Z = V.*sin(U./2);
mesh(X, Y, Z);
title('Лента Мебиуса');
grid on;

%%
function F = F(x,y)
F = 20-x.^2-y.^2;
end

function F2 = F2(x,y)
a = -1;
b = 1;
c = 1;
d = 1;
F2 = (d - a.*x - b.*y)./c;
end
