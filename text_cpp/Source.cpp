#include <iostream>
#include <fstream>
#include <string>
#include <regex>
#include <vector>
#include <Windows.h>

using namespace std;

//makeCommon tolower off

class Word
{
public:
	Word()
	{
		Count = 0;
		EndPhrase = false;
	}
	
	void ConsolePrint()
	{
		cout << String << "=" << Count << "    ";
		for (int i = 0; i < Nears.size(); i++)
		{
			cout << Nears[i] << " ";
		}
		cout << endl;
	}

	void PlusCount()
	{
		Count++;
	}

	void MakeVector(int size)
	{
		Nears.resize(size);
		EndPhrase = false;
	}

	void PlusNear(int index, int count)
	{
		Nears[index] += (double)1 / count;
	}

	void SetString(string& string)
	{
		String = string;
	}

	void FileWrite(ostream& file)
	{
		file << String;
		for (int i = 0; i < Nears.size(); i++)
		{
			file << " " << Nears[i];
		}
		file << endl;
	}

	void FromFile(istream& file, int count)
	{
		Nears.resize(count);

		for (int i = 0; i < Nears.size(); i++)
		{
			file >> Nears[i];
		}

	}

	bool GetEndPhrase()
	{
		return EndPhrase;
	}

	int GetCount()
	{
		return Count;
	}

	string GetString()
	{
		return String;
	}

	vector<double> GetNears()
	{
		return Nears;
	}

	double Calculate(const Word& other)
	{
		double dif, sum = 0;

		for (int i = 0; i < this->Nears.size(); i++)
		{
			dif = other.Nears[i] - this->Nears[i];
			dif = pow(dif, 2);
			sum += dif;
		}

		return sqrt(sum);
	}

	bool operator > (const Word& other)
	{
		return this->String > other.String;
	}

	bool operator < (const Word& other)
	{
		return this->String < other.String;
	}

	bool operator != (const Word& other)
	{
		return this->String != other.String;
	}

	Word& operator = (const Word& other)
	{
		this->String = other.String;
		this->Count = other.Count;
		this->EndPhrase = other.EndPhrase;
		return *this;
	}

	friend istream& operator >> (istream& in, Word& object);

private:
	string String;
	int Count;
	bool EndPhrase;
	vector<double> Nears;

	void setString(istream& in)
	{
		in >> String;
		EndPhrase = makeCommon(String);
		Count = 1;
	}

	bool makeCommon(string& in)
	{
		bool endPhrase;
		cmatch result;
		regex regular("([\"«]?)""([A-Яа-я-]*)""([\\W]?)");

		regex_match(in.c_str(), result, regular);
		endPhrase = result[3] != "";
		in = result[2];
		//transform(in.begin(), in.end(), in.begin(), ::tolower);
		return endPhrase;
	}
};

istream& operator >> (istream& in, Word& object)
{
	object.setString(in);
	return in;
}

class Text
{
public:
	int FileRead(istream& in)
	{
		int wordsCount = 0;
		string buffer;

		while (!in.eof())
		{
			in >> buffer;
			wordsCount++;
		}

		if (wordsCount <= 10)
		{
			cout << "Текст слишком короткий" << endl;
			return 0;
		}

		cout << "Количество слов " << wordsCount << endl;
		
		in.clear();
		in.seekg(0);

		int part = 0, startPart = 0, endPart = 0;

		cout << "Чтение файла ";
		Words.reserve(wordsCount);

		if (wordsCount > 100)
		{
			part = wordsCount / 100;
			startPart = wordsCount - part * 99;

			Word temp;
			
			in >> temp;
			Words.push_back(temp);

			for (int i = 1; i < startPart; i++)
			{
				partRead(in);
			}

			cout << 1 << "%";

			for (int i = 1; i < 100; i++)
			{
				endPart = startPart + part;

				for (int i = startPart; i < endPart; i++)
				{
					partRead(in);
				}

				startPart = endPart;

				if ((1 + 1 * i)-1 < 10)
				{
					cout << "\b\b" << 1 + 1 * i << "%";
				}
				else
				{
					cout << "\b\b\b" << 1 + 1 * i << "%";
				}
			}
		}
		else
		{
			if (wordsCount > 10)
			{
				part = wordsCount / 10;
				startPart = wordsCount - part * 9;

				Word temp;

				in >> temp;
				Words.push_back(temp);

				for (int i = 1; i < startPart; i++)
				{
					partRead(in);
				}

				cout << 10 << "%";

				for (int i = 1; i < 10; i++)
				{
					endPart = startPart + part;

					for (int i = startPart; i < endPart; i++)
					{
						partRead(in);
					}

					startPart = endPart;
					cout << "\b\b\b" << 10 + 10 * i << "%";
				}
			}
		}

		Words.shrink_to_fit();
		cout << endl;

		if (Words.size() <= 10)
		{
			cout << "Малое разнообразие слов" << endl;
			return 0;
		}

		return wordsCount;
	}

