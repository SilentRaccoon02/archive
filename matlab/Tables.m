%%
clear;
xlsName = 'Table.xlsx';
T = readtable(xlsName);

%%
Name1 = "Руководитель";
Name2 = "Исполнитель";
[i1 j1] = find(Table == Name1);
R = Table(i1, 1);
Str1 = join(R, '; ');
[i2 j2] = find(Table == Name2);
I = Table(i2, 1);
Str2 = join(I, '; ');
Out = [Name1 Str1; Name2  Str2];
OutTable = array2table(Out);
writetable(OutTable, 'Table_.xlsx');

%%
Table2;
age = split(Table2(:, 3), '-');
age = 2021 - str2double(age(:,3));

idsum = strlength(Table2(:, 4)) == 11 | strlength(Table2(:, 5)) == 11;
K = str2double(Table2(:, 6))./str2double(Table2(:,7)).*idsum;

X = zeros(size(Table2(:, 1)));
X = X + (K > 0.5 & K <= 1);
X = X + 0.8*(K > 0.4 & K <= 0.5);
X = X + 0.6*(K > 0.3 & K <= 0.4);
X = X + 0.4*(K > 0.2 & K <= 0.3);
X = X + 0.2*(K > 0.1 & K <= 0.2);
X = X + 0.1*(K > 0 & K <= 0.1);

%+имена переменных
OutNames = ["Surname" "Name" "Date" "Age" "id1" "id2" "Inside" "Outside" "K" "X" "Publication"];
Out = array2table([Table2(:,1:3), age, Table2(:,4:7), K, X, Table2(:,8)]);
writetable(Out, 'Table2_.xlsx');
