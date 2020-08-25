/*
给定一颗二叉树，分别实现按层和 ZigZag 打印二叉树。
ZigZag遍历: 意思是第一层从左到右遍历，第二层从右到左遍历，依次类推。
*/

#include <iostream>
#include <vector>
#include <queue>
#include <stack>
using namespace std;

struct TreeNode{
    /*TreeNode * lch, * rch;
    TreeNode(TreeNode* Curlch, TreeNode* Currch){
        lch = Curlch;
        rch = Currch;
    }*/
    int val;
    int lch;
    int rch;
};

void printLevel(vector<TreeNode> tree, int rootIndex){
    //if(tree[root]==NULL)
    //    return;
    queue<TreeNode> nodeQueue;
    nodeQueue.push(tree[rootIndex]);
    int level = 1;
    while(!nodeQueue.empty()){
        int levelSize = nodeQueue.size();
        cout << "Level " << level << " :";
        while(levelSize--){
            TreeNode curNode = nodeQueue.front();
            if(curNode.lch)
                nodeQueue.push(tree[curNode.lch]);
            if(curNode.rch)
                nodeQueue.push(tree[curNode.rch]);
            cout << " " << curNode.val;
            nodeQueue.pop();
        }
        //if(!nodeQueue.empty())
            cout << endl;//多了一行
        level++;
    }
}

void printZigzag(vector<TreeNode> tree, int rootIndex){
    stack<TreeNode> nodeStack;

    int level = 1;
    nodeStack.push(tree[rootIndex]);
    while(!nodeStack.empty()){
        int levelSize = nodeStack.size();
        vector<int> levelVec;
        while(levelSize--){
            levelVec.push_back(nodeStack.top().val) ;
            nodeStack.pop();
        }
        
        if(level & 0x01==1){
            cout << "Level " << level << " from left to right:";
            for(int i=0; i<levelVec.size(); i++){
                TreeNode curNode = tree[levelVec[i]];
                if(curNode.lch)
                    nodeStack.push(tree[curNode.lch]);
                if(curNode.rch)
                    nodeStack.push(tree[curNode.rch]);
                cout << " " << curNode.val;
            }
        }
        else{//偶数层使用
            cout << "Level " << level << " from right to left:";
            for(int i=0; i<levelVec.size(); i++){
                TreeNode curNode = tree[levelVec[i]];
                if(curNode.rch)
                    nodeStack.push(tree[curNode.rch]);
                if(curNode.lch)
                    nodeStack.push(tree[curNode.lch]);
                cout << " " << curNode.val;
            }
        }
        
        cout << endl;//多了一行
        level++;
    }
}

int main(void){
    int n, rootIndex;
    cin >> n >> rootIndex;
    vector<TreeNode> treeNodeVec(n+1);
    int fa, lch, rch;
    while(n--){
        cin >> fa >> lch >> rch;
        treeNodeVec[fa] = TreeNode{fa, lch, rch};
    }
    
    printLevel(treeNodeVec, rootIndex);
    printZigzag(treeNodeVec, rootIndex);
    
    
    return 0;
}