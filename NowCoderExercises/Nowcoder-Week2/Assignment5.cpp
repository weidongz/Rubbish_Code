/*
给定一棵二叉树，已经其中没有重复值的节点，请判断该二叉树是否为搜索二叉树和完全二叉树。
*/

#include <iostream>
#include <string>
#include <vector>
#include <queue>

using namespace std;

struct TreeNode
{
    int val;
    int lch;
    int rch;
};

void GetBST(vector<TreeNode> &treeVec, int rootIndex, vector<int> &inOrderVec)
{
    if (treeVec[rootIndex].lch)
        GetBST(treeVec, treeVec[rootIndex].lch, inOrderVec);
    inOrderVec.push_back(treeVec[rootIndex].val);
    if (treeVec[rootIndex].rch)
        GetBST(treeVec, treeVec[rootIndex].rch, inOrderVec);
    return;
}

bool judgeFullTree(vector<TreeNode> &treeVec, int rootIndex)
{
    TreeNode root = treeVec[rootIndex];

    /*递归解失效
    if(root.lch==0 && root.rch!=0) return false; 
    if(root.lch && root.rch){
        return judgeFullTree(treeVec, root.lch) && judgeFullTree(treeVec, root.rch);
    }
    if(root.lch && root.rch==0) //这种情况应保证root.rch其后无叶节点
        return judgeFullTree(treeVec, root.lch);
    
    return true;*/
    //只能用迭代解，保证左不空右空的情况，该节点之后都是叶节点
    queue<TreeNode> treeQueue;
    treeQueue.push(root);
    bool leaf = false;

    while (!treeQueue.empty())
    {
        TreeNode Curnode = treeQueue.front();
        treeQueue.pop();
        if (Curnode.lch && Curnode.rch)
        {
            treeQueue.push(treeVec[Curnode.lch]);
            treeQueue.push(treeVec[Curnode.rch]);
        }
        else if (Curnode.lch == 0 && Curnode.rch != 0)
            return false;
        else
        { //左右皆空与左不空右空
            if (Curnode.lch && Curnode.rch != 0)
            {
                treeQueue.push(treeVec[Curnode.lch]);
            }

            while (!treeQueue.empty())
            { //保证左不空右空的节点或者叶节点之后都是叶节点
                TreeNode leafNode = treeQueue.front();
                treeQueue.pop();
                if (leafNode.lch != 0 || leafNode.rch != 0)
                {
                    return false;
                }
            }
        }
    }
    return true;
}

int main()
{
    int n, rootIndex;
    cin >> n >> rootIndex;
    vector<TreeNode> treeVec(n + 1);
    for (int i = 0; i < n; i++)
    {
        int fa, lch, rch;
        cin >> fa >> lch >> rch;
        treeVec[fa] = TreeNode{fa, lch, rch};
    }

    vector<int> inOrderArray;
    GetBST(treeVec, rootIndex, inOrderArray); //根据中序遍历结果判断
    string isBST = "true";
    for (int i = 0; i < inOrderArray.size() - 1; i++)
    {
        if (inOrderArray[i] > inOrderArray[i + 1])
        {
            isBST = "false";
        }
    }
    cout << isBST << endl;

    bool isFull = judgeFullTree(treeVec, rootIndex); //遍历所有节点结构进行判断
    if (isFull)
        cout << "true";
    else
        cout << "false";

    return 0;
}
