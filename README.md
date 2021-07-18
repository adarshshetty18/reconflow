# RECONFLOW
Reconflow is all in one tool for gathering reconnaissance information about a target without the hassle of installing multiple tools and their dependencies & also presents you the results to your telegram chat.

### Tools used
1. [Subfinder](https://github.com/projectdiscovery/subfinder) for subdomain enumeration.
2. [Httpx](https://github.com/projectdiscovery/httpx) for finding livedomains.
3. [Naabu](https://github.com/projectdiscovery/naabu) for scanning ports.
4. [FFUF](https://github.com/ffuf/ffuf) for bruteforcing directories.

### Docker Repository
https://hub.docker.com/r/adarshshetty/reconflow

### Pre-requisites
- [Docker Engine](https://docs.docker.com/engine/install/)
- [docker-compose](https://docs.docker.com/compose/install/)

### How to install
1. Create a [telegram bot](https://core.telegram.org/bots#3-how-do-i-create-a-bot) & copy the bot token.
1. Download the docker-compose file
   ```
   wget https://raw.githubusercontent.com/adarshshetty18/reconflow/main/docker-compose.yaml
   ```
   
2. Open the downloaded docker-compose file & add the telegram bot token from step 1 where required.
   
3. Use the following command to deploy the system
   ```
   docker-compose up -d
   ```
4. Head over to the bot that you created in step 1 & send the follwing command.
   ```
   /start
   ```
