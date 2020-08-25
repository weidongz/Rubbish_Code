/*
对二叉树的节点来说，有本身的值域，有指向左孩子节点和右孩子节点的两个指针；
对双向链表的节点来说，有本身的值域，有指向上一个节点和下一个节点的指针。
在结构上，两种结构有相似性，现在有一棵搜索二叉树，请将其转换成一个有序的双向链表。
*/

//思路：找出左右子树的链表头尾节点，并与根节点联系起来

#include <bits/stdc++.h>
#include <cstdio>
//Edited by Weidong Zheng, 牛客ID：584575940
using namespace std;

struct double_list_node{
    int val;
    struct double_list_node * pre, * next;
};

struct BST{
    int val;
    struct BST * lch, * rch;
};

BST * input_BST()
{
    int n, fa, lch, rch;
    scanf("%d", &n);
    BST * root, * new_node;
    map<int, BST *> mp;
    for (int i = 1; i <= n; ++i) {
        scanf("%d %d %d", &fa, &lch, &rch);
        if (mp.find(fa) == mp.end()) {
            new_node = (BST *)malloc(sizeof(BST));
            mp[fa] = new_node;
            new_node->val = fa;
            if (i == 1) root = new_node;
        }
        if (lch && mp.find(lch) == mp.end()) {
            new_node = (BST *)malloc(sizeof(BST));
            mp[lch] = new_node;
            new_node->val = lch; new_node->lch = new_node->rch = NULL;
        }
        if (rch && mp.find(rch) == mp.end()) {
            new_node = (BST *)malloc(sizeof(BST));
            mp[rch] = new_node;
            new_node->val = rch; new_node->lch = new_node->rch = NULL;
        }
        mp[fa]->lch = (lch ? mp[lch] : NULL);
        mp[fa]->rch = (rch ? mp[rch] : NULL);
    }
    return root;
}

pair<double_list_node*, double_list_node*> build_double_list(BST* root){
    //获得子树链表的头节点和尾节点
    pair<double_list_node*, double_list_node*> TreeList(nullptr, nullptr);
    if(root==nullptr){
        return TreeList;
    }
    
    //获得左子树有序链表起点和终点
    pair<double_list_node*, double_list_node*> rightListInfo = build_double_list(root->rch);
    pair<double_list_node*, double_list_node*> leftListInfo = build_double_list(root->lch);
    
    double_list_node* rootListNode=new double_list_node;
    rootListNode->val = root->val;
    
    //left.last <- root
    rootListNode->pre = leftListInfo.second;
    
    //left.last -> root
    if(leftListInfo.second!=nullptr)
        leftListInfo.second->next = rootListNode;
    
    //root -> right.first
    rootListNode->next = rightListInfo.first;
    
    if(rightListInfo.first!=nullptr)
        rightListInfo.first->pre = rootListNode;
    
    //返回整棵树的头
    TreeList.first = (leftListInfo.first!=nullptr)? leftListInfo.first : rootListNode;
    //尾
    TreeList.second = (rightListInfo.second!=nullptr) ? rightListInfo.second : rootListNode;
    return TreeList;
}


double_list_node * convert(BST * root)
{
    //////暴力解：中序遍历再用值构建链表
    //递归解：找出左右子树头尾节点进行相连
    if(root==nullptr){
        return nullptr;
    }
    /*
    double_list_node* pHead = new double_list_node;
    BST * pTreeNode = root;
    while(pTreeNode->lch)
        pTreeNode = pTreeNode->lch;
    pHead->val = pTreeNode->val;//找到链表头节点
    */
    double_list_node* pHead = build_double_list(root).first;
    return pHead;
    
}

void print_double_list(double_list_node * head)
{
    while (head != NULL) {
        printf("%d ", head->val);
        head = head->next;
    }
    puts("");
}

int main ()
{
    BST * root = input_BST();
    double_list_node * new_double_head = convert(root);
    print_double_list(new_double_head);
    return 0;
}