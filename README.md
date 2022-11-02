# Finance-Control-Bot
TG bot for monitoring your expenses and income

## Quick Start
- `$ mkdir db` 
- `$ touch db/finance.db`
- `$ cp bot.ini.example bot.ini`
- `$ sudo chmod a+rw db db/*`
- add your token to 'bot.ini'
- build a docker image, using `docker build -t finance_conrol .`  
- run a docker container, using compose `docker-compose up -d`