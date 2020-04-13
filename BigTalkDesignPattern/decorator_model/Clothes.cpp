
#include <iostream>
// #include <memory>
#include <string>

class Person
{
public:
    Person() = default;

    Person(std::string name)
    {
        this->name = name;
    };

    virtual ~Person() = default;

    virtual void Show() const
    {
        std::cout << "this is " << name << std::endl;
    }

private:
    std::string name;
};

class Finery : public Person
{
public:
    void Decorator(Person* m_component)
    {
        component=m_component;
    }
    virtual void Show() const override
    {
        if (component != nullptr)
        {
            component->Show();
        }
    }

protected:
    Person* component = nullptr;
};

class TShirts : public Finery
{
public:
    virtual void Show() const override
    {
        std::cout << "T-Shirt is weared on." << std::endl;
        Finery::Show();
    }
};

class BigTrouser : public Finery{
    public:
    virtual void Show() const override{
        std::cout << "Big Trouser is weared on." << std::endl;
        Finery::Show();
    }
};

int main()
{
    Person *m_person = new Person("zhangsan");
    TShirts *m_tShirt = new TShirts();
    BigTrouser *m_bigTrouse = new BigTrouser();

    m_bigTrouse->Decorator(m_person);
    m_tShirt->Decorator(m_bigTrouse);
    m_tShirt->Show();

    delete m_person;
    delete m_tShirt;
    delete m_bigTrouse;

    std::cin.get();

    return 0;
}