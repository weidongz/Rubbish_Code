//

#include <iostream>
#include <string>
#include <exception>

// OOP: 可维护，可复用，可拓展，灵活性好
// 封装，继承，多态降低耦合度，设计模式思想使程序灵活易修改复用
// https://www.cnblogs.com/wuyuegb2312/archive/2013/04/09/3008320.html#

class Operation
{
public:
    static double GetResult(double numA, double numB, char stroperator);
    
};

double Operation::GetResult(double numA, double numB, char strOperator){
    double result = 0;
   switch (strOperator)
    {
    case '+':
        result = numA + numB;
        break;
    case '-':
        result = numA - numB;
        break;
    case '*':
        result = numA * numB;
        break;
    case '/':
        if (numB == 0)
        {
            throw "Denominator cannot be zero";
        }
        else
            result = numA / numB;
        break;

    default:
        throw  "wrong input";
    }

    return result;
}

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

    Operation op;
    try{
        double result = op.GetResult(numA, numB, strOperator);
        std::cout << result << std::endl;
    }
    catch(const char* e){
        cout << e << endl;
    }
    

    cin.get();
    cin.get();
    // system("pause");

    return 0;
}
