/*牛牛有一些排成一行的正方形。每个正方形已经被染成红色或者绿色。
牛牛现在可 以选择任意一个正方形然后用这两种颜色的任意一种进行染色,这个正方形的颜色将 会被覆盖。
牛牛的目标是在完成染色之后,每个红色R都比每个绿色G距离最左侧近。 牛牛想知道他最少需要涂染几个正方形。*/

//思想：计算第i个正方形左边有几个绿色，右边有几个红色

//思路：双指针
#include <iostream>
#include <string>
using namespace std;

int main()
{
    string str;
    cin >> str;
    int strLen = str.length();
    if (strLen <= 1)
    {
        cout << 0;
        return 0;
    }

    //辅助数组
    int *leftG = new int[strLen];
    int *rightR = new int[strLen];
    leftG[0] = (str[0] == 'G' ? 1 : 0);
    rightR[strLen - 1] = str[strLen - 1] == 'R' ? 1 : 0;
    for (int i = 1; i < strLen; i++)
    {
        leftG[i] = leftG[i - 1] + (str[i] == 'G' ? 1 : 0);
        rightR[strLen - 1 - i] = rightR[strLen - i] + (str[strLen - 1 - i] == 'R' ? 1 : 0);
    }
    int min = (rightR[0] < leftG[strLen - 1] ? rightR[0] : leftG[strLen - 1]); //因为永远也到不了rightR[0]he和leftG[strLen-1]
    for (int i = 1; i < strLen - 1; i++)
    {
        if (leftG[i - 1] + rightR[i + 1] < min)
            min = leftG[i - 1] + rightR[i + 1];
    }
    cout << min;
    
    delete[] rightR;
    delete[] leftG;

    return 0;
}