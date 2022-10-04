%% 1
clear;
x = -10:0.01:10;
y = x.^3 - 3.55.*x.^2+5.1.*x-3.1;
yP = [1 -3.55 5.1 -3.1];
plot(x, y, 'LineWidth', 1.2);
hold on;
R = roots(yP);
L = real(R) == R;
R = R(L);
plot(R, 0, '.', 'MarkerSize', 20);
grid on;

%% 2_a
clear;
P = [1 0.1 0.2 -0.2 -2 1];
R = roots(P);
Real = R(real(R) == R);
Max = max(abs(R));
X = -Max:0.01:Max;
Y = X.^5+0.1.*X.^4+0.2.*X.^3-0.2.*X.^2-2.*X+1;
subplot(1, 2, 1);
plot(X,Y, 'b', 'LineWidth', 1.2);
hold on;
plot(Real, 0, '.r', 'MarkerSize', 20);
x1 = 1/2*Max;
y1 = polyval(P, x1);
D = polyder(P);
k1 = polyval(D, x1);
K = k1*(X-x1)+y1;
plot(X, K, 'k--');
plot(x1, y1, '.k', 'MarkerSize', 20);
x2 = -1/2*Max;
y2 = polyval(P, x2);
k2 = -1/polyval(D, x2);
N = k2*(X-x2)+y2;
ang = atan(k2);
xn = cos(ang)+x2;
yn = sin(ang)+y2;
line([x2 xn], [y2 yn], 'Color', 'Red', 'LineWidth', 1.2);
plot(X, N, 'k--');
plot(x2, y2, '.k', 'MarkerSize', 20);
grid on;
axis equal
hold off
subplot(1, 2, 2)
Re = real(R);
Im = imag(R);
hold on
for i = 1:size(R)
    plot([0 Re(i)], [0 Im(i)], 'k--');
end
plot(Re, Im, '.r', 'MarkerSize', 15);
grid on;
hold off;

%% 4_a
clear;
P = [1 -2 6 -10 16];
X0 = 4;
Ans = P(1);
for i = 2:1:5
    Val = X0*Ans(i-1)+P(i);
    Ans = [Ans Val];
end
disp(Val);
disp(polyval(P, X0));
D = (polyval(polyder(P), X0));
P = Ans;
Ans = P(1);
for i = 2:1:4
    Val = X0*Ans(i-1)+P(i);
    Ans = [Ans Val];
end
disp(Val);
disp(D)

%% 4_b
clear;
P = [1 1+2i 0 -(1+3i) 0 7];
X0 = -2-i;
Ans = P(1);
for i = 2:1:6
    Val = X0*Ans(i-1)+P(i);
    Ans = [Ans Val];
end
disp(Val);
disp(polyval(P, X0));
D = (polyval(polyder(P), X0));

P = Ans;
Ans = P(1);
for i = 2:1:5
    Val = X0*Ans(i-1)+P(i);
    Ans = [Ans Val];
end
disp(Val);
disp(D)

%% 5

%% 6_1
clear;
syms b;
b = collect(b^2);
B = sym2poly(b);
syms a;
a = collect((a-1)*(a+2)*(a+3));
A = sym2poly(a);
[r, p] = residue(B, A);
syms x
C = [];
for i=1:size(r)
    C = [C r(i)*1/(x-(p(i)))];
    
end
disp(C);

%% 6_2
clear;
syms b;
b = collect(3+b);
B = sym2poly(b);
syms a;
a = collect((a-1)*(a^2+1));
A = sym2poly(a);
[r, p] = residue(B, A);
disp(r);
disp(p);

%% 6_3
clear;
syms b;
b = collect(b^2);
B = sym2poly(b);
syms a;
a = collect((b^4-1));
A = sym2poly(a);
[r, p] = residue(B, A);
disp(r);
disp(p);

%% 7_1

%% 7_2
clear;
x = [-1 0 1 2 3];
y = [6 5 0 3 2];
X = -1:0.01:3;
Y = interp1(x, y, X, 'spline' );
plot(X, Y);
hold on
I = find(Y==0);
plot(X(I), Y(I), '.r', 'MarkerSize' , 20);
grid on;
