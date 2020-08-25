/*
平衡二叉树的性质为: 要么是一棵空树，要么任何一个节点的左右子树高度差的绝对值不超过 1。
给定一棵二叉树，判断这棵二叉树是否为平衡二叉树。
一颗树的高度指的是树的根节点到所有节点的距离中的最大值。
*/

//后序遍历看子树高度是否满足要求

#include <bits/stdc++.h>
#include <iostream>
using namespace std;

struct tree_node
{
    int val;
    tree_node *left;
    tree_node *right;
    tree_node(int value) : val(value), left(nullptr), right(nullptr) {}
};

void build_tree(tree_node *root, int cnt)
{
    if (root == nullptr)
    {
        return;
    }
    int p, l, r;
    cin >> p >> l >> r;
    if (l)
    {
        tree_node *left = new tree_node(l);
        root->left = left;
        build_tree(root->left, --cnt);
    }
    if (r)
    {
        tree_node *right = new tree_node(r);
        root->right = right;
        build_tree(root->right, --cnt);
    }
}

int getTreeBalance(tree_node *root)
{
    if (root == nullptr)
        return 0;

    int leftDepth = getTreeBalance(root->left);
    if (leftDepth == -1)
        return -1;

    int rightDepth = getTreeBalance(root->right);
    if (rightDepth == -1)
        return -1;

    int rootdepth = 0;
    if (abs(rightDepth - leftDepth) > 1)
        rootdepth = -1;
    else
    {
        rootdepth = max(rightDepth, leftDepth) + 1;
    }

    return rootdepth;
}

int main()
{
    int n, root_val;
    cin >> n >> root_val;
    tree_node *root = new tree_node(root_val);
    build_tree(root, n);

    if (getTreeBalance(root) > 0)
        cout << "true";
    else
        cout << "false";

    return 0;
}
