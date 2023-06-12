function varargout = GUI(varargin)

gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @GUI_OpeningFcn, ...
                   'gui_OutputFcn',  @GUI_OutputFcn, ...
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

function GUI_OpeningFcn(hObject, eventdata, handles, varargin)

handles.output = hObject;

guidata(hObject, handles);

function varargout = GUI_OutputFcn(hObject, eventdata, handles) 
varargout{1} = handles.output;

function slider1_Callback(hObject, eventdata, handles)
sliderValue = get(hObject, 'Value');
set_param('scheme/dB Gain1', 'db', num2str(sliderValue));
set(handles.text1, 'String', sprintf('%0.2f', sliderValue));
drawnow

function slider1_CreateFcn(hObject, eventdata, handles)
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end

function text1_CreateFcn(hObject, eventdata, handles)
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end

function slider2_Callback(hObject, eventdata, handles)
sliderValue = get(hObject, 'Value');
set_param('scheme/dB Gain2', 'db', num2str(sliderValue));
set(handles.text2, 'String', sprintf('%0.2f', sliderValue));
drawnow

function slider2_CreateFcn(hObject, eventdata, handles)
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


function slider3_Callback(hObject, eventdata, handles)
sliderValue = get(hObject, 'Value');
set_param('scheme/dB Gain3', 'db', num2str(sliderValue));
set(handles.text3, 'String', sprintf('%0.2f', sliderValue));
drawnow

function slider3_CreateFcn(hObject, eventdata, handles)
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


function slider4_Callback(hObject, eventdata, handles)
sliderValue = get(hObject, 'Value');
set_param('scheme/dB Gain4', 'db', num2str(sliderValue));
set(handles.text4, 'String', sprintf('%0.2f', sliderValue));
drawnow

function slider4_CreateFcn(hObject, eventdata, handles)
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


function slider5_Callback(hObject, eventdata, handles)
sliderValue = get(hObject, 'Value');
set_param('scheme/dB Gain5', 'db', num2str(sliderValue));
set(handles.text5, 'String', sprintf('%0.2f', sliderValue));
drawnow

function slider5_CreateFcn(hObject, eventdata, handles)
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


function slider6_Callback(hObject, eventdata, handles)
sliderValue = get(handles.slider6, 'Value');
set_param('scheme/dB Gain6', 'db', num2str(sliderValue));
set(handles.text6, 'String', sprintf('%0.2f', sliderValue));
drawnow

function slider6_CreateFcn(hObject, eventdata, handles)
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


function slider7_Callback(hObject, eventdata, handles)
sliderValue = get(handles.slider7, 'Value');
set_param('scheme/dB Gain7', 'db', num2str(sliderValue));
set(handles.text7, 'String', sprintf('%0.2f', sliderValue));
drawnow

function slider7_CreateFcn(hObject, eventdata, handles)
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


function slider8_Callback(hObject, eventdata, handles)
sliderValue = get(handles.slider8, 'Value');
set_param('scheme/dB Gain8', 'db', num2str(sliderValue));
set(handles.text8, 'String', sprintf('%0.2f', sliderValue));
drawnow

function slider8_CreateFcn(hObject, eventdata, handles)

if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


function radiobutton1_Callback(hObject, eventdata, handles)
if get(hObject,'Value') == 1
    load_system('scheme.slx');
    set_param('scheme', 'SimulationCommand', 'start');
else
    set_param('scheme', 'SimulationCommand', 'stop');
end


function radiobutton2_Callback(hObject, eventdata, handles)
switch_block_handle = get_param('scheme/DelaySwitch', 'Handle');
if handles.radiobutton2.Value == 1
    set_param(switch_block_handle, 'sw', '0');
else
    set_param(switch_block_handle, 'sw', '1');
end


function radiobutton3_Callback(hObject, eventdata, handles)
switch_block_handle = get_param('scheme/VibratoSwitch', 'Handle');
if handles.radiobutton3.Value == 1
    set_param(switch_block_handle, 'sw', '0');
else
    set_param(switch_block_handle, 'sw', '1');
end


function volume_slider_Callback(hObject, eventdata, handles)
sliderValue = get(handles.volume_slider, 'Value');
set_param('scheme/Volume Gain', 'db', num2str(sliderValue));
set(handles.volume_text, 'String', sprintf('%0.1f', sliderValue));
drawnow

function volume_slider_CreateFcn(hObject, eventdata, handles)
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


function browse_button_Callback(hObject, eventdata, handles)
[file, path] = uigetfile({'*.wav'; '*.mp3'; '*.ogg'}, 'Select Audio File');
set_param('scheme/From Multimedia File', 'FileName', fullfile(path, file));
set(handles.browse_button, 'String', file);
