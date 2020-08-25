/*
给定一个有 n 个不重复整数的数组 arr，判断 arr 是否可能是节点值类型为整数的搜索二叉树后序遍历的结果。
*/

#include <iostream>
#include <vector>
using namespace std;

//vector不传引用超时，传引用通过
bool judgePostArray(vector<int> &arr, int start, int end)
{
    if (start >= end)
        return true;

    //int arrLen = arr.size();
    int rootVal = arr[end];

    int rightTreeIndex = start; //右子树起点
    for (; rightTreeIndex < end; rightTreeIndex++)
    {
        if (arr[rightTreeIndex] > rootVal)
            break;
    }

    for (int i = rightTreeIndex; i < end; i++)
    {
        if (arr[i] < rootVal)
            return false; //右子树中有小于根节点的值
    }

    return judgePostArray(arr, start, rightTreeIndex - 1) && judgePostArray(arr, rightTreeIndex, end - 1);
}

int main()
{
    int n;
    cin >> n;

    vector<int> arr;
    for (int i = 0; i < n; i++)
    {
        int arr_i;
        cin >> arr_i;
        arr.push_back(arr_i);
    }

    if (judgePostArray(arr, 0, n - 1))
        cout << "true";
    else
        cout << "false";

    return 0;
}