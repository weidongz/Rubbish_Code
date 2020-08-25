/*
二叉树的前序、中序、后序遍历的定义： 
前序遍历：对任一子树，先访问跟，然后遍历其左子树，最后遍历其右子树； 
中序遍历：对任一子树，先遍历其左子树，然后访问根，最后遍历其右子树； 
后序遍历：对任一子树，先遍历其左子树，然后遍历其右子树，最后访问根。 
给定一棵二叉树的前序遍历和中序遍历，求其后序遍历（提示：给定前序遍历与中序遍历能够唯一确定后序遍历）。
*/

#include <iostream>
#include <string>
using namespace std;

void getPostOrder(string preOrder, string inOrder, int preStart, int preEnd, int inStart, int inEnd, string &result)
{

    if (preOrder.size() != inOrder.size() || preOrder.size() == 0 || inOrder.length() == 0)
    {
        return;
    }
    /*
    if(preStart==preEnd){//仅剩一个节点
        result += preOrder[preStart];
        return;
    }*/
    if (preStart > preEnd)
        return; //这对应没有左子树的情况,关键

    int rootMidIndex = inStart;
    while (inOrder[rootMidIndex] != preOrder[preStart])
        rootMidIndex++;

    int leftTreeSize = rootMidIndex - inStart;
    getPostOrder(preOrder, inOrder, preStart + 1, preStart + leftTreeSize, inStart, inStart + leftTreeSize + 1, result);
    getPostOrder(preOrder, inOrder, preStart + leftTreeSize + 1, preEnd, rootMidIndex + 1, inEnd, result);
    result += preOrder[preStart];
    return;
}

int main()
{
    string s1, s2;
    while (cin >> s1 >> s2)
    {
        string result = "";
        getPostOrder(s1, s2, 0, s1.size() - 1, 0, s2.length() - 1, result);
        cout << result << endl;
    }
    return 0;
}