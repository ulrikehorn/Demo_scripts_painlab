function remove_blinks(data_file_path, before, after)

% input: filepath to pspm_*.mat with eyetracking data
% remove blinks by linear interpolation, extend the found blink by
% b ms before and a ms after
% remove_blinks(data_file_path, b, a)

if ~isfile(data_file_path)
    error('File not found')
end

load(data_file_path,'data');

% interpolate NaNs in all channels by using the info in one channel
% --> not possible, because x and y already had some NaNs
% pupil is zero instead or really small when there is a blink
% so sometimes numbers differ for gaze and pupil data
% so maybe just combine them? (other possibility would be to look at those
% separately but the NaNs in the gaze give more hints which values of
% pupil data might also be corrupted)

% add a data column for blinks (either from gaze or pupil info)
data{5,1}.data = zeros(length(data{1,1}.data),1);
data{5,1}.data(isnan(data{1,1}.data) | isnan(data{2,1}.data) | isnan(data{3,1}.data)) = 1;
data{5,1}.header = 'blinks';
% pupil often only has a minimum amount of NaNs
data{1,1}.data(data{5,1}.data == 1) = NaN;

% TO DO: add possibility here to insert manually selected artefacts in form
% of loading a file?
% or better: write another function so that you can do that at any point

% channels:
% 1 pupil
% 2 gaze x
% 3 gaze y
% 4 marker
% 5 blinks

if any(isnan(data{1,1}.data))
    %-----------> set time points before and after also to NaN
    % convert ms values to data points although in our case it makes no
    % difference
    sr = data{1,1}.header.sr;
    before = before * sr / 1000;
    after = after * sr / 1000;
    for i = 1:length(data{1,1}.data)
        if (data{5,1}.data(i) == 1)
            data{1,1}.data(i-before:i+after) = NaN;
            data{2,1}.data(i-before:i+after) = NaN;
            data{3,1}.data(i-before:i+after) = NaN;
        end
    end
    
    % looking at pupil values which are abnormally low,
    % these can also be excluded
    % change this value if it does not fit the plot!
    %     figure; histogram((data{1,1}.data));
    %     hold on;
    %     cut_off = 1100;
    %     line([cut_off cut_off],get(gca,'ylim'),'Color',[1 0 0])
    %     hold off
    %     data{1,1}.data(data{1,1}.data < cut_off) = NaN;
    
    % interpolate missing data linearly and plot it
    data_interp = data;
    for ichannel = 1:3
        data_interp{ichannel,1}.data = fillmissing(data{ichannel,1}.data,'linear');
        fighandle = figure;
        plot(data_interp{ichannel,1}.data); hold on;
        plot(data{ichannel,1}.data); hold off
        close(fighandle);
    end

end

[subj_path,name,~] = fileparts(data_file_path);
data = data_interp; % rename it so that you can open all files no matter 
% what preprocessing they had and you can access structure called data
save(fullfile(subj_path,[name,'_interpol.mat']),'data');
fprintf('Saved interpolated data as: %s \n',fullfile(subj_path,[name,'_interpol','.mat']));

end