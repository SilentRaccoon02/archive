%%
clear;
f = @zerosearch;
r = fzero(f, 0);

%%
clear;
x = linspace(-5, 5, 100);
y = x.^2+2*x-1-sin(x);
figure
plot(x, y)
z = ginput(1);

%%
clear;
syms x;
f = x*x+2*x-1-sin(x);
r1 = solve(f);
f = x*x+2*x+3;
r2 = solve(f, x);

%%
function f = zerosearch(x)
%f = x^2-2*x-3;
f = x^2+2*x-1-sin(x);
end
