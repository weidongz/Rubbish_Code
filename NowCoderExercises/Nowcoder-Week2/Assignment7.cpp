/*
牛能在某小城有了固定的需求，为了节省送货的费用，他决定在小城里建一个仓库，但是他不知道选在哪里，可以使得花费最小。
给出一个m*n的矩阵，代表下一年小城里各个位置对货物的需求次数。
我们定义花费为货车载货运输的距离，货车只能沿着水平或竖直方向行驶。
*/

//BFS， 队列存元素
//没有那么麻烦，队列存元素然后求每个节点与起始点距离
#include <iostream>
#include <vector>
#include <queue>
using namespace std;

int main()
{
    int T;
    cin >> T;
    while (T--)
    {
        int cols, rows;
        cin >> cols >> rows;
        /*
        int** arr = new int*[n];
        for(int i=0; i<n; i++){
            arr[i] = new int[m];
            for(int j=0; j<m; j++){
                cin  >> arr[i][j];
            }
        }*/
        vector<vector<int>> mat(rows, vector<int>(cols));
        for (int i = 0; i < rows; i++)
        {
            for (int j = 0; j < cols; j++)
            {
                cin >> mat[i][j];
            }
        }

        int minSpent = -1;
        //queue<int> disQueue;//保存BFS当前节点
        for (int i = 0; i < rows; i++)
        {
            for (int j = 0; j < cols; j++)
            {
                //每个节点作初始点
                int curSpent = 0;
                for (int k = 0; k < rows; k++)
                {
                    for (int l = 0; l < cols; l++)
                    {
                        int dis = abs(i - k) + abs(j - l);
                        curSpent += dis * mat[k][l];
                    }
                }
                if (minSpent == -1)
                    minSpent = curSpent;
                else
                    minSpent = min(minSpent, curSpent);
            }
        }

        cout << minSpent << endl;
    }

    return 0;
}
