library(ggplot2)
library(reshape)

path <- '/home/raid3/uhorn/Documents/PsychoPy/PainExperiments/IMPRS Workshop/data'
sub = '03'

# load data from psychopy
setwd(paste(path, sep = ''))
df <- read.csv(paste(path,'/nback_result_',sub,'.csv', sep = ''), na.strings=c("NA","NaN", " "))
df_overview <- read.csv(paste(path,'/nback_result_',sub,'_ratings.csv', sep = ''), na.strings=c("NA","NaN", " "))

# make a barplot for the hot condition to see the effect on rating
p <- ggplot(df_overview[df_overview$Stim=='hot',], aes(x = Task, y = Rating, fill = Task)) +
  geom_boxplot(outlier.shape = NA) +
  ggtitle(paste('subject',sub,'pain ratings', sep = ' '))
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
  }
  else{
    df_overview$num_targets[iblock] = sum(df$target[df$block==iblock-1])
    df_overview$num_correct[iblock] = sum(df$response[df$block==iblock-1 & df$response==1])
    df_overview$num_missed[iblock] = length(df$response[df$block==iblock-1 & df$response==-2])
    df_overview$num_wrong[iblock] = length(df$response[df$block==iblock-1 & df$response==-1])
  }
}
df_overview$percent_correct = df_overview$num_correct/df_overview$num_targets*100
# rename factors
df$stim=as.factor(df$stim)
levels(df$stim) <- c("hot","warm")
df$task=as.factor(df$task)
levels(df$task) <- c("control","nback")

# make a barplot to see the effect on performance
# 1. look at scores at the end of a trial
p <- ggplot(df[df$Trials.thisN==max(df$Trials.thisN),], aes(x = stim, y = score, fill = stim)) +
  geom_boxplot(outlier.shape = NA) +
  ggtitle(paste('subject',sub,'performance score', sep = ' '))
p

# 2. compare how many targets the subject had correct
p <- ggplot(df_overview, aes(x = Stim, y = percent_correct, fill = Stim)) +
  geom_boxplot(outlier.shape = NA) +
  ggtitle(paste('subject',sub,'performance - target hits in percent', sep = ' '))
p

# 3. compare how often the subject wrongly pressed
p <- ggplot(df_overview, aes(x = Stim, y = num_wrong, fill = Stim)) +
  geom_boxplot(outlier.shape = NA) +
  ggtitle(paste('subject',sub,'performance - wrongly pressed', sep = ' '))
p