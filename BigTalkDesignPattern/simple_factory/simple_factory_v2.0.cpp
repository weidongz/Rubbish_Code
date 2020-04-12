//

#include <exception>
#include <iostream>
#include <string>
#include <memory>

// OOP: 可维护，可复用，可拓展，灵活性好
// 封装，继承，多态降低耦合度，设计模式思想使程序灵活易修改复用
// https://www.cnblogs.com/wuyuegb2312/archive/2013/04/09/3008320.html#

class Operation_Base
{
public:
    virtual double GetResult(double numA, double numB) const = 0;

    virtual ~Operation_Base() = default;
};

class Operation_Add : public Operation_Base
{
    virtual double GetResult(double numA, double numB) const override
    {
        double result = numA + numB;
        return result;
    }
};

class Operation_Sub : public Operation_Base
{
    virtual double GetResult(double numA, double numB) const override
    {
        return numA - numB;
    }
};

class Operation_Mul : public Operation_Base
{
    virtual double GetResult(double numA, double numB) const override
    {
        return numA * numB;
    }
};

class Operation_Div : public Operation_Base
{
    virtual double GetResult(double numA, double numB) const override
    {
        if (numB == 0)
        {
            throw "Denominator cannot be zero";
        }
        else
            return numA / numB;
    }
};

    Operation_Base* createOp(char strOper)
    {
        Operation_Base* oper;
        switch (strOper)
        {
        case '+':
            oper = new Operation_Add;
            break;
        case '-':
            oper = new Operation_Sub;
            break;
        case '*':
            oper = new Operation_Mul;
            break;
        case '/':

            oper = new Operation_Div;
            break;

        default:
            throw "wrong input";
        }

        return oper;
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

    Operation_Base* op;
    op = createOp(strOperator);
    try
    {
        double result = op->GetResult(numA, numB);
        std::cout << result << std::endl;
        delete op;
    }
    catch (const char *e)
    {
        cout << e << endl;
    }

    cin.get();
    cin.get();
    // system("pause");

    return 0;
}
