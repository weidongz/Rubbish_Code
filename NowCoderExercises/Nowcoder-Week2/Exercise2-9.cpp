/*
给定一棵二叉树，求以根节点为端点的最长路径（路径上所有节点权值和）

第一行输入N，表示有N个节点
接下来N行输入2个数
权值以及各个节点的父节点序号，0表示是根节点
*/

//思想：已知父节点，从每一个叶节点回溯到根节点即可得出所有路径，取最大值即为所求
//答案错误，通过率70%，

#include <iostream>
#include <vector>
using namespace std;

struct TreeNode
{
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode *parent;
    TreeNode(int x) : val(x), left(NULL), right(NULL), parent(NULL) {}
};

int main()
{
    int n;
    cin >> n;
    if (n <= 0)
        return 0;
    vector<TreeNode *> nodeVec;
    bool *isParent = new bool[n];
    for (int i = 0; i < n; i++)
        isParent[i] = false; //判断该节点是否叶节点

    for (int i = 0; i < n; i++)
    {
        int value;
        cin >> value;
        TreeNode *Curnode = new TreeNode(value);
        nodeVec.push_back(Curnode);
        int parentIndex;
        cin >> parentIndex;
        if (parentIndex != 0)
        {
            nodeVec[i]->parent = nodeVec[parentIndex - 1];
            isParent[parentIndex - 1] = true;
        }
    }

    long long maxPath = nodeVec[0]->val; //初始化为根节点值，防止负数出现
    for (int i = n - 1; i >= 0; i--)
    {
        if (isParent[i] == false)
        {
            TreeNode *pCur = nodeVec[i]; //nodeVec[i]叶节点, pCur当前节点指针
            long long curPath = 0;
            while (pCur)
            {
                curPath += pCur->val;
                pCur = pCur->parent;
            }
            if (curPath > maxPath)
                maxPath = curPath;
        }
    }
    cout << maxPath;

    delete[] isParent;
    return 0;
}
