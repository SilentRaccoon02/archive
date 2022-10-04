function a = two_rows(in)
x = size(in, 1);
y = size(in, 2);
out = zeros(x,y);
if (size(in, 1) == 2) && (ismatrix(in))
        a = in;
else
    fprintf('NO\n')
    a = out;
end
end
