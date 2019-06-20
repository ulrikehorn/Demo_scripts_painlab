function trialize_pd(subj_path, subject, baseline, interval)

addpath(genpath('/NOBACKUP2/Demo_Painlab/eeglab14_1_2b'))

% if that ratio of samples in a trial is NaN we discard the trial
trial_discard_criterion = 0.5;

color_pain = [165,15,21]/255;
color_no_pain = [251,106,74]/255;

fighandle = figure;

load(fullfile(subj_path,['pspm_', subject,'_interpol_filt.mat']),'data');
% if you selected manual artifact correction there are 6 parts, otherwise 5
% data contains 6 parts: pupil dilation, x, y, marker, blinks and manually
% selected artifacts
% combine blinks and manual artifacts
if length(data)>5
    data{6,1}.data = data{5,1}.data | data{6,1}.data;
else
    data{6,1}.data = data{5,1}.data;
end

sr = data{1,1}.header.sr;

% ------------slice data into trials----------------
cue_onsets = data{4,1}.data(data{4,1}.markerinfo.name=="pain_cue" | data{4,1}.markerinfo.name=="no_pain_cue")*sr;
num_trials = length(cue_onsets);

% for time courses epoch from baseline-1s to interval+1s to have a nice
% plot
num_samples = (interval(2)+1)*sr - (baseline(1)-1)*sr;
blink_epo = zeros(num_samples,num_trials);
pd_epo = zeros(num_samples,num_trials);
for trial = 1:num_trials
    % epoch the blinks in the same way to be able to check whether
    % whole trials are invalid, remove these from the plot
    blink_epo(:,trial) = data{6,1}.data(round(cue_onsets(trial) + (baseline(1)-1)*sr):...
        round(cue_onsets(trial) + (interval(2)+1)*sr)-1,1);
    if sum(blink_epo(:,trial)==1) > num_samples*trial_discard_criterion
        pd_epo(:,trial) = NaN(num_samples,1);
    else
        pd_epo(:,trial) = data{1,1}.data(round(cue_onsets(trial) + (baseline(1)-1)*sr):...
            round(cue_onsets(trial) + (interval(2)+1)*sr)-1,1);
    end
end

pd_epo_baseline_locked = pd_epo;
for itrial=1:num_trials
    pd_epo_baseline_locked(:,itrial) = pd_epo_baseline_locked(:,itrial) - pd_epo_baseline_locked(1*sr,itrial);
end

% read behavioural data
behav_table = readtable(fullfile(subj_path,[subject '.csv']));
pain_ind = strcmp(behav_table.pain,'pain');
% change here when you have inserted ITI after the end
pain_ind(end)=[];
no_pain_ind = strcmp(behav_table.pain,'no pain');
% change here when you have inserted ITI after the end
no_pain_ind(end) = [];


x = 1/sr:1/sr:size(pd_epo_baseline_locked,1)/sr;
mean_pain = mean(pd_epo_baseline_locked(:,pain_ind), 2)';
sem_pain = (std(pd_epo_baseline_locked(:,pain_ind), 0, 2)/...
    sqrt(size(pd_epo_baseline_locked(:,pain_ind),2)))';
mean_no_pain = mean(pd_epo_baseline_locked(:,no_pain_ind), 2)';
sem_no_pain = (std(pd_epo_baseline_locked(:,no_pain_ind), 0, 2)/...
    sqrt(size(pd_epo_baseline_locked(:,no_pain_ind),2)))';
clf(fighandle);
% plot it once to get the ylim
hold on
h1a = fill([x fliplr(x)],[mean_pain + sem_pain fliplr(mean_pain - sem_pain)],...
    color_pain, 'FaceAlpha', 0.2,'linestyle','none');
h1 = plot(x, mean_pain, 'Color', color_pain, 'LineWidth',3);
h2a = fill([x fliplr(x)],[mean_no_pain + sem_no_pain fliplr(mean_no_pain - sem_no_pain)],...
    color_no_pain, 'FaceAlpha', 0.2,'linestyle','none');
h2 = plot(x, mean_no_pain, 'Color', color_no_pain, 'LineWidth',3);
ylimits_save = ylim();
% plus and minus a bit of offset
ylimits = [ylimits_save(1)-(ylimits_save(2)-ylimits_save(1))*0.1 ...
    ylimits_save(2)+(ylimits_save(2)-ylimits_save(1))*0.1];
hold off
% clear and plot again, now with rectangles in the back
clf(fighandle)
hold on
ylim(ylimits)
h7 = line([-(baseline(1)-1) -(baseline(1)-1)], get(gca,'ylim'),'Color','k');
h8 = rectangle('Position',[(baseline(1)-(baseline(1)-1)) ylimits(1) (baseline(2)-baseline(1)) diff(ylimits)],...
    'FaceColor',[0.5 1 0.5 0.3],'EdgeColor','none');
h8a = line(NaN,NaN,'LineWidth',3,'Color',[0.5 1 0.5 0.3]);
h9 = rectangle('Position',[(interval(1)-(baseline(1)-1)) ylimits(1) (interval(2)-interval(1)) diff(ylimits)],...
    'FaceColor',[0.5 0.5 1 0.3],'EdgeColor','none');
h9a = line(NaN,NaN,'LineWidth',3,'Color',[0.5 0.5 1 0.3]);
h1a = fill([x fliplr(x)],[mean_pain + sem_pain fliplr(mean_pain - sem_pain)],...
    color_pain, 'FaceAlpha', 0.2,'linestyle','none');
h1 = plot(x, mean_pain, 'Color', color_pain, 'LineWidth',3);
h2a = fill([x fliplr(x)],[mean_no_pain + sem_no_pain fliplr(mean_no_pain - sem_no_pain)],...
    color_no_pain, 'FaceAlpha', 0.2,'linestyle','none');
h2 = plot(x, mean_no_pain, 'Color', color_no_pain, 'LineWidth',3);
hold off
legend([h1 h2 h7 h8a h9a], 'pain', 'no pain', 'cue onset', 'baseline',...
    'interval of interest','Location', 'NorthWest');
xlabel('seconds')
ylabel('pupil dilation (a.u.)')
title(['Averaged pupil dilation ' subject])
saveas(fighandle, fullfile(subj_path,[subject '_PD_conditions_'...
    num2str(baseline(1)) '_' num2str(baseline(2)) '_' ...
    num2str(interval(1)) '_' num2str(interval(2)) '.png']))

end