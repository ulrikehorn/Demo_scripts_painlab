library(ggplot2)
library(reshape)
library(gridExtra)

path <- '/home/raid3/uhorn/Documents/PsychoPy/PainExperiments/IMPRS Workshop/data'
sub = '1'

# load data from psychopy
setwd(paste(path, sep = ''))
df <- read.csv(paste(path,'/nback_result_',sub,'.csv', sep = ''), na.strings=c("NA","NaN", " "))
df_overview <- read.csv(paste(path,'/nback_result_',sub,'_ratings.csv', sep = ''), na.strings=c("NA","NaN", " "))

# make a barplot for the hot condition to see the effect on rating
p <- ggplot(df_overview[df_overview$Stim=='hot',], aes(x = Task, y = Rating, fill = Task)) +
  geom_boxplot(outlier.shape = NA) + ylim(50,100) + 
  ggtitle(paste('subject',sub,'effect of attention on pain ratings', sep = ' '))
p

# add information on rating
num_blocks = length(unique(df$block))
for (iblock in 1:num_blocks){
  df$task[df$block==iblock-1] = df_overview$Task[iblock]
  df$rating[df$block==iblock-1] = df_overview$Rating[iblock]
  df$stim[df$block==iblock-1] = df_overview$Stim[iblock]
  if (df_overview$Task[iblock]=='control'){
    df_overview$num_targets[iblock] = NaN
    df_overview$num_correct[iblock] = NaN
    df_overview$num_missed[iblock] = NaN
    df_overview$num_wrong[iblock] = NaN
    df_overview$max_score[iblock] = NaN
    df_overview$score[iblock] = NaN
    df_overview$score_diff[iblock] = NaN
    df_overview$rt[iblock] = NaN
  }
  else{
    df_overview$num_targets[iblock] = sum(df$target[df$block==iblock-1])
    df_overview$num_correct[iblock] = sum(df$response[df$block==iblock-1 & df$response==1])
    df_overview$num_missed[iblock] = length(df$response[df$block==iblock-1 & df$response==-2])
    df_overview$num_wrong[iblock] = length(df$response[df$block==iblock-1 & df$response==-1])
    df_overview$max_score[iblock] = df_overview$num_targets[iblock]*15
    df_overview$score[iblock] = df$score[df$block==iblock-1 & df$Trials.thisN==max(df$Trials.thisN)]
    df_overview$score_diff[iblock] = df_overview$score[iblock]-df_overview$max_score[iblock]
    df_overview$rt[iblock] = mean(df$rt[df$block==iblock-1 & df$response==1])
  }
}
# rename factors
df$stim=as.factor(df$stim)
levels(df$stim) <- c("hot","warm")
df$task=as.factor(df$task)
levels(df$task) <- c("control","nback")
df_overview$percent_correct = df_overview$num_correct/df_overview$num_targets*100

Stim <- c('hot', 'warm')
df_sums <- data.frame(Stim)
df_sums$targets <- c(sum(df_overview$num_targets[df_overview$Stim=='hot' & df_overview$Task=='nback']),
                     sum(df_overview$num_targets[df_overview$Stim=='warm'& df_overview$Task=='nback']))
df_sums$hits <- c(sum(df_overview$num_correct[df_overview$Stim=='hot' & df_overview$Task=='nback']),
                     sum(df_overview$num_correct[df_overview$Stim=='warm'& df_overview$Task=='nback']))
df_sums$misses <- c(sum(df_overview$num_missed[df_overview$Stim=='hot' & df_overview$Task=='nback']),
                  sum(df_overview$num_missed[df_overview$Stim=='warm'& df_overview$Task=='nback']))
df_sums$false_alarms <- c(sum(df_overview$num_wrong[df_overview$Stim=='hot' & df_overview$Task=='nback']),
                    sum(df_overview$num_wrong[df_overview$Stim=='warm'& df_overview$Task=='nback']))

# make a barplot to see the effect on performance
# 1. target hits
p1 <- ggplot(df_sums, aes(x = Stim, y = hits, fill = Stim)) +
  geom_bar(stat="identity") +
  #geom_jitter(position=position_jitter(width=.1, height=0))+
  geom_hline(yintercept=12, linetype="dashed", color = "black") +
  labs(x = 'heat stimulation condition', y = 'overall number of hits') +
  ggtitle(paste('subject',sub,'sum of hits', sep = ' '))

# 2. misses
p2 <- ggplot(df_sums, aes(x = Stim, y = misses, fill = Stim)) +
  geom_bar(stat="identity") + ylim(0,max(df_sums$misses+1)) + 
  labs(x = 'heat stimulation condition', y = 'overall number of misses') +
  ggtitle(paste('subject',sub,'sum of misses', sep = ' '))

# 3. compare how often the subject wrongly pressed
p3 <- ggplot(df_sums, aes(x = Stim, y = false_alarms, fill = Stim)) +
  geom_bar(stat="identity") + ylim(0,max(df_sums$false_alarms+1)) + 
  labs(x = 'heat stimulation condition', y = 'overall number of false alarms') +
  ggtitle(paste('subject',sub,'sum of false alarms', sep = ' '))

# 4. compare the reaction times
p4 <- ggplot(df_overview, aes(x = Stim, y = rt, fill = Stim)) +
  geom_boxplot(outlier.shape = NA) +
  labs(x = 'heat stimulation condition', y = 'reaction times (s)') +
  ggtitle(paste('subject',sub,'average reaction times for hits', sep = ' '))

grid.arrange(p1, p2, p3, p4, nrow = 2, top = 'effect of pain on performance')
