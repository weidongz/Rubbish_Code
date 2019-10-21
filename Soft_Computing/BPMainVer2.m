% parameter description
%     h=4   the node number of input layer
%     i=5   the node number of hidden layer
%     j=3 the node number of output layer
%     V[h,i]  the weights between input and hidden layers
%     W[i,j]  the weights between hidden and output layers
%     Phi[i]   the thresholds of hidden layer nodes
%     Tau[j]  the thresholds of output layer nodes
%     a[h]    the input values
%     b[i]    the hidden layer node actibations
%     c[j]    the output layer node activations
%     ck[j]   the desired output of output layer nodes
%     d[j]    the error in output layer nodes
%     e[i]    the error in hidden layer nodes
%     DeltaW[i,j] the amount of changes for the weights W[i,j]
%     DeltaV[h,i] the amount of changes for the weights V[h,i]
%     DeltaPhi[i] the amount of changes for the threshold 
%     DeltaTau[j] the amount of changes for the threshold Tau[j]
%     Alpha=0.1   the learning rate of deltaW
%     Beta=0.1    the learning rate of DeltaV
%     Gamma=0.8   the constant determines effect of past weight changes
%     Toe=0.001   the torrelance that determines when to stop trainging
%     Maxepoch=1000   the max iteratenumber

clear
close all
clc
% pwd
%change the work dir
% cd D:\school\backpropagation
%h:input layer nodes;i:hidden layer nodes;j:output layer nodes
h=4;
i=5;
j=3;
Alpha=0.2;   %the learning rate of deltaW
Beta=0.2;    %the learning rate of DeltaV
Gamma=0.8;   %the constant determines effect of past weight changes
Toe=0.01;   %the torrelance that determines when to stop trainging
Maxepoch=1000;   %the max iterate number

load('iris_data.dat')
X = iris_data(:,3:6);%150*4 Feature matrix
a = mapminmax(X',0,1);%normalization, accounding to rows, y = (ymax - ymin)*(x - xmin)/(xmax - xmin) + ymin;
a = transpose(a);
y = iris_data(:,2);%150*1 label matrix
% label = zeros(length(y),j);%150*3 matrix for one-hot
% %one-hot encoding
% for tmp=1:length(y)
%     if y(tmp)==0
%         label(tmp,1)=1;
%     elseif y(tmp)==1
%         label(tmp,2)=1;
%     elseif y(tmp)==2
%         label(tmp,3)=1;
%     end
% end
%one-hot encoding
label=eye(3);
label=label(y+1,:);
%choose the ramdom 105 samples for training
randnum=sort(randperm(length(label),length(label)*0.7));
randremain=setdiff(1:length(label),randnum);
a_train=a(randnum,:);
y_train=label(randnum,:);

a_test=a(randremain,:);
y_test=label(randremain,:);
% ck=label(1:length(label)*0.7,:);
ck=y_train;

%randomize parameter in [-1,1]
V = -1+2*rand(h,i);
W = -1+2*rand(i,j);
Phi = -1+2*rand(i,1);
Tau = -1+2*rand(j,1);
Phi=Phi';
Tau=Tau';
lossvec=[];
tic; %calculate time
for epoch=1:Maxepoch

    Phi = repmat(Phi(1,:), length(y_train), 1);
    Tau = repmat(Tau(1,:), length(y_train), 1);
    %sigmoid function g=1.0 ./ (1.0 + exp(-z));
    sigmoid=@(x)1.0 ./ (1.0+exp(-x));
    
    %forward propagation
    b=sigmoid(a_train*V-Phi);
    c=sigmoid(b*W-Tau);

    %compute output layer error
    d=c.*(1-c).*(ck-c);
    %compute hidden layer error
    e=b.*(1-b).*(d*W');
    
%     epoch=epoch+1;
    loss=sum(sum((ck'-c').^2)/2)/length(y_train);%训练目标最小化累积误差
%     fprintf('%f\n', loss)
    if(loss<=Toe)
         break
    end        

    lossvec=[lossvec,loss];

    %backword propagation
    for tmp2=1:length(y_train)
        DeltaW = Alpha*transpose(b(tmp2,:))*d(tmp2,:);
%         W = DeltaW+Gamma*W;
        W = DeltaW+W;
        DeltaV = Beta*transpose(a_train(tmp2,:))*e(tmp2,:);
%         V = DeltaV+Gamma*V;
        V = DeltaV+V;
%         Phi(1,:)=Beta*e(tmp,:)-Gamma*Phi(1,:);
%         Tau(1,:)=Alpha*d(tmp,:)-Gamma*Tau(1,:);
        Phi(1,:)=Phi(1,:)-Beta*e(tmp2,:);
        Tau(1,:)=Tau(1,:)-Alpha*d(tmp2,:);
    end
    
end
toc;%output time
%test data
b_test=sigmoid(a_test*V-repmat(Phi(1,:), length(y_test), 1));
c_test=sigmoid(b_test*W-repmat(Tau(1,:), length(y_test), 1));
%data analysis
[~,class] = max(c_test, [], 2);
accuracy = sum(class==y(randremain)+1)/length(y_test);
plot(1:length(lossvec),lossvec,'LineWidth',5)
fprintf('accuracy: %f\n',accuracy)
xlabel('epoch')
ylabel('loss')
title('loss-epoch变化图像')
% % for tmp1=1:Maxepoch
% %     for tmp2=1:length(y_train)
% %         sigmoid=@(x)1.0 ./ (1.0+exp(-x));
% %         b=sigmoid(a_train(tmp2,:)*V+Phi);
% %         c=sigmoid(b*W+Tau);
% %         d=c.*(1-c).*(ck(tmp2,:)-c);
% %         e=b.*(1-b).*(d*W');
% %         DeltaW = Alpha*transpose(b)*d;
% %         W=DeltaW+W;
% %         DeltaV=Beta*transpose(a_train(tmp2,:))*e;
% %         V=DeltaV+V;
% %         Phi=Phi-Beta*e;
% %         Tau=Tau-Alpha*d;
% %     end
% %     epoch=epoch+1;
% %     loss=sum((ck'-c').^2)/2;%训练目标最小化累积误差
% %     fprintf('%f\n', loss)
% %     if(loss<=Toe)
% %          break
% %     end   
% % end
% % c_test=[];
% % for tmp=1:length(y_test)
% %     b_test=sigmoid(a_test(tmp,:)*V+Phi);
% %     c_test_tmp=sigmoid(b_test*W+Tau);
% %     c_test=[c_test;c_test_tmp];
% % end
% 
% %use BP ToolBox Demo
% [x,t] = iris_dataset;
% net = feedforwardnet(10,'traingd');
% net = train(net,x,t);
% view(net)
% y = net(x);
% result=sim(net,x);
% %use Toolbox in this experiment
% a_train=a(randnum,:);
% y_train=y(randnum,:);
% a_test=a(randremain,:);
% y_test=y(randremain,:);
% net=feedforwardnet(5,'traingd');
% net=train(net,a_train',y_train');
% y_predict=sim(net,a_test');
% accuracy = sum(round(y_predict')==y_test)/length(y_test);
% fprintf('accuracy: %f\n',accuracy)
% %输入到隐层权值
% V=net.iw{1,1};
% %隐层阙值
% Phi=net.b{1}; 
% %隐层到输出层权值
% W=net.lw{2,1}; 
% %输出层阙值 
% Tau=net.b{2};