function filter_pupil_data(data_file_path)

load(data_file_path, 'data');
[subj_path, name, ~] = fileparts(data_file_path);

sr = data{1,1}.header.sr;

% filter the pupil dilation data
% 1st order butterworth filter (iir) low pass 5 Hz
order    = 1;
fcuthigh = 5;
[b,a]    = butter(order,fcuthigh/(sr/2), 'low');
filt_data = filtfilt(b,a,data{1,1}.data);

% get it back into the structure and save it
data{1,1}.data = filt_data;
save(fullfile(subj_path,[name,'_filt.mat']),'data');
fprintf('Saved interpolated and filtered data as: %s \n',fullfile(subj_path,[name,'_filt','.mat']));
end