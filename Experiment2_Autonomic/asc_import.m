function asc_import(full_file, make_plots, overwrite)

% imports asc files and converts them to readable mat files
% if there exist some files, it overwrites them only if you want that
% it additionally generates some general plots

% To Do: check inputs
% plots/overwrite either True or false

% Initialise PSPM as customized version for the import from asc file
addpath(genpath('/NOBACKUP2/Demo_Painlab/pspm_customized/v4.0.2'));

[subj_path,name,~] = fileparts(full_file);

num_channels = 3;

pspm_file_exists = isfile(fullfile(subj_path,['pspm_', name,'.mat']));

% if you find a saved pspm data set check whether the user wants to
% overwrite this
% or if there is no file
% in these cases load with pspm
if (pspm_file_exists && overwrite) || ~pspm_file_exists
    %-----------PSPM import------------------
    datafile = cellstr(full_file);
    options = struct('overwrite',1);
    import = cell(1,4);
    import{1,1} = struct('type','pupil_l','channel',4,'eyelink_trackdist','none');
    import{1,2} = struct('type','gaze_x_l','channel',2,'eyelink_trackdist','none');
    import{1,3} = struct('type','gaze_y_l','channel',3,'eyelink_trackdist','none');
    import{1,4} = struct('type','marker','channel',1,'eyelink_trackdist','none');
    
    fprintf('Importing data with PsPM: %s \n',full_file);
    
    outfile = pspm_import(datafile, 'eyelink', import, options);
    load(outfile{1})
    
    % this calls the functions pspm_get_eyelink and import_eyelink (which have
    % been modified by me)
    % these steps read in the data, read saccade and blink information and set
    % data to NaN where the blink sorrounding saccades start and end 
    % (plus an offset of 0.05*sampling rate) --> currently no offset!
else
    fprintf('You chose not to overwrite the file %s \nUpcoming Plots show data from this file.\n',full_file);
    load(fullfile(subj_path,['pspm_',name,'.mat']),'data');
end

sr = data{1,1}.header.sr;
time = [1:1:length(data{1,1}.data)]/sr;
if make_plots
    %-----------Plot data raw-----------------
    % open the mat file the PSPM toolbox created
    % this mat file contains a data struct and an info struct
    % data{1,1} to data{4,1} represent the channels+marker
    % find out how many different marker values there are and what they
    % represent and assign different colors
    rng(19)
    data{4,1}.markerinfo.value(isnan(data{4,1}.markerinfo.value))=0; %convert NaN to 0
    markers = unique(data{4,1}.markerinfo.value);
    marker_colors = cell(1,length(markers));
    marker_names = cell(1,length(markers));
    for m = 1:length(markers)
        marker_names{m} = data{4,1}.markerinfo.name{data{4,1}.markerinfo.value==markers(m)};
        marker_colors{m} = rand(1,3);
    end
    plot_dummies = cell(1,length(markers));
    data_to_plot = gobjects(1,length(markers)+1);
    % all data channels as subplots with markers as specified in data{4,1}
    figure
    for i = 1:num_channels
        subplot(num_channels,1,i)
        hold on
        dataline = plot(time,data{i,1}.data, 'k');
        %             dataline = plot(time,preprocessed_data{i,1}.data, 'k');
        for j=1:length(data{4,1}.markerinfo.value)
            line([data{4,1}.data(j) data{4,1}.data(j)], get(gca,'ylim'),'Color',...
                marker_colors{data{4,1}.markerinfo.value(j)});
        end
        xlabel('seconds')
        ylabel(data{i,1}.header.units)
        
        data_to_plot(1,1) = dataline;
        for m=1:length(markers)
            plot_dummies{1,m} = plot([NaN,NaN], "color", marker_colors{m});
            data_to_plot(1,m+1) = plot_dummies{1,m};
        end
        legend(data_to_plot, data{i,1}.header.chantype, marker_names{:});
        hold off
    end
    saveas(gcf,fullfile(subj_path,[name,'_raw','.png']));
    close
    fprintf('Saved raw channel data figure as: %s \n',fullfile(subj_path,[name,'_raw','.png']));
    
    % convert x and y data to matrix so that you know how often the
    % gaze has been in that pixel
    % allocate matrix
    screen = zeros(length(0:1:1980)-1,length(0:1:1080)-1);
    for k = 1:length(time)
        x = round(data{2,1}.data(k));
        y = round(data{3,1}.data(k));
        if (1<=x)&&(x<=size(screen,1))&&(1<=y)&&(y<=size(screen,2))
            screen(x,y) = screen(x,y)+1;
        end
    end
    figure;
    img = imread('/data/pt_02121/Behav_Data/Behavioral_data_analyses/screen.png');
    imagesc(img);
    hold on
    colormap('hot')
    h = image(screen');
    colorbar
    set(h, 'AlphaData', 0.6);
    hold off
    saveas(gcf,fullfile(subj_path,[name,'_gaze','.png']));
    close
    fprintf('Saved gaze heatmap as: %s \n',fullfile(subj_path,[name,'_gaze','.png']));
end

end