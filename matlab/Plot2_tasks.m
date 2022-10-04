%% 1
clear;
x = -10:0.1:10;
y = x+(1./(x.^2));
plot(x, y, 'LineWidth', 1.2);
grid on;
title('y = x+(1/x^2)');

%% 2
clear;
x = -10:0.1:10;
y = 2.*x./(1+x.^2);
plot(x, y, 'LineWidth', 1.2);
grid on;
title('y = 2x/(1+x^2)');

%% 8
clear;
phi = -pi/2:0.001:3*pi/2;
a = 100;
b = 2;
n = 4;
m = 7;
k = 14;
r = a./(a+(phi-pi/2).^n).*(b-sin(k.*phi)-cos(m.*phi));
y = r.*sin(phi);
x = r.*cos(phi);
plot(x, y, 'Linewidth', 1.2);
grid on;
title('r = a/(a+(φ-pi/2)^n)*(b-sinkφ-cosmφ)');

%% 12
clear;
t =-5:0.001:5;
a = 1/4;
b = 1/16;
m = 8;
n = 8;
s = 10;
x = (cos(t)-a.*cos(m.*t)+b.*sin(n.*t));
y = (sin(t)-a.*sin(m.*t)+b.*cos(n.*t));
for k = 1:1:s
    plot(x./k, y./k, 'LineWidth', 1.2);
end
grid on;

%% 13_1
clear;
x = -10:0.1:10;
y = 1./x-1./(x-1)+1./(x-2);
plot(x, y, 'LineWidth', 1.2);
grid on;
title('y = 1/x-1/(x-1)+1/(x-2)');

%% 13_2
clear;
x = -10:0.1:10;
y = sqrt(cos(pi.*x.^2));
plot(x, y, 'LineWidth', 1.2);
grid on;
title('sqrt(cos(pix^2))');

%% 13_3
clear;
x = -10:0.1:10;
y = acos(2.*sin(x));
plot(x, y, 'LineWidth', 1.2);
grid on;
title('arccos(2sin(x))');

%% 14 Розы Гранди
clear;
a = 4;
b = 4;
phi = -2*pi:0.1:2*pi;
r = a.*sin(b.*phi);
y = r.*sin(phi);
x = r.*cos(phi);
plot(x, y, 'LineWidth', 1.2);
grid on;
title('Розы Гранди');

%% 14 Лемниската Бернулли
clear;
phi = -10:0.001:10;
c = pi;
r = sqrt(2.*c^2.*cos(2.*phi));
y = r.*sin(phi);
x = r.*cos(phi);
plot(x, y, 'LineWidth', 1.2);
grid on;
title('Лемниската Бернулли');

%% 14 Улитка Паскаля
clear;
phi = -10:0.001:10;
b = 1;
r = 2*b*cos(phi./3);
y = r.*sin(phi);
x = r.*cos(phi);
plot(x, y, 'LineWidth', 1.2);
grid on;
title('Улитка Паскаля');