	Word GetWord(string& wordName, int& index)
	{
		Word temp;

		temp.SetString(wordName);

		index = binarySearch(Words, 0, Words.size() - 1, temp);

		if (index != -1)
		{
			return Words[index];
		}
		else
		{
			return Words[0];
		}
	}

	string GetString(int index)
	{
		return Words[index].GetString();
	}

	vector<double> CalculateSims(int index)
	{
		vector<double> sims;

		sims.reserve(Words.size());

		for (int i = 0; i < Words.size(); i++)
		{
			sims.push_back(Words[index].Calculate(Words[i]));
		}

		return sims;
	}

	void FileAn(istream& in, int wordsCount)
	{
		cout << "Анализ файла ";

		in.clear();
		in.seekg(0);

		Word minOne, minTwo;

		in >> minTwo;
		in >> minOne;

		int minOneI = findOrig(minOne),
			minTwoI = findOrig(minTwo),
			minOneC = Words[minOneI].GetCount(),
			minTwoC = Words[minTwoI].GetCount();

		if (minOne != minTwo)
		{
			if (!minTwo.GetEndPhrase())
			{
				Words[minTwoI].PlusNear(minOneI, minTwoC);
				Words[minOneI].PlusNear(minTwoI, minOneC);
			}
		}

		int part = 0, startPart = 0, endPart = 0;

		if (wordsCount > 100)
		{
			part = wordsCount / 100;
			startPart = wordsCount - part * 99;

			for (int i = 2; i < startPart; i++)
			{
				partAn(in, minTwo, minOne, minTwoI, minOneI, minTwoC, minOneC);
			}

			cout << 1 << "%";

			for (int i = 1; i < 100; i++)
			{
				endPart = startPart + part;

				for (int i = startPart; i < endPart; i++)
				{
					partAn(in, minTwo, minOne, minTwoI, minOneI, minTwoC, minOneC);
				}

				startPart = endPart;

				if ((1 + 1 * i) - 1 < 10)
				{
					cout << "\b\b" << 1 + 1 * i << "%";
				}
				else
				{
					cout << "\b\b\b" << 1 + 1 * i << "%";
				}
			}
		}
		else
		{
			if (wordsCount > 10)
			{
				part = wordsCount / 10;
				startPart = wordsCount - part * 9;

				for (int i = 2; i < startPart; i++)
				{
					partAn(in, minTwo, minOne, minTwoI, minOneI, minTwoC, minOneC);
				}

				cout << 10 << "%";

				for (int i = 1; i < 10; i++)
				{
					endPart = startPart + part;

					for (int i = startPart; i < endPart; i++)
					{
						partAn(in, minTwo, minOne, minTwoI, minOneI, minTwoC, minOneC);
					}

					startPart = endPart;
					cout << "\b\b\b" << 10 + 10 * i << "%";
				}
			}
		}
		cout << endl;
	}

	void MakeMatrix()
	{
		for (int i = 0; i < Words.size(); i++)
		{
			Words[i].MakeVector(Words.size());
		}
	}

