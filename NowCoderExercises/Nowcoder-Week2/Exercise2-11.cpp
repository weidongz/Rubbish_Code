/*给出一个整数 n，如果 n < 1，代表空树，
否则代表中序遍历的结果为 {1, 2, 3... n}。请输出可能的二叉树结构有多少。*/

//思想：二叉树结构=根节点+左子树结构+右子树结构

#include <iostream>

using namespace std;

const long long mod = (1e9 + 7);

int treeMethod(int n)
{
    if (n <= 1)
        return 1; //空树与只有一个根节点
    if (n == 2)
        return 2; 
    /* //递归方法超时
    long long methods = 0;
    for(int i=0; i<n; i++){
        methods += treeMethod(n-1-i)*treeMethod(i);
    }
    return methods;*/
    int *dp = new int[n + 1];
    dp[0] = 1, dp[1] = 1, dp[2] = 2;
    for (int i = 3; i <= n; i++)
    {
        for (int j = 0; j < i; j++)
        { //左侧j个节点，右侧i-j-1个
            dp[i] += dp[j] % mod * dp[i - j - 1] % mod;
            dp[i] %= mod;
        }
    }
    int result = dp[n] % mod;
    delete[] dp;
    return result;
}

int main()
{
    int n;
    cin >> n;

    int ways = treeMethod(n);
    cout << ways;

    return 0;
}