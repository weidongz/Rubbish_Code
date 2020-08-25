/* 给定一棵完全二叉树的头节点head，返回这棵树的节点个数。
// 如果完全二叉树的节点数为N，请实现时间复杂度低于O(N)的解法。*/
// 思想：二分法找出，并判断

/**
struct TreeNode {
    int val;
    struct TreeNode *left;
    struct TreeNode *right;
    TreeNode(int x) :
            val(x), left(NULL), right(NULL) {
    }
};
*/
class Solution
{
public:
    int nodeNumCore(TreeNode *root)
    {
        if (root == nullptr)
            return 0;
        if (root->left == nullptr) // && root->right==nullptr //左空右肯定空
            return 1;

        int depth = 0; //完全二叉树深度
        TreeNode *pCur = root;
        while (pCur)
        {
            depth++;
            pCur = pCur->left;
        }

        int rightDepth = 0; //根的右子树深度
        pCur = root->right; //此处为null也没关系，不会进入循环
        while (pCur)
        {
            rightDepth++;
            pCur = pCur->left;
        }

        if (depth - 2 == rightDepth)
        {
            //右子树是满二叉树
            int rightNodeNum = (1 << rightDepth) - 1; //满二叉树计算公式:2^深度 - 1
            //if(root->right == nullptr) rightNodeNum = 0; //1 << 0 = 1，  故应当重置
            return nodeNumCore(root->left) + 1 + rightNodeNum;
        }

        if (depth - 1 == rightDepth)
        {
            //右子树可能不满，左子树满
            int leftNodeNum = (1 << (depth - 1)) - 1; //注意运算符优先级，最外面的括号不能省略
            return leftNodeNum + 1 + nodeNumCore(root->right);
        }

        //return 0;//不满足完全二叉树定义
    }

    int nodeNum(struct TreeNode *head)
    {
        //小于O(n) ，遍历节点的结果必然是O(N)， 从二分查找上si'ka
        /*O（n）的解法
        int result = 0;
        if(head == nullptr)
            return 0;
        TreeNode* pCur = head;
        vector<TreeNode*> nodeVec;
        nodeVec.push_back(head);
        while(!nodeVec.empty()){
            pCur = nodeVec.back();
            nodeVec.pop_back();
            result++;
            if(pCur->left)
                nodeVec.push_back(pCur->left);
            if(pCur->right)
                nodeVec.push_back(pCur->right);
        }
        return result;*/

        //O（logn）的解法
        return nodeNumCore(head);
    }
};