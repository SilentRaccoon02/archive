%%
clear;
t = (0:0.05:9*pi);
x = 2*sin(t);
y = 3*cos(t);
plot3(x, y, t, 'b*');
grid on;
title('Пространственная спираль');

%%
clear;
t = -10*pi:pi/250:10*pi;
x = (cos(2*t).^2).*sin(t);
y = (sin(2*t).^2).*cos(t);
comet3(x,y,t);

%%
clear;
[X, Y, Z] = sphere(12);
subplot(1,2,1);
mesh(X, Y, Z);
title('Figure a: Opaque');
hidden on;
axis square off;
subplot(1,2,2);
mesh(X, Y, Z);
title('Figure b: Transparent');
hidden off;
axis square off;

%%
clear;
y = (-10:0.5:10);
x = (-10:0.5:10);
[X, Y] = meshgrid(x,y);
Z = sin(sqrt(X.^2+Y.^2))./sqrt(X.^2+Y.^2);
figure
surfc(X, Y, Z);
view(-38, 18);
title('Normal Response');
