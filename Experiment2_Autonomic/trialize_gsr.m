function trialize_gsr(subj_path, subject, baseline, interval)

addpath(genpath('/NOBACKUP2/Demo_Painlab/eeglab14_1_2b'))

color_pain = [165,15,21]/255;
color_no_pain = [251,106,74]/255;

course_data = [];

fighandle = figure;

load(fullfile(subj_path,[subject '_gsr_filt.mat']), 'gsr_filt');

sr = gsr_filt.srate;

% epoch data using cue onset marker
num_events = length(gsr_filt.event);
cue_onsets = [];
j=1;
for e=1:num_events
    if (strcmp(gsr_filt.event(1,e).type, 'S  4'))
        cue_onsets(j) = gsr_filt.event(1,e).latency;
        j = j+1;
    end
end

% for time courses epoch from baseline-1s to interval+1s to have a nice
% plot
gsr_epo = epoch(gsr_filt.data, cue_onsets, [(baseline(1)-1)*sr (interval(2)+1)*sr]);

gsr_course = squeeze(gsr_epo); % removes useless channel dimension

% read behavioural data
behav_table = readtable(fullfile(subj_path,[subject '.csv']));
pain_ind = strcmp(behav_table.pain,'pain');
no_pain_ind = strcmp(behav_table.pain,'no pain');

% read behavioural data
num_trials = size(gsr_course,2);
if num_trials ~= size(behav_table,1)
    error('Trial number in csv file does not match trial number in data')
end

% start at zero with cue onset
for itrial=1:num_trials
    gsr_course(:,itrial) = gsr_course(:,itrial) - gsr_course(1*sr,itrial);
end

x = 1/sr:1/sr:size(gsr_course,1)/sr;

mean_pain = mean(gsr_course(:,pain_ind), 2)';
sem_pain = (std(gsr_course(:,pain_ind), 0, 2)/...
    sqrt(size(gsr_course(:,pain_ind),2)))';
mean_no_pain = mean(gsr_course(:,no_pain_ind), 2)';
sem_no_pain = (std(gsr_course(:,no_pain_ind), 0, 2)/...
    sqrt(size(gsr_course(:,no_pain_ind),2)))';

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
legend([h1 h2 h7 h8a h9a], 'pain', 'no pain',...
    'cue onset', 'baseline',...
    'interval of interest','Location', 'NorthWest');
xlabel('seconds')
ylabel('skin conductance \muS')
title(['Averaged skin conductance ' subject])
saveas(fighandle, fullfile(subj_path,[subject '_GSR_conditions_'...
    num2str(baseline(1)) '_' num2str(baseline(2)) '_' ...
    num2str(interval(1)) '_' num2str(interval(2)) '.png']))


end