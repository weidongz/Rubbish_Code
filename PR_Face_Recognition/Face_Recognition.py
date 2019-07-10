# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 18:53:27 2019
@description: Use for test Yale and ORL datasets
ref: https://www.cnblogs.com/zmshy2128/p/6150690.html
@author: lab
"""
import numpy as np
import os, glob, random, cv2
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.model_selection import GridSearchCV
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
import pywt

#%% 加载ORL图像集，10张中随机选择sampleCount张图片用于训练
def loadORLImages(folder, sampleCount): 
    trainData = []; testData = []; yTrain=[]; yTest = [];
    for k in range(40):
        folder2 = os.path.join(folder, 's%d' % (k+1))
        data = [cv2.imread(d,0) for d in glob.glob(os.path.join(folder2, '*.pgm'))]
        sample = random.sample(range(10), sampleCount)
        trainData.extend([data[i].ravel() for i in range(10) if i in sample])
        testData.extend([data[i].ravel() for i in range(10) if i not in sample])
        yTest.extend([k]* (10-sampleCount))
        yTrain.extend([k]* sampleCount)
    return np.array(trainData),  np.array(yTrain), np.array(testData), np.array(yTest)

#%% 加载Yale图像集
def loadYaleImages(folder=u'./Yale', sampleCount=5): #加载图像集，随机选择sampleCount张图片用于训练
    trainData = []; testData = []; yTrain=[]; yTest = [];
    face_num = 11
    for k in range(15):
        folder2 = os.path.join(folder, str(k+1))
        data = [cv2.imread(d,0) for d in glob.glob(os.path.join(folder2, '*.bmp'))]
        sample = random.sample(range(face_num), sampleCount)
        trainData.extend([data[i].ravel() for i in range(face_num) if i in sample])
        testData.extend([data[i].ravel() for i in range(face_num) if i not in sample])
        yTest.extend([k]* (face_num-sampleCount))
        yTrain.extend([k]* sampleCount)
    return np.array(trainData),  np.array(yTrain), np.array(testData), np.array(yTest)
#%% 进行小波变换
def wavelet_transform (xData,img_width=92,img_height=112):
    img_num = xData.shape[0]
    imgdata = []
    for img_index in range(img_num):
        img = xData[img_index].reshape(img_width,img_height)
        coeffs = pywt.dwt2(img, 'haar')
        cA, (cH, cV, cD) = coeffs
        img = cA
        img = img.ravel()
#        print(img.shape)
        imgdata.append(img)
#        xData[img_index] = img
    return imgdata
#%%
def SVM_GridSearch(xTrain,yTrain,xTest,yTest):
    svc = SVC(kernel='rbf', class_weight='balanced')
    c_range = np.logspace(-5, 15, 11, base=2) #default: 1
    gamma_range = np.logspace(-9, 3, 13, base=2) #default: 1/n_features
    # 网格搜索交叉验证的参数范围，cv=3,3折交叉
    param_grid = [{'kernel': ['linear','rbf'], 'C': c_range, 'gamma': gamma_range}]
    grid_search = GridSearchCV(svc, param_grid, cv=3, n_jobs=-1)
#    print("Best parameters:{}".format(grid_search.best_params_))
#    print("Best score on train set:{}".format(grid_search.best_score_)
#    clf = grid_search.fit(np.float32(xTrain), np.float32(yTrain))
#    print("Best: %f using %s" % (clf.best_score_,clf.best_params_))
    grid_search.fit(np.float32(xTrain), np.float32(yTrain))
    score = grid_search.score(xTest, yTest)
    return score
#    yPredict = clf.predict(np.float32(xTest))
#    yPredict = grid_search.predict(xTest)
    #yPredict = svm.predict_all(xTest.astype(np.float64)) 
#    print(u'支持向量机识别率: %.2f%%' % ((yPredict == np.array(yTest)).mean()*100))
#%%
def main(): 
    # load ORL or load Yale
    xTrain_, yTrain, xTest_, yTest = loadORLImages(u'./att_faces',5)
#    xTrain_, yTrain, xTest_, yTest = loadYaleImages()
    # WT+PCA+SVM
    # WT
    xTrain = np.array(wavelet_transform(xTrain_))
    xTest = np.array(wavelet_transform(xTest_))
    #Yale dataset wavelet
#    xTrain = np.array(wavelet_transform(xTrain_,100,100))
#    xTest = np.array(wavelet_transform(xTest_,100,100))
    # PCA
    data = np.float32(np.mat(xTrain)) 
    pca = PCA(n_components=50)
    pca.fit(data)
    xTrain = pca.transform(data)
    print('PCA解释率%s' % sum(pca.explained_variance_ratio_))
    xTest = pca.transform(np.float32(np.mat(xTest)))
    # SVM
    score = SVM_GridSearch(xTrain,yTrain,xTest,yTest)
    print('WT+PCA+SVM精度为%s' % score)
    
    # PCA+SVM
    # PCA
    data = np.float32(np.mat(xTrain_)) 
    pca = PCA(n_components=50)
    pca.fit(data)
    xTrain = pca.transform(data)
    print('PCA解释率%s' % sum(pca.explained_variance_ratio_))
    xTest = pca.transform(np.float32(np.mat(xTest_)))
    # SVM
    score = SVM_GridSearch(xTrain,yTrain,xTest,yTest)
    print('PCA+SVM精度为%s' % score)
    
    # LDA+SVM
#    #%% LDA directly
#    clf = LDA()
#    clf.fit(xTrain_, yTrain)
#    yPredict = clf.predict(xTest_)
#    print(np.where(yPredict != np.array(yTest)))
#    print(u'LDA识别率: %.2f%%' % ((yPredict == np.array(yTest)).mean()*100))
    
    #use for feature extration
    clf = LDA(n_components=50)
    clf.fit(xTrain_, yTrain)
    xTrain = clf.transform(xTrain_) #xTrain为降维后的数据
    xTest = clf.transform(xTest_)
    #print ('LDA的数据中心点:',clf.means_) #中心点
    print ('LDA做分类时的正确率:',clf.score(xTest_, yTest)) #score是指分类的正确率
    # SVM
    score = SVM_GridSearch(xTrain,yTrain,xTest,yTest)
    print('LDA+SVM精度为%s' % score)
    
    # LLE+SVM
    from sklearn.manifold import LocallyLinearEmbedding as LLE
    lle = LLE(n_neighbors =30, n_components = 50, method='standard')
    lle.fit(xTrain_)
    xTrain = lle.transform(xTrain_)
    xTest = lle.transform(xTest_) 
#    trans_data,err = lle.fit_transform(xTrain_)
#    print("LLE Done. Reconstruction error: %g" % err)
    # SVM
    score = SVM_GridSearch(xTrain,yTrain,xTest,yTest)
    print('LLE+SVM精度为%s' % score)
    
if __name__ =='__main__':
    main()
