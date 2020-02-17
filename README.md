# csgo-data: 

Data collection for professional matches of the game "Counter-Strike: Global Offensive". This repository is in charge of updating the data on a daily basis, and saving the results on a ''CSV'' file

---

## Dependencies

* NodeJS
* HLTV npm (npm install hltv)
* Python3

---

## Daily update via cron jobs

The continuous execution of the data collection program is done via a cron job.

To set the cron job for execution every day N minutes past M o'clock (assuming the repository is located in ''~/Desktop/csgo-data''):

> crotab -e

> N M * * * cd ~/Desktop/csgo-data; python3 master-scraper.py >> ~/Desktop/csgo-data/log/cron.log



---

## Possible problems

* Path of the commands for node (inside cron, you need to add the path of where NodeJS is installed
* Use absolute path for the files
* When saving a map, if the game isn't over, the information might be incomplete
* * To avoid this problem, we always re-write the independent map JSON files given that we only do the update of a couple of days

--- 
## Related repositories
* In 'emmanuel-garza/moneyball-csgo' is located the source code for the web app, whose url is: http://helmholtzanalytics.xyz/
* In 'emmanuel-garza/insight-csgo' is located the source code for modeling the outcome of a match.
