% wrapper for analysis of fear conditioning demo data
clear
subjects          = {'003'};
num_subs          = numel(subjects);
dir_starting      = pwd;
data_path = '/NOBACKUP2/Demo_Painlab/data';

processing_gsr = true;
processing_pd = true;
manual_corr = false;
extract_trial_data = true;

% all intervals relative to cue onset in seconds!
% anticipation baseline cue onset to cue onset +1s
antic_baseline = [0 3.5];
% anticipation interval 1s to 3.5s after cue onset = no confound
% by stimulation
antic_interval = [3.5 8.5];

if processing_gsr
    for isub=1:num_subs
        subj_path = fullfile(data_path);
        file_name = subjects{isub};
        % import brain amp data and save gsr channel
        vhdr_file = fullfile(subj_path,[subjects{isub} '.vhdr']);
        % TO DO: check whether it exists?
        brainamp_import(vhdr_file, subjects{isub}, true);
        % returns plots
        trialize_gsr(subj_path, subjects{isub},...
            antic_baseline, antic_interval);
    end
end

if processing_pd
    for isub=1:num_subs
        subj_path = fullfile(data_path);
        file_name = subjects{isub};
        asc_files = dir(fullfile(subj_path,[file_name,'*.asc']));
        asc_file_path = fullfile(subj_path,asc_files(1).name);
        % import the raw asc file, trim data
        % save preprocessed data and save some
        %  plots if make_plots == true
        % asc_import(full_file,make_plots, overwrite)
        asc_import(asc_file_path, false, false);
        % a pspm file was created which contains the imported data
        data_file_path = fullfile(subj_path, ['pspm_',file_name,'.mat']);
        % remove blinks by linear interpolation, extend the found blink by
        % b ms before and a ms after
        % remove_blinks(data_file_path, b, a)
        remove_blinks(data_file_path, 100, 150);
        % remove additional artifacts by going through the trials manually
        % and saving weird time points
        interp_data_file_path = fullfile(subj_path, ['pspm_', file_name,'_interpol.mat']);
        if manual_corr
            setappdata(0,'data_path',interp_data_file_path);
            manual_artifact_selection;
            uiwait(manual_artifact_selection);
        end
        % filter the interpolated data and save again
        filter_pupil_data(interp_data_file_path);
        trialize_pd(subj_path, subjects{isub},...
            antic_baseline, antic_interval);
    end
end
cd(dir_starting);