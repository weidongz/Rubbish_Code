/*
一棵二叉树原本是搜索二叉树，但是其中有两个节点调换了位置，
使得这棵二叉树不再是搜索二叉树，请按升序输出这两个错误节点的值。(每个节点的值各不相同)
*/

#include <iostream>
#include <vector>
using namespace std;

struct TreeNode
{
    int val;
    int lch;
    int rch;
};

vector<int> inOrderResult;

void inOrderVisited(vector<TreeNode> &tree, int rootIndex)
{
    //中序遍历
    TreeNode pRoot = tree[rootIndex];

    if (pRoot.lch)
        inOrderVisited(tree, pRoot.lch);
    inOrderResult.push_back(pRoot.val);
    if (pRoot.rch)
        inOrderVisited(tree, pRoot.rch);

    return;
}

int main()
{
    int n, rootIndex;
    cin >> n >> rootIndex;
    vector<TreeNode> treeVec(n + 1); //索引从1开始
    for (int i = 0; i < n; i++)
    {
        int fa, lch, rch;
        cin >> fa >> lch >> rch;
        treeVec[fa] = TreeNode{fa, lch, rch};
    }

    inOrderVisited(treeVec, rootIndex);

    //判断哪两个数调换了
    int lastIndex = inOrderResult.size() - 1;
    while (inOrderResult[lastIndex] > inOrderResult[lastIndex - 1])
        lastIndex--;
    cout << inOrderResult[lastIndex] << " ";

    int firstIndex = 0;
    while (inOrderResult[firstIndex] < inOrderResult[firstIndex + 1])
        firstIndex++;
    cout << inOrderResult[firstIndex];
    return 0;
}