	void FileWrite(const string& outName)
	{
		ofstream file(outName);
		file << Words.size() << endl;

		int part = 0, startPart = 0, endPart = 0;

		cout << "Запись файла ";

		if (Words.size() > 100)
		{
			part = Words.size() / 100;

			startPart = Words.size() - part * 99;

			for (int i = 0; i < startPart; i++)
			{
				Words[i].FileWrite(file);
			}

			cout << "0" << 1 << "%";

			for (int i = 1; i < 100; i++)
			{
				endPart = startPart + part;

				for (int i = startPart; i < endPart; i++)
				{
					Words[i].FileWrite(file);
				}

				startPart = endPart;

				if (1 + 1 * i < 10)
				{
					cout << "\b\b\b0" << 1 + 1 * i << "%";
				}
				else
				{
					cout << "\b\b\b" << 1 + 1 * i << "%";
				}
			}
		}
		else
		{
			if (Words.size() > 10)
			{
				part = Words.size() / 10;

				startPart = Words.size() - part * 9;

				for (int i = 0; i < startPart; i++)
				{
					Words[i].FileWrite(file);
				}

				cout << 10 << "%";

				for (int i = 1; i < 10; i++)
				{
					endPart = startPart + part;

					for (int i = startPart; i < endPart; i++)
					{
						Words[i].FileWrite(file);
					}

					startPart = endPart;

					cout << "\b\b\b" << 10 + 10 * i << "%";
				}
			}
		}

		file.close();
		cout << endl;
	}

	void FromFile(const string& inName)
	{
		ifstream file(inName);
		int count;

		file >> count;
		Words.reserve(count);

		int part = 0, startPart = 0, endPart = 0;

		cout << "Чтение файла ";

		if (Words.capacity() > 100)
		{
			part = Words.capacity() / 100;

			startPart = Words.capacity() - part * 99;

			for (int i = 0; i < startPart; i++)
			{
				partFrom(count, file);
			}

			cout << "0" << 1 << "%";

			for (int i = 1; i < 100; i++)
			{
				endPart = startPart + part;

				for (int i = startPart; i < endPart; i++)
				{
					partFrom(count, file);
				}

				startPart = endPart;

				if (1 + 1 * i < 10)
				{
					cout << "\b\b\b0" << 1 + 1 * i << "%";
				}
				else
				{
					cout << "\b\b\b" << 1 + 1 * i << "%";
				}
			}
		}
		else
		{
			if (Words.capacity() > 10)
			{
				part = Words.capacity() / 10;

				startPart = Words.capacity() - part * 9;

				for (int i = 0; i < startPart; i++)
				{
					partFrom(count, file);
				}

				cout << 10 << "%";

				for (int i = 1; i < 10; i++)
				{
					endPart = startPart + part;

					for (int i = startPart; i < endPart; i++)
					{
						partFrom(count, file);
					}

					startPart = endPart;

					cout << "\b\b\b" << 10 + 10 * i << "%";
				}
			}
		}
		file.close();
		cout << endl;
	}

private:
	vector<Word> Words;

	void partRead(istream& in)
	{
		Word temp;

		in >> temp;
		
		int index = binarySearch(Words, 0, Words.size() - 1, temp);

		if (index == -1)
		{
			Words.push_back(temp);

			for (int i = Words.size() - 1; i > 0 && Words[i - 1] > Words[i]; i--)
			{
				swap(Words[i - 1], Words[i]);
			}
		}
		else
		{
			Words[index].PlusCount();
		}
	} 

	void partAn(istream& in,
		Word& minTwo, Word& minOne,
		int& minTwoI, int& minOneI,
		int& minTwoC, int& minOneC)
	{
		Word temp;

		in >> temp;

		int tempI = findOrig(temp),
			tempC = Words[tempI].GetCount();

		if (!minOne.GetEndPhrase())
		{
			if (minOne != temp)
			{
				Words[minOneI].PlusNear(tempI, minOneC);
				Words[tempI].PlusNear(minOneI, tempC);
			}

			if (!minTwo.GetEndPhrase())
			{
				if (minTwo != temp)
				{
					Words[minTwoI].PlusNear(tempI, minTwoC);
					Words[tempI].PlusNear(minTwoI, tempC);
				}
			}
		}

		minTwo = minOne;
		minTwoI = minOneI;
		minTwoC = minOneC;
		minOne = temp;
		minOneI = tempI;
		minOneC = tempC;
	}

	void partFrom(int& count, istream& file)
	{
		Word temp;

		file >> temp;
		temp.FromFile(file, count);
		Words.push_back(temp);
	}

	int findOrig(Word& object)
	{
		return binarySearch(Words, 0, Words.size() - 1, object);
	}

	int binarySearch(vector<Word> arr, int left, int right, Word key)
	{
		int midd = 0;

		while (true)
		{
			midd = (left + right) / 2;

			if (key < arr[midd])
			{
				right = midd - 1;
			}
			else
			{
				if (key > arr[midd])
				{
					left = midd + 1;
				}
				else
				{
					return midd;
				}
			}

			if (left > right)
			{
				return -1;
			}
		}
	}
};

