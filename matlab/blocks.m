function M = blocks(n,m)
nmones = ones(n,m);
nmzeros = zeros(n,m);
M = [nmones nmzeros; nmzeros nmones];
end
