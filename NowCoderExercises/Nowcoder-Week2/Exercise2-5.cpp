/*
给定一个的矩阵matrix，在这个矩阵中，只有0和1两种值，返回边框全是1的最大正方形的边长长度、
*/

//找出矩阵所有正方形的时间复杂度O(N^3)
//思想与左老师课上讲的一样，自测样例均通过，运行显示答案错误

#include <iostream>
using namespace std;

int* CountOne(bool rightmat, bool downmat, int* &matrix, int n){
    int *Curmat = new int[n*n];
    for(int i=0; i<n*n; i++) Curmat[i]=0;
    if(rightmat){
        //计算(i,j)位置右方的1的个数
        for (int i = n - 1; i >= 0; i--)
        {
            Curmat[i * n + n - 1] = matrix[(i + 1) * n - 1];
            for (int j = 1; j < n; j++)
            {
                Curmat[(i + 1) * n - 1 - j] = Curmat[(i + 1) * n - 1 - j + 1] + matrix[(i + 1) * n - 1 - j];
            }
        }
    }
    if(downmat){
        //计算(i,j)位置下方的1的个数
        for (int i = 0; i < n; i++)
        {
            Curmat[n * (n - 1) + i] = matrix[n * (n - 1) + i];
            for (int j = 1; j < n; j++)
            {
                Curmat[n * (n - 1 - j) + i] = matrix[n * (n - 1 - j) + i] + Curmat[n * (n - j) + i];
            }
        }
    }
    return Curmat;
}

int main(){
    int n;
    cin >> n;
    if(n==1)
        return 0;
    int *mat = new int[n*n];
    for(int i=0; i<n; i++){
        for(int j=0; j<n; j++){
            cin >> mat[i*n+j];
        }
    }
    
    int* rightmat = new int[n*n];
    int* downmat = new int[n*n];
    rightmat = CountOne(1, 0, mat, n);
    downmat = CountOne(0, 1, mat, n);
    
    int maxsize=0;
    for(int i=0; i<=(n-2)*n; ){
        for(int j=0; j<n-1; j++){//最底下的边和最右边的边的点构不成正方形，不需要遍历
            for(int size=1; size < n-j && size < n-i; size++){//正方形边长,边长1需要两个点
                if(rightmat[i+j]>=size && downmat[i+j]>=size && rightmat[i+j+size*n]>=size && downmat[i+j+size]>=size)
                    if(size>maxsize)
                        maxsize=size+1;
            }
        }
        i=i+n;
    }
    
    cout << maxsize;
    delete[] rightmat;
    delete[] downmat;
    delete[] mat;
    return 0;
}
