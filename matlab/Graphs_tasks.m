%%
s = Graphsedges(:, 1);
t = Graphsedges(:, 2);
weights = str2double(Graphsedges(:, 3));
G = digraph(s, t, weights);
D = indegree(G);
G.Nodes.NodeSizes = 2.*sqrt(D - min(D)+0.2);
G.Nodes.NodeColors = D;
p = plot(G);
colormap hsv;
disp(p);
p.MarkerSize = G.Nodes.NodeSizes;
p.NodeCData = G.Nodes.NodeColors;
colorbar
T = table(G.Nodes.Name, D);
T1 = sortrows(T, 'Var2', 'descend');
disp(head(T1, 5));