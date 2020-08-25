/*给定一颗二叉树，已知其中所有节点的值都不一样，
找到含有节点最多的搜索二叉子树，输出该子树总节点的数量。
搜索二叉树是指对于二叉树的任何一个节点，如果它有儿子，
那么左儿子的值应该小于它的值，右儿子的值应该大于它的值。*/

//思想：二叉搜索树2条件：左子树最大 < 根节点， 右子树最小 > 根节点
//思路：递归找出搜索二叉树的最大

#include <iostream>
#include <map>
using namespace std;

struct TreeNode
{
    int val;
    TreeNode *lch;
    TreeNode *rch;
};

TreeNode *input_TreeNode()
{
    int n, rootval, fa, lch, rch;
    cin >> n >> rootval;
    TreeNode *root, *new_node;
    map<int, TreeNode *> mp;
    for (int i = 1; i <= n; ++i)
    {
        scanf("%d %d %d", &fa, &lch, &rch);
        if (mp.find(fa) == mp.end())
        {
            new_node = (TreeNode *)malloc(sizeof(TreeNode));
            mp[fa] = new_node;
            new_node->val = fa;
            if (i == 1)
                root = new_node;
        }
        if (lch && mp.find(lch) == mp.end())
        {
            new_node = (TreeNode *)malloc(sizeof(TreeNode));
            mp[lch] = new_node;
            new_node->val = lch;
            new_node->lch = new_node->rch = NULL;
        }
        if (rch && mp.find(rch) == mp.end())
        {
            new_node = (TreeNode *)malloc(sizeof(TreeNode));
            mp[rch] = new_node;
            new_node->val = rch;
            new_node->lch = new_node->rch = NULL;
        }
        mp[fa]->lch = (lch ? mp[lch] : NULL);
        mp[fa]->rch = (rch ? mp[rch] : NULL);
    }
    return root;
}

struct TreeInfo
{
    bool isAllBST;  //包括根节点是否二叉搜索树
    int maxVal;     //左树最大值
    int minVal;     //右树最小值
    int maxBSTSize; //子树中最大二叉搜索树的大小
};
/*
bool JudgeBST(TreeNode* root){
    if(root==nullptr)
        return true;
    if(root->lch == nullptr && root->rch == nullptr)
        return true;
    if(root->lch!=nullptr && root->lch->val > root->val){
        return false;
    }
    if( root->rch!=nullptr && root->rch->val < root->val){
        return false;
    }
    return JudgeBST(root->lch)&&JudgeBST(root->rch);//左右子树皆不空且孩子均符合二叉搜索树，判断左右子树
}*/

TreeInfo GetMaxBSTSize(TreeNode *root)
{
    if (root == nullptr)
    {
        return (TreeInfo){true, 1000000, 0, -1}; //空节点即叶节点之后的子节点，题设1 <= val <=1000000
    }

    TreeInfo leftTreeInfo = GetMaxBSTSize(root->lch);
    TreeInfo rightTreeInfo = GetMaxBSTSize(root->rch);

    int CurmaxBSTSize = 0;
    bool CurisAllBST = false;
    //可行性1，左子树MaxBSTSize
    int p1 = -2;
    if (root->lch)
    {
        p1 = leftTreeInfo.maxBSTSize;
    }

    //p2:右子树上的MaxBSTSize是根的
    int p2 = -2;
    if (root->rch)
    {
        p2 = rightTreeInfo.maxBSTSize;
    }

    //p3:包括当前root节点在内全体均是二叉搜索树
    int p3 = -2;
    if ((root->lch ? leftTreeInfo.isAllBST : 1) && (root->rch ? rightTreeInfo.isAllBST : 1) && (root->lch ? root->val > leftTreeInfo.maxVal : 1) && (root->rch ? root->val < rightTreeInfo.minVal : 1))
    {
        //全体均是二叉搜索树
        CurisAllBST = true;
        p3 = (root->lch ? leftTreeInfo.maxBSTSize : 0) + (root->rch ? rightTreeInfo.maxBSTSize : 0) + 1;
    }
    //三种可能性取最大
    CurmaxBSTSize = max(p1, max(p2, p3));

    int Curmin = root->val;
    int Curmax = Curmin;
    //更新当前树最大值和树最小值
    if (root->lch)
    {
        Curmin = (Curmin > leftTreeInfo.minVal) ? leftTreeInfo.minVal : Curmin;
        Curmax = (Curmax < leftTreeInfo.maxVal) ? leftTreeInfo.maxVal : Curmax;
    }
    if (root->rch)
    {
        Curmin = (Curmin > rightTreeInfo.minVal) ? rightTreeInfo.minVal : Curmin;
        Curmax = (Curmax < rightTreeInfo.maxVal) ? rightTreeInfo.maxVal : Curmax;
    }

    return (TreeInfo){CurisAllBST, Curmax, Curmin, CurmaxBSTSize};
}

int main()
{
    TreeNode *root = input_TreeNode();

    cout << GetMaxBSTSize(root).maxBSTSize;

    return 0;
}