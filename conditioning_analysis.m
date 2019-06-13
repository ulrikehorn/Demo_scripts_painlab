% wrapper for analysis of fear conditioning demo data
clear
subjects          = {'01'};
num_subs          = numel(subjects);
dir_starting      = pwd;
data_path = '/data/pt_02121/Demo_Painlab/';

preprocessing = true;
manual_corr = true;
extract_trial_data = true;

% preprocessing
if preprocessing
    for isub=1:num_subs
        subj_path = fullfile(data_path);
        file_name = subjects{isub};
        asc_files = dir(fullfile(subj_path,[file_name,'*.asc']));
        asc_file_path = fullfile(subj_path,asc_files(1).name);
        
        % import the raw asc file, trim data
        % save preprocessed data and save some
        %  plots if make_plots == true
        % asc_import(full_file,make_plots, overwrite)
        asc_import(asc_file_path, true, false);
        
        % a pspm file was created which contains the imported data
        data_file_path = fullfile(subj_path, ['pspm_',file_name,'.mat']);
        % remove blinks by linear interpolation, extend the found blink by
        % b ms before and a ms after
        % remove_blinks(data_file_path, b, a)
        remove_blinks(data_file_path, 100, 150);
        
        % remove additional artifacts by going through the trials manually
        % and saving weird time points
        if manual_corr
            interp_data_file_path = fullfile(subj_path, ['pspm_', file_name,'_interpol.mat']);
            setappdata(0,'data_path',interp_data_file_path);
            manual_artifact_selection;
            uiwait(manual_artifact_selection);
        end
        
        % filter the interpolated data and save again
        interp_data_file_path = fullfile(subj_path, ['pspm_', file_name,'_interpol_man.mat']);
        
        filter_pupil_data(interp_data_file_path);
        
    end
end

% load interpolated and preprocessed data
% and extract trial wise data (all blocks in a row)
if extract_trial_data
    
    % all intervals relative to cue onset in seconds!
    
    %     % anticipation baseline 1s before cue onset to cue onset
    %     antic_baseline = [-1 0];
    % anticipation baseline cue onset to cue onset +1s
    antic_baseline = [0 1];
    % anticipation interval 1s to 5s after cue onset = no confound
    % by stimulation
    antic_interval = [1 5];
    
    % stimulation onset is 5s after cue onset
    stim = 5;
    % stimulation baseline: 1s before stimulation onset to stimulation onset
    % comparable to anticipation baseline
    stim_baseline = [stim-1 stim];
    % stimulation interval: 1s after stimulation onset to 5s after stimulation offset
    stim_interval = [stim+1 stim+1.5+5];
    
    for isub=1:num_subs
        trial_data = [];
        subj_path = fullfile(data_path);
        % returns plots and a response amplitude value for each trial over
        % all blocks
        %         trial_data.pd_amp_stim_min = trialize_pd(subj_path, subjects{isub},...
        %             num_blocks, stim_baseline, stim_interval, 'min', false);
        trial_data.pd_amp_antic_min = trialize_pd(subj_path, subjects{isub},...
            antic_baseline, antic_interval, 'min', true, false);
        %         trial_data.pd_amp_whole_min = trialize_pd(subj_path, subjects{isub},...
        %             num_blocks, antic_baseline, stim_interval, 'min', true);
        t = struct2table(trial_data);
        writetable(t,fullfile(subj_path,[subjects{isub} '_trial_data.csv']));
        
    end
    
end

cd(dir_starting);