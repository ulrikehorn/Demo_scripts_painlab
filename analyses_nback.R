library(ggplot2)
library(reshape)

path <- '/home/raid3/uhorn/Documents/PsychoPy/PainExperiments/IMPRS Workshop/data'
sub = '04'

# load data from psychopy
setwd(paste(path, sep = ''))
df <- read.csv(paste(path,'/nback_result_',sub,'_hot.csv', sep = ''), na.strings=c("NA","NaN", " "))
df_rating <- read.csv(paste(path,'/nback_result_',sub,'_hot_ratings.csv', sep = ''), na.strings=c("NA","NaN", " "))

# make a barplot for the hot condition to see the effect on rating
p <- ggplot(df_rating, aes(x = Task, y = Rating, fill = Task)) +
  geom_boxplot(outlier.shape = NA) +
  ggtitle(paste('subject',sub,'pain ratings', sep = ' '))
p

# add information on rating
num_blocks = length(unique(df$block))
for (iblock in 1:num_blocks){
  df$task[df$block==iblock-1] = df_rating$Task[iblock]
  df$rating[df$block==iblock-1] = df_rating$Rating[iblock]
}
# add the label for the stimulation
df$stim = as.factor('hot')

# load the warm stimulation data as well
df2 <- read.csv(paste(path,'/nback_result_',sub,'_warm.csv', sep = ''), na.strings=c("NA","NaN", " "))
df_rating2 <- read.csv(paste(path,'/nback_result_',sub,'_warm_ratings.csv', sep = ''), na.strings=c("NA","NaN", " "))

# add information on rating
num_blocks = length(unique(df2$block))
for (iblock in 1:num_blocks){
  df2$task[df2$block==iblock-1] = df_rating2$Task[iblock]
  df2$rating[df2$block==iblock-1] = df_rating2$Rating[iblock]
}
# add the label for the stimulation
df2$stim = as.factor('warm')

# merge dataframes
df_all <- rbind(df, df2) 

# make a barplot to see the effect on performance
# look at scores at the end of a trial
p <- ggplot(df_all[df_all$Trials.thisN==max(df_all$Trials.thisN),], aes(x = stim, y = score, fill = stim)) +
  geom_boxplot(outlier.shape = NA) +
  ggtitle(paste('subject',sub,'performance', sep = ' '))
p
