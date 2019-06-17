function varargout = manual_artifact_selection(varargin)
% MANUAL_ARTIFACT_SELECTION MATLAB code for manual_artifact_selection.fig
%      MANUAL_ARTIFACT_SELECTION, by itself, creates a new MANUAL_ARTIFACT_SELECTION or raises the existing
%      singleton*.
%
%      H = MANUAL_ARTIFACT_SELECTION returns the handle to a new MANUAL_ARTIFACT_SELECTION or the handle to
%      the existing singleton*.
%
%      MANUAL_ARTIFACT_SELECTION('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in MANUAL_ARTIFACT_SELECTION.M with the given input arguments.
%
%      MANUAL_ARTIFACT_SELECTION('Property','Value',...) creates a new MANUAL_ARTIFACT_SELECTION or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before manual_artifact_selection_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to manual_artifact_selection_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help manual_artifact_selection

% Last Modified by GUIDE v2.5 21-May-2019 15:57:55

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @manual_artifact_selection_OpeningFcn, ...
                   'gui_OutputFcn',  @manual_artifact_selection_OutputFcn, ...
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


% --- Executes just before manual_artifact_selection is made visible.
function manual_artifact_selection_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to manual_artifact_selection (see VARARGIN)

% Choose default command line output for manual_artifact_selection
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

handles.data_path = getappdata(0,'data_path');
if ~isfile(handles.data_path)
    error('File not found')
end
load(handles.data_path,'data');

set(handles.text2,'String','Select start and end point of an artifact.');

% create an additional structure for the additional artifacts
data{6,1}.data = zeros(length(data{1,1}.data),1);
data{6,1}.header = 'manually selected artifacts';
handles.data = data;
handles.data_corr = data; %copy for corrected data
handles.sr = data{1,1}.header.sr;
handles.cue_onsets = handles.data{4,1}.data(handles.data{4,1}.markerinfo.name==...
    "pain_cue" | handles.data{4,1}.markerinfo.name=="no_pain_cue")*handles.sr;
handles.curr_trial = 1;
handles.artifact_found = 0;
interval = [handles.cue_onsets(handles.curr_trial):handles.cue_onsets(handles.curr_trial+1)];
axes(handles.plot1); % create plot window
datacursormode on;
guidata(hObject, handles);
cla; % clear plot content
plot(interval,handles.data{1,1}.data(interval,1));
xlabel({'time'});
ylabel({'pupil dilation (a.u.)'});
handles.dcm_obj = datacursormode(gcf);
guidata(hObject, handles);

% UIWAIT makes manual_artifact_selection wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = manual_artifact_selection_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in pushbutton1.
function pushbutton1_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

%     f = uifigure;
%     msg = 'Do you want to keep the changes?';
%     title = 'Confirm Save';
%     selection = uiconfirm(f,msg,title,...
%            'Options',{'Save','Discard'},...
%            'DefaultOption',2);
if handles.artifact_found
    button = questdlg('Do you want to save this?','Confirmation');
    if strcmpi(button, 'Yes')
       handles.data = handles.data_corr;
       handles.artifact_found = 0;
    end
    if strcmpi(button, 'No')
       handles.data_corr = handles.data;
       handles.artifact_found = 0;
    end
end
set(handles.text2,'String','Select start and end point of an artifact.');
if handles.curr_trial>1
    handles.curr_trial = handles.curr_trial-1;
end
if handles.curr_trial==length(handles.cue_onsets)
    interval = [round(handles.cue_onsets(handles.curr_trial)):length(handles.data{1,1}.data)];
else
    interval = [round(handles.cue_onsets(handles.curr_trial)):round(handles.cue_onsets(handles.curr_trial+1))];
end

% axes(handles.plot1); % create plot window
cla; % clear plot content
datacursormode on
plot(interval,handles.data{1,1}.data(interval));
xlabel({'time'});
ylabel({'pupil dilation (a.u.)'});
handles.dcm_obj = datacursormode(gcf);
guidata(hObject, handles);

% --- Executes on button press in pushbutton2.
function pushbutton2_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
if handles.artifact_found
    button = questdlg('Do you want to save this?','Confirmation');
    if strcmpi(button, 'Yes')
       handles.data = handles.data_corr;
       handles.artifact_found = 0;
    end
    if strcmpi(button, 'No')
       handles.data_corr = handles.data;
       handles.artifact_found = 0;
    end
end

set(handles.text2,'String','Select start and end point of an artifact.');
if handles.curr_trial<length(handles.cue_onsets)
    handles.curr_trial = handles.curr_trial+1;
end
if handles.curr_trial==length(handles.cue_onsets)
    interval = [round(handles.cue_onsets(handles.curr_trial)):length(handles.data{1,1}.data)];
else
    interval = [round(handles.cue_onsets(handles.curr_trial)):round(handles.cue_onsets(handles.curr_trial+1))];
end
% axes(handles.plot1); % create plot window
cla; % clear plot content
datacursormode on
plot(interval,handles.data{1,1}.data(interval));
xlabel({'time'});
ylabel({'pupil dilation (a.u.)'});
handles.dcm_obj = datacursormode(gcf);
guidata(hObject, handles);


% --- Executes on button press in okbutton.
function okbutton_Callback(hObject, eventdata, handles)
% hObject    handle to okbutton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
c_info = getCursorInfo(handles.dcm_obj);
if isempty(c_info)
    set(handles.text2,'String','You did not select anything.');
elseif length(c_info)==1
    set(handles.text2,'String','You only selected one data point. Hold shift to select two.');
elseif length(c_info)>2
    set(handles.text2,'String','Please select start and end point of only one artifact.');
else
    handles.artifact_found = 1;
    artifact_start = min(c_info(1).Position(1),c_info(2).Position(1));
    artifact_end = max(c_info(1).Position(1),c_info(2).Position(1));
    handles.data_corr{1,1}.data(artifact_start:artifact_end,1)=NaN;
    handles.data_corr{1,1}.data = fillmissing(handles.data_corr{1,1}.data, 'linear');
    if handles.curr_trial==length(handles.cue_onsets)
        interval = [round(handles.cue_onsets(handles.curr_trial)):length(handles.data{1,1}.data)];
    else
        interval = [round(handles.cue_onsets(handles.curr_trial)):round(handles.cue_onsets(handles.curr_trial+1))];
    end
    handles.data_corr{6,1}.data(artifact_start:artifact_end,1)=1;
    cla; % clear plot content
    datacursormode on
    plot(interval,handles.data_corr{1,1}.data(interval));
    xlabel({'time'});
    ylabel({'pupil dilation (a.u.)'});
    handles.dcm_obj = datacursormode(gcf);
    guidata(hObject, handles);
end


% --- Executes when user attempts to close figure1.
function figure1_CloseRequestFcn(hObject, eventdata, handles)
% hObject    handle to figure1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
if handles.artifact_found
    button = questdlg('Do you want to save this?','Confirmation');
    if strcmpi(button, 'Yes')
       handles.data = handles.data_corr;
       handles.artifact_found = 0;
    end
    if strcmpi(button, 'No')
       handles.data_corr = handles.data;
       handles.artifact_found = 0;
    end
end
button = questdlg('Do you want to save all your changes?','Confirmation');
if strcmpi(button, 'Yes')
    data = handles.data;
    [subj_path,name,~]= fileparts(handles.data_path);
    save(fullfile(subj_path,[name,'.mat']),'data');
    delete(hObject);
end
if strcmpi(button, 'No')
    delete(hObject);
end


% --- Executes during object deletion, before destroying properties.
function figure1_DeleteFcn(hObject, eventdata, handles)
% hObject    handle to figure1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% hObject    handle to figure1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
close