class DataOut
{
public:
	DataOut()
	{
		Count = 0;
		Index = 0;
	}

	bool CopyWord(Text& text, string& wordName)
	{
		int index = -1;
		Word other = text.GetWord(wordName, index);

		if (index == -1)
		{
			return false;
		}

		vector<double> tempVectorNears = other.GetNears();

		Nears.reserve(tempVectorNears.size());

		for (int i = 0; i < tempVectorNears.size(); i++)
		{
			Near tempNear;

			tempNear.index = i;
			tempNear.value = tempVectorNears[i];

			Nears.push_back(tempNear);
		}

		vector<double> tempVectorSims = text.CalculateSims(index);

		Sims.reserve(tempVectorSims.size());

		for (int i = 0; i < tempVectorSims.size(); i++)
		{
			Sim tempSim;

			tempSim.index = i;
			tempSim.value = tempVectorSims[i];

			Sims.push_back(tempSim);
		}

		this->String = other.GetString();
		this->Count = other.GetCount();

		Index = index;
		return true;
	}
	
	void ConsolePrint(Text& text)
	{
		cout << String << " (" << Index << ", " << Count << ")" << endl;

		int i = 0;

		cout <<endl <<"Близость" << endl;

		for (i = Nears.size() - 1; i >= Nears.size() - 10; i--)
		{

			cout << text.GetString(Nears[i].index);

			for (int j = 0; j < 32 - text.GetString(Nears[i].index).length(); j++)
			{
				cout << " ";
			}

			cout << "(" << Nears[i].index << ", " << Nears[i].value << ")" << endl;
			
				
		}

		cout << endl << "Схожесть" << endl;
		i = 0;

		for (i; i < 10; i++)
		{
			cout << text.GetString(Sims[i].index);

			for (int j = 0; j < 32 - text.GetString(Sims[i].index).length(); j++)
			{
				cout << " ";
			}

			cout << "(" << Sims[i].index << ", " << Sims[i].value << ")" << endl;
		}
	}

	void SortForNears()
	{
		sort(Nears.begin(), Nears.end());
	}

	void SortForSims()
	{
		sort(Sims.begin(), Sims.end());
	}

private:
	string String;
	int Count;
	int Index;

	class Near
	{
	public:
		int index = 0;
		double value = 0;

		bool operator < (const Near& other)
		{
			return this->value < other.value;
		}
	};

	class Sim
	{
	public:
		int index = 0;
		double value = 0;

		bool operator < (const Sim& other)
		{
			return this->value < other.value;
		}
	};

	vector<Near> Nears;
	vector<Sim> Sims;
};

int main(int argc, char* argv[])
{
	setlocale(LC_ALL, "ru");
	SetConsoleCP(1251);
	SetConsoleOutputCP(1251);

	string fileName;

	cout << ">>";
	cin >> fileName;
	fileName += ".txt";

	fstream file(fileName);
	Text Text;

	if (!file.is_open())
	{
		cout << "Файл не найден";
		return 0;
	}
	
	string type;

	cout << ">>";
	cin >> type;

	if (type != "in" && type != "an")
	{
		cout << "Неверный параметр" << endl;
		return 0;
	}

	if (type == "an")
	{
		int wordsCount = Text.FileRead(file);

		if (!wordsCount)
		{
			return 0;
		}

		Text.MakeMatrix();
		Text.FileAn(file, wordsCount);
		file.close();

		string outName;

		cout << ">>";
		cin >> outName;
		outName += ".txt";

		if (outName != "0")
		{
			Text.FileWrite(outName);
		}
	}
	else
	{
		file.close();
	}

	if (type == "in")
	{
		Text.FromFile(fileName);
	}

	string wordName;

	while (true)
	{
		cout << endl << ">>";
		cin >> wordName;

		if (wordName == "0")
		{
			break;
		}

		DataOut Out;

		if (!Out.CopyWord(Text, wordName))
		{
			cout << "Слово не найдено" << endl;
			continue;
		}
		
		Out.SortForNears();
		Out.SortForSims();
		Out.ConsolePrint(Text);
	}

	return 0;
}
