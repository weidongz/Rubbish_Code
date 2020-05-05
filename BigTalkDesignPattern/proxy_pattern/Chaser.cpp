#include <iostream>
#include <string>
class SchoolGirl
{
private:
    std::string name;

public:
    SchoolGirl(std::string m_name) : name(m_name){};
    std::string getname() { return name; }
};

class subject
{
public:
	virtual ~subject() = default;
	virtual void sendflower()const = 0;
    // virtual void senddoll() const = 0;
};

class Pursuit : public subject
{
public:
    Pursuit() = default;
    Pursuit(SchoolGirl* m_mm) : mm(m_mm){};
    virtual void sendflower() const override
    {
        std::string name = mm->getname();
        std::cout << "send flower to " << name;
    }

private:
    SchoolGirl* mm = nullptr;
};

class Proxy : public subject
{
    public:
        Proxy(SchoolGirl* m_mm) { tiangou = new Pursuit(m_mm); }
        virtual void sendflower() const override{
            tiangou->sendflower();
        }
        ~Proxy() { delete tiangou; }

    private:
        Pursuit *tiangou = nullptr;
};

int
main()
{
    SchoolGirl* mm = new SchoolGirl("lilu");
    Proxy man = Proxy(mm);
    man.sendflower();

    return 0;
}