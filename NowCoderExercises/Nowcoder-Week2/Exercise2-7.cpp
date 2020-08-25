/*给出一棵二叉树的先序和中序数组，通过这两个数组直接生成正确的后序数组。*/

//思路：找出中序根节点的位置，确定左右子树大小

#include <iostream>
#include <vector>

using namespace std;

vector<int> posArray;
void findPosArray(vector<int> &preArray, vector<int> &inArray, int preStart, int preEnd, int inStart, int inEnd)
{
    if (preArray.size() != inArray.size())
        return;
    if (preStart > preEnd)
        return; //这对应没有左子树的情况

    int rootIndex = 0;
    for (rootIndex = inStart; rootIndex < inEnd; rootIndex++)
    {
        if (inArray[rootIndex] == preArray[preStart])
            break;
    }
    int leftTreeSize = rootIndex - inStart;
    findPosArray(preArray, inArray, preStart + 1, preStart + leftTreeSize, inStart, inStart + leftTreeSize - 1);
    findPosArray(preArray, inArray, preStart + leftTreeSize + 1, preEnd, rootIndex + 1, inEnd);

    posArray.push_back(preArray[preStart]);
}

int main()
{
    int n;
    cin >> n;
    if (n <= 0)
        return 0;

    int num;
    vector<int> preArray;
    vector<int> inArray;
    for (int i = 0; i < n; i++)
    {
        cin >> num;
        preArray.push_back(num);
    }
    for (int i = 0; i < n; i++)
    {
        cin >> num;
        inArray.push_back(num);
    }

    findPosArray(preArray, inArray, 0, n - 1, 0, n - 1);
    for (int i = 0; i < n; i++)
    {
        cout << posArray[i] << " ";
    }
}
