#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <set>
#include <ctime>
#include <limits>
#include "Header.h"

using namespace std;

Plant::Plant()
{
	Name = "0";
	AreaC = 1;
	AreaS = new int* [AreaC]; AreaS[0] = new int[2];
	AreaS[0][0] = 0; AreaS[0][1] = 0;
	Light[0] = 0; Light[1] = 0;
	Temp[0] = 0; Temp[1] = 0;
	Humi[0] = 0; Humi[1] = 0;
	Acid[0] = 0; Acid[1] = 0;
}

Plant::Plant(int seed)
{
	srand(seed);
	Name = to_string(10 + rand() % 90);
	AreaC = 1 + rand() % 4;

	AreaS = new int* [AreaC];

	for (int i = 0; i < AreaC; i++)
	{
		AreaS[i] = new int[2];

		AreaS[i][0] = 0 + rand() % 20;
		AreaS[i][1] = 0 + rand() % 20;
	}

	Light[0] = 0 + rand() % 10; Light[1] = 10 + rand() % 20;
	Temp[0] = 0 + rand() % 10; Temp[1] = 10 + rand() % 20;
	Humi[0] = 0 + rand() % 10; Humi[1] = 10 + rand() % 20;
	Acid[0] = 0 + rand() % 10; Acid[1] = 10 + rand() % 20;
}

void Plant::copy(const Plant& other)
{
	this->Name = other.Name;
	this->AreaC = other.AreaC;
	this->AreaS = new int* [this->AreaC];

	for (int i = 0; i < this->AreaC; i++)
	{
		this->AreaS[i] = new int[2];
		this->AreaS[i][0] = other.AreaS[i][0];
		this->AreaS[i][1] = other.AreaS[i][1];
	}

	this->Light[0] = other.Light[0];
	this->Light[1] = other.Light[1];
	this->Temp[0] = other.Temp[0];
	this->Temp[1] = other.Temp[1];
	this->Humi[0] = other.Humi[0];
	this->Humi[1] = other.Humi[1];
	this->Acid[0] = other.Acid[0];
	this->Acid[1] = other.Acid[1];
}

void Plant::destructor()
{
	for (int i = 0; i < AreaC; i++)
	{
		delete[] AreaS[i];
	}

	delete[] AreaS;
}

Plant::Plant(const Plant& other)
{
	copy(other);
}

Plant& Plant::operator = (const Plant& other)
{
	destructor();
	copy(other);
	return *this;
}

Plant::~Plant()
{
	destructor();
}

ostream& operator << (ostream& out, const Plant& obj)
{
	if (&out == &cout)
	{
		out << "Название: " << obj.Name << endl;
		out << "Занимаемые квадраты: ";

		for (int i = 0; i < obj.AreaC; i++)
		{
			out << "(" << obj.AreaS[i][0] << ", " << obj.AreaS[i][1] << ") ";
		}

		out << "\nДиапазон допустимой освещенности: [" << obj.Light[0] << ", " << obj.Light[1] << "]" << endl;
		out << "                    температуры: [" << obj.Temp[0] << ", " << obj.Temp[1] << "]" << endl;
		out << "                    влажности: [" << obj.Humi[0] << ", " << obj.Humi[1] << "]" << endl;
		out << "                    кислотности: [" << obj.Acid[0] << ", " << obj.Acid[1] << "]" << endl;
	}
	else
	{
		out << obj.Name << endl;
		
		for (int i = 0; i < obj.AreaC; i++)
		{
			out << obj.AreaS[i][0] << " " << obj.AreaS[i][1];
			out << " ";
		}

		out << endl << obj.Light[0] << " " << obj.Light[1] << endl;
		out << obj.Temp[0] << " " << obj.Temp[1] << endl;
		out << obj.Humi[0] << " " << obj.Humi[1] << endl;
		out << obj.Acid[0] << " " << obj.Acid[1];
	}

	return out;
}

