# twitfem
Feminism Tweet Analysis - Big Data Week Hackathon Project

Attitude analysis and corpus analytics of 1M tweets about feminism

[Link to slides.com presentation](https://slides.com/prooffreader/deck-4/)

Using a corpus of 988,000 tweets retrieved from Twitter's Search API from January to April 2015 containing the words "feminism", "feminist" or "feminists", we trained a classifier to label them as pro-feminist, anti-feminist or neither (regardless of sentiment), and determined the most characteristic words used by each group with the log-likelihood keyness method.


### GRAPHS:
- [Most Characteristic Words in Pro and Anti Feminist Tweets](https://plot.ly/~iamzaf/436/most-characteristic-words-in-pro-and-anti-feminist-tweets/)
- [Low Activity Accounts vs All Accounts](https://plot.ly/~iamzaf/557/low-activity-accounts-vs-all-accounts/)

##HPC McGill
[Instructions](https://www.tinyurl.com/bdw-mcgillhpc)

####To move files back and forth
#####GET a file
```bash
scp -P 57328 class03@aw-4r12-n03.hpc.mcgill.ca:/home/class03/path_to_file /local_path_to_put_file
```
#####PUT a file
```bash
scp -P 57328 /local_path_to_put_file class03@aw-4r12-n03.hpc.mcgill.ca:/home/class03/path_to_file
```
Team User Name: class03

Assigned Node: aw-4r12-n03.hpc.mcgill.ca

(ssh requires port flag -p 57328)

password: ask Dave

[running notebook (requires password)](https://aw-4r12-n03.hpc.mcgill.ca:8088)

you need to accept the cerificate

##RadialPoint Repo
[on github](http://www.github.com/radialpoint/bigdata-week-sentiment)
