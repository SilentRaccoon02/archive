#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <set>
#include <ctime>
#include <limits>
#include "Header.h"

using namespace std;

void fileRead(List& Plants)
{
	string path;
	ifstream file;

	cout << "Введите имя файла: ";
	do
	{
		cin >> path;

		if (path == "d")
		{
			path = "file.txt"; //стандратное имя
		}

		file.open(path);

		if (!file.is_open())
		{
			cout << "Файл не найден" << endl;
		}
		else
		{
			cout << "Файл открыт" << endl;
		}
	} while (!file.is_open());

	file >> Plants;
	file.close();
	cout << endl;
}

int userObjects() 
{
	int objCount = 0;

	cout << "Сколько объектов создать? (1-10)" << endl;

	while (true)
	{
		cin >> objCount;

		if (cin.fail() || objCount < 1 || objCount > 10)
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

	return objCount;
}

int typeToDo()
{
	int doType = 0;

	cout << "(0)Finish" << endl;
	cout << "(1)Print" << endl;
	cout << "(2)WriteFile" << endl;
	cout << "(3)Sort" << endl;
	cout << "(4)CheckWrite" << endl;
	cout << "(5)CheckRemove" << endl;
	cout << "(6)AddToSorted" << endl;
	cout << "(7)Clear" << endl;
	cout << "(8)ReadFile" << endl;
	cout << "(9)setGoodConditions" << endl;

	while (true)
	{
		cin >> doType;

		if (cin.fail() || doType < 0 || doType > 9)
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

	return doType;
}

void setGoodConditions(List& in)
{
	int size = in.GetSize(), sqCount;
	Plant* plants = new Plant[size];
	Square* squares = in.to_array(plants, sqCount);

	for (int i = 0; i < sqCount; i++)
	{
		for (int k = 0; k < size; k++)
		{
			int count = plants[k].GetAreaC();

			for (int j = 0; j < count; j++)
			{
				XY xy;

				xy.x = plants[k].GetAreaS(j, 0);
				xy.y = plants[k].GetAreaS(j, 1);

				if (squares[i].sq.x == xy.x && squares[i].sq.y == xy.y)
				{
					squares[i].sqPlants.push_back(plants[k]);
					break;
				}
			}
		}
	}

	for (int i = 0; i < sqCount; i++)
	{
		if (squares[i].sqPlants.size() > 0)
		{
			bool check = true;

			Plant best = squares[i].sqPlants[0];

			for (int j = 0; j < squares[i].sqPlants.size(); j++)
			{
				if (best.isConsistentWith_lite(squares[i].sqPlants[j]))
				{
					best = best.MakeBest(squares[i].sqPlants[j]);
				}
				else
				{
					check = false;
					break;
				}
			}
			if (check)
			{
				squares[i].best = best;
			}

		}
	}

	for (int i = 0; i < sqCount; i++)
	{
		cout << "square: " << squares[i].sq.x << " " << squares[i].sq.y << endl;
		cout << "size:" << squares[i].sqPlants.size() << endl;
		cout << "best:";
		squares[i].best.PritnBest();

		cout << "plants:" << endl;

		for (int j = 0; j < squares[i].sqPlants.size(); j++)
		{
			cout << squares[i].sqPlants[j];
		}
		cout << endl;
	}

	delete[] squares;
	delete[] plants;
}
