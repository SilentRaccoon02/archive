#pragma once

struct XY
{
	int x;
	int y;

	bool operator < (const XY& point) const {
		return this->x < point.x;
	}
};

class Plant
{
private:
	std::string Name;
	int AreaC;
	int** AreaS;
	double Light[2], Temp[2], Humi[2], Acid[2];

	void copy(const Plant& other);
	void destructor();

public:
	Plant();
	Plant(int seed);
	~Plant();

	Plant(const Plant& other);
	Plant& operator = (const Plant& other);

	bool Check(int area[], int light[], int temp[], int humi[], int acid[]);
	bool isConsistentWith(const Plant& other);
	bool isConsistentWith_lite(const Plant& other);
	Plant MakeBest(const Plant& other);
	void PritnBest();

	bool operator < (const Plant& other);
	bool operator <= (const Plant& other);

	friend std::ostream& operator << (std::ostream& out, const Plant& obj);
	friend std::istream& operator >> (std::istream& in, Plant& obj);

	int GetAreaC();
	int GetAreaS(int i, int j);
};

struct Square
{
	XY sq;
	std::vector<Plant> sqPlants;
	Plant best;
};

class List
{
public:
	List();
	~List();

	void pop_front();
	void push_back(Plant data);
	void push_front(Plant data);
	void clear();
	void sort();
	void add_to_sorted(Plant data);
	void write(int area[], int light[], int temp[], int humi[], int acid[]);
	void remove(int area[], int light[], int temp[], int humi[], int acid[]);
	Square* to_array(Plant in_array[], int& sqCount);
	int GetSize();

	friend std::ostream& operator << (std::ostream& out, const List& obj);
	friend std::istream& operator >> (std::istream& in, List& obj);

private:
	class Node
	{
	public:
		Node* pNext;
		Plant data;

		Node(Plant data, Node* pNext);
	};

	int Size;
	Node* head;
	Node* tail;

	Node* merge_sort(Node* head);
	Node* merge(Node* a, Node* b);
	Node* get_middle(Node* head);
};

void fileRead(List& Plants);
int userObjects();
int typeToDo();
void setGoodConditions(List& plants);
