function varargout = Image_Retrivel(varargin)
% IMAGE_RETRIVEL MATLAB code for Image_Retrivel.fig
%      IMAGE_RETRIVEL, by itself, creates a new IMAGE_RETRIVEL or raises the existing
%      singleton*.
%
%      H = IMAGE_RETRIVEL returns the handle to a new IMAGE_RETRIVEL or the handle to
%      the existing singleton*.
%
%      IMAGE_RETRIVEL('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in IMAGE_RETRIVEL.M with the given input arguments.
%
%      IMAGE_RETRIVEL('Property','Value',...) creates a new IMAGE_RETRIVEL or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before Image_Retrivel_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to Image_Retrivel_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help Image_Retrivel

% Last Modified by GUIDE v2.5 05-Jan-2019 21:15:37

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @Image_Retrivel_OpeningFcn, ...
                   'gui_OutputFcn',  @Image_Retrivel_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before Image_Retrivel is made visible.
function Image_Retrivel_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to Image_Retrivel (see VARARGIN)

% Choose default command line output for Image_Retrivel
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes Image_Retrivel wait for user response (see UIRESUME)
% uiwait(handles.figure1);

% setappdata(handles.PicSelectBtn,'FilePath',0);
global FilePath ;%当前输入文件全路径
FilePath = 0;

% --- Outputs from this function are returned to the command line.
function varargout = Image_Retrivel_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in PicSelectBtn.
function PicSelectBtn_Callback(hObject, eventdata, handles)
% hObject    handle to PicSelectBtn (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global FilePath;
[FileName,FileDir] = uigetfile({'*.jpg'},'Pick an image');
if FileName == 0
    errordlg('You have not select any image','WrongInput');
else
    axes(handles.OrignalAxes);%用axes命令设定当前操作的坐标轴是OrignalAxes
    FilePath = [FileDir FileName];
    PicData = imread(FilePath);
    imshow(PicData);
%     setappdata(handles.PicSelectBtn,'FilePath',FilePath);
end


% --- Executes on button press in ahashbtn.
function ahashbtn_Callback(hObject, eventdata, handles)
% hObject    handle to ahashbtn (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% FilePath = getappdata(handles.PicSelectButton,'FilePath');
global FilePath;
if FilePath == 0
    errordlg('清先选择图片','WrongInput');
else
    [FileDir,~,~] = fileparts(FilePath);
    [HashResult,distance] = rank_show(FilePath, 'ahash');
    axes(handles.Pic1Axes);%用axes命令设定当前操作的坐标轴
    imshow(fullfile(FileDir,  HashResult{1}))
    axes(handles.Pic2Axes);%用axes命令设定当前操作的坐标轴
    imshow(fullfile(FileDir,  HashResult{2}))
    axes(handles.Pic3Axes);%用axes命令设定当前操作的坐标轴
    imshow(fullfile(FileDir, HashResult{3}))
    set(handles.dist1,'String',['dist:' num2str(distance(1))] );
    set(handles.dist2,'String',['dist:' num2str(distance(2))] );
    set(handles.dist3,'String',['dist:' num2str(distance(3))] );
end

% --- Executes on button press in phashbtn.
function phashbtn_Callback(hObject, eventdata, handles)
% hObject    handle to phashbtn (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global FilePath;
if FilePath == 0
    errordlg('清先选择图片','WrongInput');
else
    [FileDir,~,~] = fileparts(FilePath);
    [HashResult,distance] = rank_show(FilePath, 'phash');
    axes(handles.Pic1Axes);%用axes命令设定当前操作的坐标轴
    imshow(fullfile(FileDir,  HashResult{1}))
    axes(handles.Pic2Axes);%用axes命令设定当前操作的坐标轴
    imshow(fullfile(FileDir,  HashResult{2}))
    axes(handles.Pic3Axes);%用axes命令设定当前操作的坐标轴
    imshow(fullfile(FileDir, HashResult{3}))
    set(handles.dist1,'String',['dist:' num2str(distance(1))] );
    set(handles.dist2,'String',['dist:' num2str(distance(2))] );
    set(handles.dist3,'String',['dist:' num2str(distance(3))] );
end

% --- Executes on button press in dhashbtn.
function dhashbtn_Callback(hObject, eventdata, handles)
% hObject    handle to dhashbtn (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global FilePath;
if FilePath == 0
    errordlg('清先选择图片','WrongInput');
else
    [FileDir,~,~] = fileparts(FilePath);
    [HashResult,distance] = rank_show(FilePath, 'dhash');
    axes(handles.Pic1Axes);%用axes命令设定当前操作的坐标轴
    imshow(fullfile(FileDir,  HashResult{1}))
    axes(handles.Pic2Axes);%用axes命令设定当前操作的坐标轴
    imshow(fullfile(FileDir,  HashResult{2}))
    axes(handles.Pic3Axes);%用axes命令设定当前操作的坐标轴
    imshow(fullfile(FileDir, HashResult{3}))

    set(handles.dist1,'String',['dist:' num2str(distance(1))] );
    set(handles.dist2,'String',['dist:' num2str(distance(2))] );
    set(handles.dist3,'String',['dist:' num2str(distance(3))] );
%     set(handles.dist3,'String',[HashResult{3} 'dist:' num2str(distance(3))] );
end
