%%
clear;
syms x;
syms a;
f = x^3-sin(x) + a*exp(-2*x);
subs(f, a, tan(x));
p = x^5-2*x^3+5*x^2+2*x-1;
horner(p);