istream& operator >> (istream& in, Plant& obj)
{
	for (int i = 0; i < obj.AreaC; i++)
	{
		delete[] obj.AreaS[i];
	}

	delete[] obj.AreaS;

	if (&in == &cin)
	{
		cout << "Название: ";
		in >> obj.Name;
		cout << "Количество квадратов: ";

		while (true)
		{
			in >> obj.AreaC;

			if (in.fail() || obj.AreaC < 1 || obj.AreaC > 1000) {
				cout << "Неверное значение" << endl;
				in.clear();
				in.ignore(numeric_limits < streamsize>::max(), '\n');
			}
			else
			{
				break;
			}
		}

		obj.AreaS = new int* [obj.AreaC];

		for (int i = 0; i < obj.AreaC; i++)
		{
			obj.AreaS[i] = new int[2];

			while (true)
			{
				in >> obj.AreaS[i][0] >> obj.AreaS[i][1];

				if (in.fail() || obj.AreaS[i][0] < 0 || obj.AreaS[i][0] > 1000
					|| obj.AreaS[i][1] < 0 || obj.AreaS[i][1] > 1000)
				{
					cout << "Неверное значение" << endl;
					in.clear();
					in.ignore(numeric_limits < streamsize>::max(), '\n');
				}
				else
				{
					break;
				}
			}
		}

		cout << "Диапазон допустимой освещенности: ";

		while (true)
		{
			in >> obj.Light[0] >> obj.Light[1];

			if (in.fail() || obj.Light[0] < 0 || obj.Light[0] > 1000
				|| obj.Light[1] < 0 || obj.Light[1] > 1000)
			{
				cout << "Неверное значение" << endl;
				in.clear();
				in.ignore(numeric_limits < streamsize>::max(), '\n');
			}
			else
			{
				break;
			}
		}

		cout << "                    температуры: ";

		while (true)
		{
			in >> obj.Temp[0] >> obj.Temp[1];

			if (in.fail() || obj.Temp[0] < 0 || obj.Temp[0] > 1000
				|| obj.Temp[1] < 0 || obj.Temp[1] > 1000)
			{
				cout << "Неверное значение" << endl;
				in.clear();
				in.ignore(numeric_limits < streamsize>::max(), '\n');
			}
			else
			{
				break;
			}
		}

		cout << "                    влажности: ";

		while (true)
		{
			in >> obj.Humi[0] >> obj.Humi[1];

			if (in.fail() || obj.Humi[0] < 0 || obj.Humi[0] > 1000
				|| obj.Humi[1] < 0 || obj.Humi[1] > 1000)
			{
				cout << "Неверное значение" << endl;
				in.clear();
				in.ignore(numeric_limits < streamsize>::max(), '\n');
			}
			else
			{
				break;
			}

		}

		cout << "                    кислотности: ";

		while (true)
		{
			in >> obj.Acid[0] >> obj.Acid[1];

			if (in.fail() || obj.Acid[0] < 0 || obj.Acid[0] > 1000
				|| obj.Acid[1] < 0 || obj.Acid[1] > 1000)
			{
				cout << "Неверное значение" << endl;
				in.clear();
				in.ignore(numeric_limits < streamsize>::max(), '\n');
			}
			else
			{
				break;
			}
		}
	}
	else {
		string help = "";
		char slice;
		int j = 0, count = 0;
		obj.AreaC = 0;

		in >> obj.Name;
		in.get();

		while (help != "\n")
		{
			count++;
			in.get(slice);
			help = slice;

			if (help == " ")
			{
				obj.AreaC++;
			}
		}

		obj.AreaC++;
		obj.AreaC /= 2;
		count++;
		in.seekg(-count, ios::cur);

		obj.AreaS = new int* [obj.AreaC];

		for (int i = 0; i < obj.AreaC; i++)
		{
			obj.AreaS[i] = new int[2];
			in >> obj.AreaS[i][0] >> obj.AreaS[i][1];
		}

		in >> obj.Light[0] >> obj.Light[1];
		in >> obj.Temp[0] >> obj.Temp[1];
		in >> obj.Humi[0] >> obj.Humi[1];
		in >> obj.Acid[0] >> obj.Acid[1];
	}

	return in;
}

bool Plant::Check(int area[], int light[], int temp[], int humi[], int acid[])
{
	bool check = true;

	for (int i = 0; i < AreaC; i++)
	{
		if (AreaS[i][0] >= area[0] && AreaS[i][0] <= area[2]
			&& AreaS[i][1] >= area[1] && AreaS[i][1] <= area[3])
		{
			check = true;
			break;
		}
		else
		{
			check = false;
		}
	}

	if (this->Light[0] > light[0] || this->Light[1] < light[1])
	{
		check = false;
	}

	if (this->Temp[0] > temp[0] || this->Temp[1] < temp[1])
	{
		check = false;
	}

	if (this->Humi[0] > humi[0] || this->Humi[1] < humi[1])
	{
		check = false;
	}

	if (this->Acid[0] > acid[0] || this->Acid[1] < acid[1])
	{
		check = false;
	}
	 
	return check;
}

