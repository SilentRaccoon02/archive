%%
clear;
errordlg('Error!');
helpdlg('Help!');
msgbox('Msg');

%%
clear;
C = uicontrol('Style', 'pushbutton', 'String', 'Help');

%%
clear;
lines = 1;
A = pi;
default_val = {'Val1', 'Val2', num2str(A)};
New = inputdlg({'Bar_1', 'Bar_2', 'Bar_3'}, 'InputData', lines, default_val, 'on');

%%
clear;
waitbar(3/10, 'Wait', 'Position', [100,100, 300, 60])

%%
clear;
questdlg('Question', 'Name', 'Opt1', 'Opt2', 'Opt3');

%%
clear;
directory = uigetfile();

%%
clear;
Filter = {'*.txt'};
[FileID, PathID] = uigetfile(Filter);

%%
clear;
M = menu('Name', 'Btn1', 'Btn2', 'Btn3');

%%
clear;
guide
