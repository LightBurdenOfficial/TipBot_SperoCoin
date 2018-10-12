# Telegram SperoCoin Tipbot -

#### Forked from Telegram Reddcoin Tipbot.
####  https://github.com/samgos/reddbot-telegram
####  https://github.com/flokisatoshi/IdealCash-Telegram-Tipbot

## Dependencies

*  `apt-get install python3`
*  `apt-get install python3-pip`
*  `pip3 install beautifulsoup4`
*  `pip3 install python-telegram-bot --upgrade`

* In order to run the tip-bot effectively, a Bitcoin-core based client is needed. For this SperoCoind is used

## Setup

* Install the deps
* Install SperoCoind to /usr/bin/SperoCoind
* Run and exit program
### NOTE if not using SperoCoind compiled from the experimental branch of the github, you will have to provide the SperoCoin.conf file and place it manually in the ~/.SperoCoin/ directory.
* edit the SperoCoin.conf file located at ~/.SperoCoin/SperoCoin.conf to contain the following:

* `staking=0`
* `enableaccounts=1`
### Staking cannot be enabled while running for the tipbot.

* Run SperoCoind and let it start syncing


* Setup a bot with the user @BotFather through PM on Telegram, after going through a setup you will be given a bot token. Edit the command.py file and replace the parameter 'BOT_TOKEN_HERE' with the one you just recieved.

*  Run the script
`python3 command.py`

*  Initiate the bot by inviting it to a chat or via PM, some commands are `/funds` , `/price` , `/commands` and to find out the format related to tip others and withdrawal of funds use `/help`.

### Setting up the bot as so still leaves the wallet unencrypted, so please go to extra measures to provide extra security. Make sure to have SSH encryption on whatever device/droplet you run it on.

*  Please fork the code, happy tipping!

### Português

## Instalação das Dependências

*  `apt-get install python3`
*  `apt-get install python3-pip`
*  `pip3 install beautifulsoup4`
*  `pip3 install python-telegram-bot --upgrade`

* Para executar o tip-bot efetivamente, é necessário um cliente baseado no Bitcoin-core. Para isso será utilizado a wallet SperoCoind

## Configuração

* Instale as dependências
* Intale a wallet SperoCoind em /usr/bin/SperoCoind
* Execute o programa e saia
### OBSERVAÇÃO: Se não estiver usando o SperoCoind compilado da ramificação experimental do github, você terá que fornecer o arquivo SperoCoin.conf e colocá-lo manualmente no diretório ~/.SperoCoin/.
* Edite o arquivo SperoCoin.conf localizado em ~/.SperoCoin/SperoCoin.conf e adicione o seguinte:
* `staking=0`
* `enableaccounts=1`
### Staking não pode estar ativado durante a execução do tipbot.

* Execute novamente a wallet SperoCoind e inicie a sincronização


* Configure um bot com o usuário @BotFather através de PM no Telegram, depois de configurar, você receberá um token de bot. Edite o arquivo command.py e substitua o parâmetro 'BOT_TOKEN_HERE' pelo que você acabou de receber.

*  Execute o script
`python3 command.py`

*  Inicie o bot convidando-o para um chat ou via PM, alguns comandos são `/funds`,`/price`, `/commands` e para descobrir outros comandos e configurações como a retirada de fundos use`/help`.

### Configure a carteira para deixá-la descriptografada, então, por favor, execute medidas extras de segurança. Certifique-se de ter encriptação SSH em qualquer dispositivo/droplet que você irá executar.

*  Por favor fork nosso código e dê gorjetas!
