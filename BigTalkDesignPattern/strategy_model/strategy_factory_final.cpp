#include <iostream>
#include <math.h>

// enum CashType
// {
//     Normal,
//     Rebate,
//     Return
// };

class CashSuper
{
public:
    virtual ~CashSuper() = default;
    virtual double acceptCash(double money) const = 0;
};

class CashNormal : public CashSuper
{
public:
    virtual double acceptCash(double money) const override
    {
        return money;
    }
};

class CashRebate : public CashSuper
{
public:
    CashRebate(double rebate) : moneyRebate(rebate) {}

    virtual double acceptCash(double money) const override
    {
        return moneyRebate * money;
    }

private:
    double moneyRebate;
};

class CashReturn : public CashSuper
{
public:
    CashReturn(double condition, double m_return) : moneyCondition(condition), moneyReturn(m_return) {}
    // void cashReturn(string moneyCondition, string moneyReturn){
    //     this.moneyReturn = double(moneyReturn);
    //     this.moneyCondition = double(moneyCondition);
    // }
    virtual double acceptCash(double money) const override
    {
        double result = money;
        if (money >= moneyCondition)
        {
            result = money - floor(money / moneyCondition) * moneyReturn;
        }
        return result;
    }

private:
    double moneyCondition;
    double moneyReturn;
};

class CashContext
{
public:
    CashContext(int discount_type) {
        switch (discount_type)
        {
        case 1: //Normal
            cs = new  CashNormal();
            break;
        case 2: //Rebate:
            cs = new  CashRebate(0.8);
            break;
        case 3: //every 300 Return 100:
            cs = new CashReturn(300, 100);
            break;
        default:
            throw "wrong input";
        }
    }
    ~CashContext()
    {
        if (cs != nullptr)
        {
            delete cs;
            cs = nullptr;
        }
    }

    double GetResult(double money){
        return cs->acceptCash(money);
    }
    
private:
    CashSuper *cs = nullptr;
};
//createCashAccept

int main()
{
    using namespace std;
    double total = 0;
    double price = 0;
    int discount_type;
    cout << "Please enter price: ";
    cin >> price;
    cout << "please enter discount type(1 for normal, 2 for rebate, 3 for return): ";
    cin >> discount_type;
    try
    {
        CashContext cc(discount_type);
        
        
        total = cc.GetResult(price);
        cout << "Accept " << total << " yuan";

    }
    catch (const char *e)
    {
        cout << e << endl;
    }
}