bool Plant::isConsistentWith(const Plant& other)
{
	bool check = true;

	for (int i = 0; i < this->AreaC; i++)
	{
		for (int j = 0; j < other.AreaC; j++)
		{
			if (this->AreaS[i][0] == other.AreaS[j][0]
				&& this->AreaS[i][1] == other.AreaS[j][1])
			{
				check = false;
			}
		}
	}

	if (check)
	{
		cout << "Одинаковые квадраты: false\nreturn 1" << endl;
		return true;
	}

	if (!check)
	{
		cout << "Одинаковые квадраты: true" << endl;

		check = true;

		if (this->Light[1] >= other.Light[0] && this->Light[1] <= other.Light[1]
			|| this->Light[0] >= other.Light[0] && this->Light[0] <= other.Light[1]);
		else
		{
			check = false;
		}

		if (this->Temp[1] >= other.Temp[0] && this->Temp[1] <= other.Temp[1]
			|| this->Temp[0] >= other.Temp[0] && this->Temp[0] <= other.Temp[1]);
		else
		{
			check = false;
		}

		if (this->Humi[1] >= other.Humi[0] && this->Humi[1] <= other.Humi[1]
			|| this->Humi[0] >= other.Humi[0] && this->Humi[0] <= other.Humi[1]);
		else
		{
			check = false;
		}

		if (this->Acid[1] >= other.Acid[0] && this->Acid[1] <= other.Acid[1]
			|| this->Acid[0] >= other.Acid[0] && this->Acid[0] <= other.Acid[1]);
		else
		{
			check = false;
		}
	}

	if (!check)
	{
		cout << "Совместимы: false\nreturn 0" << endl;
		return false;
	}

	if (check)
	{
		cout << "Совместимы: true\nreturn 1" << endl;
	}

	return true;
}

bool Plant::isConsistentWith_lite(const Plant& other)
{
	if (this->Light[1] >= other.Light[0] && this->Light[1] <= other.Light[1]
		|| this->Light[0] >= other.Light[0] && this->Light[0] <= other.Light[1]);
	else
	{
		return false;
	}

	if (this->Temp[1] >= other.Temp[0] && this->Temp[1] <= other.Temp[1]
		|| this->Temp[0] >= other.Temp[0] && this->Temp[0] <= other.Temp[1]);
	else
	{
		return false;
	}

	if (this->Humi[1] >= other.Humi[0] && this->Humi[1] <= other.Humi[1]
		|| this->Humi[0] >= other.Humi[0] && this->Humi[0] <= other.Humi[1]);
	else
	{
		return false;
	}

	if (this->Acid[1] >= other.Acid[0] && this->Acid[1] <= other.Acid[1]
		|| this->Acid[0] >= other.Acid[0] && this->Acid[0] <= other.Acid[1]);
	else
	{
		return false;
	}

	return true;
}

Plant Plant::MakeBest(const Plant& other)
{
	Plant best;
	
	best.Light[0] = max(this->Light[0], other.Light[0]);
	best.Light[1] = min(this->Light[1], other.Light[1]);

	best.Temp[0] = max(this->Temp[0], other.Temp[0]);
	best.Temp[1] = min(this->Temp[1], other.Temp[1]);

	best.Humi[0] = max(this->Humi[0], other.Humi[0]);
	best.Humi[1] = min(this->Humi[1], other.Humi[1]);

	best.Acid[0] = max(this->Acid[0], other.Acid[0]);
	best.Acid[1] = min(this->Acid[1], other.Acid[1]);

	return best;
}

void Plant::PritnBest()
{
	cout << "\nДиапазон допустимой освещенности: [" << Light[0] << ", " << Light[1] << "]" << endl;
	cout << "                    температуры: [" << Temp[0] << ", " << Temp[1] << "]" << endl;
	cout << "                    влажности: [" << Humi[0] << ", " << Humi[1] << "]" << endl;
	cout << "                    кислотности: [" << Acid[0] << ", " << Acid[1] << "]" << endl;
}

bool Plant::operator < (const Plant& other)
{
	return this->Name < other.Name;
}

bool Plant::operator <= (const Plant& other)
{
	return this->Name <= other.Name;
}

int Plant::GetAreaC()
{
	return AreaC;
}

int Plant::GetAreaS(int i, int j)
{
	return AreaS[i][j];
}
