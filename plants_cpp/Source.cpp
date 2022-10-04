#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <set>
#include <ctime>
#include <limits>
#include "Header.h"

using namespace std;

int main()
{
	setlocale(LC_ALL, "ru");

	int readType = 0, doType = 0;

	cout << "Тип ввода: (0)чтение с клавиатуры, (1)чтение из файла, (2)заполнить случайно" << endl;

	while (true)
	{
		cin >> readType;

		if (cin.fail() || (readType != 0 && readType != 1 && readType != 2)) {
			cout << "Неверное значение" << endl;
			cin.clear();
			cin.ignore(numeric_limits < streamsize>::max(), '\n');
		}
		else
		{
			break;
		}
	}

	List Plants;

	if (readType == 0)
	{
		int objCount = userObjects();

		for (int i = 0; i < objCount; i++)
		{
			Plant Temp;

			cin >> Temp;
			Plants.push_back(Temp);
		}

		cout << endl;
	}

	if (readType == 1)
	{
		fileRead(Plants);
	}

	if (readType == 2)
	{
		int count;

		cout << "Сколько объектов создать? (1-20)" << endl;

		while (true)
		{
			cin >> count;

			if (cin.fail() || count < 1 || count > 100)
			{
				cout << "Неверное значение" << endl;
				cin.clear();
				cin.ignore(numeric_limits < streamsize>::max(), '\n');
			}
			else
			{
				break;
			}
		}
		for (int i = 0; i < count; i++)
		{
			Plant temp(i - i * i);
			Plants.push_back(temp);
		}
		cout << "Выполнено" << endl << endl;
	}

	do
	{
		doType = typeToDo();

		if (doType == 1)
		{
			cout << Plants;
		}

		if (doType == 2)
		{
			ofstream file;
			string path;

			cout << "Введите имя файла: ";
			cin >> path;
			file.open(path);
			file << Plants;
			file.close();
			cout << "Выполнено" << endl << endl;
		}

		if (doType == 3)
		{
			Plants.sort();
			cout << "Выполнено" << endl << endl;
		}

		if (doType == 4 || doType == 5)
		{
			int Area[4], Light[2], Temp[2], Humi[2], Acid[2];

			cout << "Прямоугольник квадратов: ";
			while (true) {
				cin >> Area[0] >> Area[1] >> Area[2] >> Area[3];
				if (cin.fail() || Area[0] < -1000 || Area[0] > 1000
					|| Area[1] < -1000 || Area[1] > 1000
					|| Area[2] < -1000 || Area[2] > 1000
					|| Area[3] < -1000 || Area[3] > 1000) {
					cout << "Неверное значение" << endl;
					cin.clear();
					cin.ignore(numeric_limits < streamsize>::max(), '\n');
				}
				else break;
			}
			cout << "Диапазон допустимой освещенности: ";
			while (true) {
				cin >> Light[0] >> Light[1];
				if (cin.fail() || Light[0] < -1000 || Light[0] > 1000
					|| Light[1] < -1000 || Light[1] > 1000) {
					cout << "Неверное значение" << endl;
					cin.clear();
					cin.ignore(numeric_limits < streamsize>::max(), '\n');
				}
				else break;
			}
			cout << "                    температуры: ";
			while (true) {
				cin >> Temp[0] >> Temp[1];
				if (cin.fail() || Temp[0] < -1000 || Temp[0] > 1000
					|| Temp[1] < -1000 || Temp[1] > 1000) {
					cout << "Неверное значение" << endl;
					cin.clear();
					cin.ignore(numeric_limits < streamsize>::max(), '\n');
				}
				else break;
			}
			cout << "                    влажности: ";
			while (true) {
				cin >> Humi[0] >> Humi[1];
				if (cin.fail() || Humi[0] < -1000 || Humi[0] > 1000
					|| Humi[1] < -1000 || Humi[1] > 1000) {
					cout << "Неверное значение" << endl;
					cin.clear();
					cin.ignore(numeric_limits < streamsize>::max(), '\n');
				}
				else break;
			}
			cout << "                    кислотности: ";
			while (true) {
				cin >> Acid[0] >> Acid[1];
				if (cin.fail() || Acid[0] < -1000 || Acid[0] > 1000
					|| Acid[1] < -1000 || Acid[1] > 1000) {
					cout << "Неверное значение" << endl;
					cin.clear();
					cin.ignore(numeric_limits < streamsize>::max(), '\n');
				}
				else break;
			}

			if (doType == 4)
			{
				Plants.write(Area, Light, Temp, Humi, Acid);
			}
			else
			{
				Plants.remove(Area, Light, Temp, Humi, Acid);
				cout << "Выполнено" << endl;
				cout << endl;
			}
		}

		if (doType == 6)
		{
			Plant temp;
			cin >> temp;
			Plants.add_to_sorted(temp);
			cout << endl << endl;
		}

		if (doType == 7)
		{
			Plants.clear();
			cout << "Выполнено" << endl << endl;
		}

		if (doType == 8)
		{
			Plants.clear();
			fileRead(Plants);
		}

		if (doType == 9)
		{
			if (Plants.GetSize() < 1)
			{
				cout << "Список пуст" << endl << endl;
			}
			else
			{
				setGoodConditions(Plants);
			}
		}
	}
	while (doType);

	return 0;
}
