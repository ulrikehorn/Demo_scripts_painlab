% this function loads the eeg file corresponding to the given header file
% using eeglab functionality
% in the beginning files have been named inconsistently
% that's why you now need information about file name AND block number
% later you can implement a clean version where you don't need all of it

function brainamp_import(vhdr_file, subject, make_plots)

[subj_path,name,~] = fileparts(vhdr_file);

addpath(genpath('/NOBACKUP2/Demo_Painlab/eeglab14_1_2b'))

% load all channels at once
raw = pop_loadbv(subj_path, [name '.vhdr']);
num_channels = length(raw.chanlocs);

% sampling rate
sr = raw.srate;

% search for markers
num_events = length(raw.event);
marker1 = [];
marker2 = [];
i=1;
j=1;
for e=1:num_events
    if (strcmp(raw.event(1,e).type, 'S  8'))
        marker1(i) = raw.event(1,e).latency;
        i = i+1;
    elseif (strcmp(raw.event(1,e).type, 'S  2'))
        marker2(j) = raw.event(1,e).latency;
        j = j+1;
    end
end

% trim data
start_exp = min(min(marker1),min(marker2)); %first marker is first ITI onset
stop_exp = max(max(marker1),max(marker2))+2*sr; %last marker marks end of experiment

trim = pop_select(raw, 'point', [start_exp stop_exp]);

%------------GSR-------------
% load first channel with GSR in name
for ichannel=1:num_channels
    if contains(trim.chanlocs(ichannel).labels,'GSR','IgnoreCase',true)
        gsr = pop_select(trim, 'channel', ichannel);
        break
    end
end

% downsample data??
new_sr = 100;
gsr_filt = [];
gsr_down = [];
gsr_down = pop_resample(gsr, new_sr);
gsr_down.data = double(gsr_down.data);

gsr_filt = gsr_down;

% 1st order butterworth filter (iir) bandpass 0.0159 - 5 Hz
order    = 1;
fcutlow  = 0.0159;
fcuthigh = 5;
[b,a]    = butter(order,[fcutlow,fcuthigh]/(new_sr/2));
filt_data = filtfilt(b,a,gsr_down.data);
if size(filt_data,1)==1
    gsr_filt.data = filt_data;
else
    gsr_filt.data = filt_data';
end

save(fullfile(subj_path,[subject '_gsr_filt.mat']), 'gsr_filt');
fprintf('Saved data as: %s \n',fullfile(subj_path,[subject '_gsr_filt.mat']));

if make_plots
    % plot GSR data
    figure;
    hold on
    h1 = plot(gsr.times/sr, gsr.data);      % plot raw
    h2 = plot(gsr_filt.times/sr, gsr_filt.data, 'r');      % plot filtered
    hold off
    xlabel('seconds')
    ylabel('skin conductance \muS')
    legend([h1 h2], 'raw data', 'filtered');
    title('Skin conductance')
    savefig(fullfile(subj_path,[subject '_GSR.fig']));
    close
end

end