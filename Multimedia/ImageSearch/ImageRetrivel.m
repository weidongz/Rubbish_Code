function varargout = ImageRetrivel(varargin)
% IMAGERETRIVEL MATLAB code for ImageRetrivel.fig
%      IMAGERETRIVEL, by itself, creates a new IMAGERETRIVEL or raises the existing
%      singleton*.
%
%      H = IMAGERETRIVEL returns the handle to a new IMAGERETRIVEL or the handle to
%      the existing singleton*.
%
%      IMAGERETRIVEL('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in IMAGERETRIVEL.M with the given input arguments.
%
%      IMAGERETRIVEL('Property','Value',...) creates a new IMAGERETRIVEL or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before ImageRetrivel_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to ImageRetrivel_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help ImageRetrivel

% Last Modified by GUIDE v2.5 05-Jan-2019 19:32:39

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @ImageRetrivel_OpeningFcn, ...
                   'gui_OutputFcn',  @ImageRetrivel_OutputFcn, ...
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


% --- Executes just before ImageRetrivel is made visible.
function ImageRetrivel_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to ImageRetrivel (see VARARGIN)

% Choose default command line output for ImageRetrivel
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes ImageRetrivel wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = ImageRetrivel_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in PicSelectButton.
function PicSelectButton_Callback(hObject, eventdata, handles)
% hObject    handle to PicSelectButton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
[FileName,FileDir] = uigetfile({'*.jpg'},'Pick an image');
if FileName == 0
    errordlg('You have not select any image','WrongInput');
else
axes(handles.OrignalImage);%用axes命令设定当前操作的坐标轴是OrignalImage
FilePath = [FileDir FileName];
PicData = imread(FilePath);
imshow(PicData);
setappdata(handles.PicSelectButton,'FilePath',FilePath);
end


% --- Executes on button press in pushbutton2.
function pushbutton2_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
File2Path = getappdata(handles.PicSelectButton,'FilePath');
set(handles.FilePath,'String',File2Path);


% --- Executes during object creation, after setting all properties.
function OrignalImage_CreateFcn(hObject, eventdata, handles)
% hObject    handle to OrignalImage (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called
set(hObject,'xTick',[]);
set(hObject,'ytick',[]);
% Hint: place code in OpeningFcn to populate OrignalImage


% --- Executes on button press in ahash.
function ahash_Callback(hObject, eventdata, handles)
% hObject    handle to ahash (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
load AHashResult.mat AHashResult
FilePath = getappdata(handles.PicSelectButton,'FilePath');
PicData = imread(FilePath);
AHashData = get_ahash_value(PicData);
dist = [];
for i=1:size(AHashResult,2)
        dist(i,1) = sum(bitxor(AHashResult{1,i},AHashData));%Hamming distance
        [dist1,index] = sort(dist(:,1));
end
for tmp=1:3
    subplot(1,3,tmp);
    imshow([FileDir AHashResult{3,index(tmp)}])
end
