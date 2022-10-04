%%
clear;
t = 0:0.05:8*pi;
x = 2*sin(t);
y = 3*cos(t);
plot3(t,x,y, 'Color', [1/2,6/8,2/9], 'Marker','*');
grid on;

%%
clear;
t = 0:0.05:8*pi;
x = 2*sin(t);
y = 3*cos(t);
comet3(t, x, y);

%%
clear;
x = (-5:0.5:5);
y = (-5:0.5:5);
[X ,Y] = meshgrid(x, y);
plot(X, Y);
[X, Y, Z] = peaks;
subplot(2, 2, 1);
mesh(Z);
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
colormap winter;

%%
clear;
x = (-5:0.5:5);
y = (-5:0.5:5);
[X ,Y] = meshgrid(x, y);
plot(X, Y);
[X, Y, Z] = peaks;
subplot(2, 2, 1);
surfc(X, Y, Z);
title('faceted');
grid on;
shading faceted;
subplot(2, 2, 2);
surfc(X, Y, Z);
title('flat');
grid on;
shading flat;
subplot(2, 2, 3);
surfc(X, Y, Z);
title('interp');
grid on;
shading interp

%%
clear;
x = @(r, fi)r.*cos(fi);
y = @(r, fi)r.*sin(fi);
z = @(r, fi)r.^2;
figure
ezsurf(x, y, z, [-pi, pi, -pi, pi]);

%%
clear;
a = 2; 
c = 1;
u1 = 0;
u2 = 5;
v1 = 0;
v2 = 2*pi;
N1 = 40;
N2 = 40;
u = linspace(u1, u2, N1);
v = linspace(v1, v2, N2);
[U, V] = meshgrid(u, v);
x = a*sinh(U).*cos(V);
y = a*sinh(U).*sin(V);
z = c*cosh(U);
surf(x, y, z); 
hold on; 
surf(x, y, -z);
title('Hyperboloid of two sheets');
hold off;
