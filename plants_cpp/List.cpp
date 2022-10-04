#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <set>
#include <ctime>
#include <limits>
#include "Header.h"

using namespace std;

List::Node::Node(Plant data = Plant(), Node* pNext = nullptr)
{
	this->data = data;
	this->pNext = pNext;
}

List::List()
{
	Size = 0;
	head = nullptr;
	tail = nullptr;
}

List::~List()
{
	clear();
}

void List::pop_front()
{
	Node* temp = head;

	head = head->pNext;

	if (head == nullptr)
	{
		tail = nullptr;
	}

	delete temp;
	Size--;
}

void List::push_back(Plant data)
{
	if (head == nullptr)
	{
		head = new Node(data);
		tail = head;
	}
	else
	{
		tail->pNext = new Node(data);
		tail = tail->pNext;
	}
	Size++;
}

void List::push_front(Plant data)
{
	head = new Node(data, head);
	Size++;
}

void List::clear()
{
	while (Size)
	{
		pop_front();
	}
}

void List::sort()
{
	if (Size > 1)
	{
		head = merge_sort(head);

		Node* current = head;

		while (current->pNext != nullptr)
		{
			current = current->pNext;
		}

		tail = current;
	}
}

void List::add_to_sorted(Plant data)
{
	if (Size == 0)
	{
		push_back(data);
	}
	else
	{
		if (data < head->data)
		{
			push_front(data);
		}
		else
		{
			if (head->pNext == nullptr)
			{
				if (head->data <= data)
				{
					push_back(data);
				}
			}
			else
			{
				Node* previous = head;

				while (previous->pNext->data < data && previous->pNext->pNext != nullptr)
				{
					previous = previous->pNext;
				}

				if (previous->pNext->pNext == nullptr && previous->pNext->data < data)
				{
					push_back(data);
				}
				else
				{
					Node* newNode = new Node(data, previous->pNext);

					previous->pNext = newNode;
					Size++;
				}
			}
		}
	}
}

void List::write(int area[], int light[], int temp[], int humi[], int acid[])
{
	for (Node* current = head; current != nullptr; current = current->pNext)
	{
		if (current->data.Check(area, light, temp, humi, acid))
		{
			cout << current->data;
			cout << endl;
		}
	}
}

void List::remove(int area[], int light[], int temp[], int humi[], int acid[])
{
	if (Size == 0)
	{
		return;
	}

	while (head != nullptr && head->data.Check(area, light, temp, humi, acid))
	{
		pop_front();
	}

	if (head == nullptr)
	{
		return;
	}
	
	Node* previous = head;

	while (previous->pNext != nullptr)
	{
		if (previous->pNext->data.Check(area, light, temp, humi, acid))
		{
			Node* toDelete = previous->pNext;

			if (toDelete->pNext != nullptr)
			{
				previous->pNext = toDelete->pNext;
			}
			else
			{
				previous->pNext = nullptr;
				tail = previous;
			}

			delete toDelete;
			Size--;
		}
		else
		{
			previous = previous->pNext;
		}
	}
}

Square* List::to_array(Plant in_array[], int& sqCount)
{
	List::Node* current = head;
	set<XY> squares;

	for (int i = 0; i < Size; i++)
	{
		in_array[i] = current->data;

		for (int j = 0; j < in_array[i].GetAreaC(); j++)
		{
			XY xy;

			xy.x = in_array[i].GetAreaS(j, 0);
			xy.y = in_array[i].GetAreaS(j, 1);

			squares.insert(xy);
		}

		current = current->pNext;
	}

	sqCount = squares.size();

	Square* out = new Square[sqCount];
	int i = 0;
	std::set<XY>::iterator it = squares.begin();

	while(it != squares.end())
	{
		out[i].sq.x = (*it).x;
		out[i].sq.y = (*it).y;

		it++;
		i++;
	}

	return out;
}

List::Node* List::merge_sort(Node* head)
{
	if (head == nullptr || head->pNext == nullptr)
	{
		return head;
	}

	Node* middle = get_middle(head);
	Node* left_head = head;
	Node* right_head = middle->pNext;
	middle->pNext = nullptr;

	return merge(merge_sort(left_head), merge_sort(right_head));
}

List::Node* List::merge(Node* a, Node* b)
{
	Node* temp_head = new Node();
	Node* current = temp_head;

	for (; a != nullptr && b != nullptr; current = current->pNext)
	{
		if (a->data <= b->data)
		{
			current->pNext = a;
			a = a->pNext;
		}
		else
		{
			current->pNext = b;
			b = b->pNext;
		}
	}
	current->pNext = (a == nullptr) ? b : a;

	Node* toReturn = temp_head->pNext;
	delete temp_head;

	return toReturn;
}

List::Node* List::get_middle(Node* head)
{
	if (head == nullptr)
	{
		return head;
	}

	Node* slow = head;
	Node* fast = head;

	while (fast->pNext != nullptr && fast->pNext->pNext != nullptr)
	{
		slow = slow->pNext;
		fast = fast->pNext->pNext;
	}
	return slow;
}

int List::GetSize()
{
	return Size;
}

std::ostream& operator<<(std::ostream& out, const List& obj)
{
	if (&out == &cout)
	{
		if (obj.Size == 0)
		{
			out << "Список пуст" << endl << endl;
			return out;
		}

		for (List::Node* current = obj.head; current != nullptr; current = current->pNext)
		{
			out << current->data;
			out << endl;
		}
	}
	else
	{
		if (obj.Size == 0)
		{
			out << "empty";
			return out;
		}

		List::Node * current = obj.head;

		for (;current->pNext != nullptr; current = current->pNext)
		{
			out << current->data;
			out << endl << endl;
		}

		out << current->data;
	}

	return out;
}

std::istream& operator>>(std::istream& file, List& obj)
{
	string stemp;

	file >> stemp;

	if (stemp == "empty")
	{
		return file;
	}

	file.clear();
	file.seekg(0);

	while (!file.eof())
	{
		Plant temp;

		file >> temp;
		obj.push_back(temp);
	}

	return file;
}
