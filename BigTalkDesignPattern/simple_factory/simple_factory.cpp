// 

#include <iostream>
#include <string>

// class 
int main()
{
    using namespace std;

    int numA, numB;
    char strOperator;

    cout << "Please enter num A: ";
    cin >> numA;
    cout << "Enter operator:";
    cin >> strOperator;
    cout << "Please enter num B: ";
    cin >> numB;

    switch(strOperator){
        case '+':
            cout << numA + numB;
            break;
        case '-':
            cout << numA - numB;
            break;
        case '*':
            cout << numA * numB;
            break;
        case '/':
            if (numB == 0){
                cout << "Denominator cannot be zero";
            }
            else
                cout << numA/numB;
            break;

        default:
            cout << "wrong input";
    }

    // cin.get();
	return 0;
}
