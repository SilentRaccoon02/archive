%%
clear;
G = graph({'A', 'B', 'B'}, {'B', 'C', 'D'});
plot(G);

%%
clear;
s = [1 1 2 2 3 3 4 4 5 5];
t = [2 5 3 4 4 5 3 1 1 6];
weight = randi(100, size(s));
names = {'a', 'b', 'c', 'd', 'e', 'f'};
G = digraph(s, t, weight, names);
p = plot(G);
p.NodeColor = 'r';
p.EdgeColor = 'k';
disp(p);
%highlight(p, {'a', 'b', 'e'}, {'b', 'c', 'f'});
shortPath = shortestpath(G, 'a', 'f');
highlight(p, shortPath)

%%
disp(adjacency(G));
disp(indegree(G));
disp(outdegree(G));

%%
clear;
n = 12;
A = delsq(numgrid('L', n));
G = graph(A, 'omitselfloops');
p = plot(G);
G.Nodes.NodeColors = degree(G);
p.NodeCData = G.Nodes.NodeColors;
colorbar
G.Edges.Weight = randi([10 250], 130, 1);
G.Edges.LWidths = 7*G.Edges.Weight/max(G.Edges.Weight);
p.LineWidth = G.Edges.LWidths;

%%
H = subgraph(G, [1:31 36:41]);
p1 = plot(H, 'NodeCData', H.Nodes.NodeColors, 'LineWidth', H.Edges.LWidths);
labeledge(p1, find(H.Edges.LWidths > 6), 'L');
path = shortestpath(H, 11, 37);
highlight(p1, [11 37]);
highlight(p1, path, 'EdgeColor', 'green');
p1.NodeLabel = {};
