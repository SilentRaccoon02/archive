%%
clear;
A = ['Фамилия     ' 'Имя         ' 'Отчество    ';
     'Иванов      ' 'Иван        ' 'Иванович    ';
     'Банкет      ' 'Михаил      ' 'Юрьевич     ';
     'Дащкова     ' 'Олеся       ' 'Вячеславовна'];

B = ["Фамилия" "Имя" "Отчество";
     "Иванов" "Иван" "Иванович";
     "Банкет" "Михаил" "Юрьевич";
     "Дащкова" "Олеся" "Вячеславовна"];
 
name = B(2, 2);
name_char = char(name);

num = 107;
num_string = string(num);
num_double = double(num_string);

%%
clear;
s_char = 'Фамилия, Имя, Отчество, , ';
s_string = string(s_char);
s_split = strsplit(s_string, ',');
s_replace = strrep(s_split, ' ', '');
s_replace(s_replace == '') = [];

%%
clear;
A = ["Фамилия" "Имя" "Отчество";
     "Иванов" "Иван" "Иванович";
     "Банкет" "Михаил" "Юрьевич";
     "Дащкова" "Олеся" "Вячеславовна";
     "Петров" "Иван" "Петрович";
     "Сидоров" "Сидр" "Иванович"];

idxIvan = find(A(:,2) == "Иван");
idxIvanovich = find(A(:,3) == "Иванович");
idxIvanIvanovich = intersect(idxIvan, idxIvanovich);

%%
clear;
c = {'Люблю тебя, Петра творенье';
    'Люблю твой строгий стройный вид'};
c_1 = c(1);
c_2 = c{1};
c_3 = c{1}(1:5);
c{1, 2} = spiral(3);
cellplot(c);

%%
clear;
A = [1 2 3; 4 5 6];
A = num2cell(A);
B = cell2mat(A);

%%
clear;
st.name = 'John';
st.age = 40;

%%
clear;
st = struct('Name', 'John', 'age', 40);
