Monitor de Conectividade de Hosts

Este script monitora a conectividade de múltiplos hosts (endereços IP ou nomes de hosts) usando o comando `ping` e envia alertas por e-mail quando um host se torna inacessível. O programa registra logs de suas atividades e permite uma configuração personalizada dos parâmetros de verificação e alertas.

Funcionalidades

- Monitora a conectividade de múltiplos hosts simultaneamente.
- Envia alertas por e-mail quando um host está inacessível ou não responde dentro do tempo limite.
- Registra logs detalhados das atividades, incluindo sucessos, falhas e alertas enviados.
- Utiliza multithreading para realizar verificações simultâneas.

Pré-requisitos

- **Python 3.9 ou superior**
- **Bibliotecas Python:**

  - `subprocess` (nativo)
  - `platform` (nativo)
  - `time` (nativo)
  - `smtplib` (nativo)
  - `email.mime` (nativo)
  - `datetime` (nativo)
  - `pytz` (para gerenciamento de fusos horários)
  - `logging` (nativo)
  - `os` (nativo)
  - `threading` (nativo)

Instalação

1. Instale o Python 3.9+

- Baixe e instale o Python em: [python.org](https://www.python.org/)

2. Instale a biblioteca `pytz`

```bash
pip install pytz
```

Configuração

1. Configuração de Variáveis de Ambiente

Para garantir que o script funcione corretamente e envie alertas por e-mail, é necessário configurar a variável de ambiente `EMAIL_PASSWORD`, que armazena a senha do e-mail usado para enviar os alertas. Abaixo estão as instruções para configurar essa variável de ambiente em diferentes sistemas operacionais:

**No Windows:**

1. **Via Prompt de Comando:**
   - Abra o Prompt de Comando (cmd).
   - Digite o seguinte comando, substituindo `"sua_senha"` pela senha real do seu e-mail:
     ```bash
     setx EMAIL_PASSWORD "sua_senha"
     ```
   - Feche e reabra o terminal para que a variável seja aplicada.

2. **Via Painel de Controle:**
   - Vá para **Painel de Controle** > **Sistema e Segurança** > **Sistema** > **Configurações avançadas do sistema**.
   - Clique em **Variáveis de Ambiente**.
   - Em **Variáveis do Sistema**, clique em **Novo**.
   - Defina:
     - **Nome da variável**: `EMAIL_PASSWORD`
     - **Valor da variável**: `sua_senha`
   - Clique em **OK** para salvar.

**No Linux ou macOS:**

1. **Via Terminal:**
   - Abra o terminal.
   - Defina a variável de ambiente com o seguinte comando, substituindo `"sua_senha"` pela senha real:
     ```bash
     export EMAIL_PASSWORD="sua_senha"
     ```
   - Para que a variável fique definida permanentemente, adicione o comando acima ao final do arquivo `~/.bashrc` (ou `~/.zshrc` se usar Zsh) e execute `source ~/.bashrc` para aplicar.

2. **Configuração Permanente no Sistema:**
   - Edite o arquivo de configuração do shell (`~/.bashrc`, `~/.profile`, ou `~/.zshrc`) e adicione:
     ```bash
     export EMAIL_PASSWORD="sua_senha"
     ```
   - Salve o arquivo e execute `source ~/.bashrc` para aplicar as alterações.

**No Docker:**

1. **Passar ao Executar o Contêiner:**
   - Execute o contêiner com a opção `-e` para passar a variável:
     ```bash
     docker run -it -e EMAIL_PASSWORD="sua_senha" meu_projeto_docker
     ```

2. **Usar um Arquivo `.env`:**
   - Crie um arquivo `.env` com o seguinte conteúdo:
     ```
     EMAIL_PASSWORD=sua_senha
     ```
   - Rode o contêiner com o arquivo `.env`:
     ```bash
     docker run --env-file .env meu_projeto_docker
     ```

2. Configuração de E-mail

- **SMTP_SERVER**: Servidor SMTP usado para enviar e-mails (configurado para o Outlook por padrão).
- **SMTP_PORT**: Porta do servidor SMTP (587 por padrão).
- **FROM_EMAIL**: Endereço de e-mail usado para enviar os alertas.

3. Fuso Horário

O script usa o fuso horário `America/Sao_Paulo` por padrão. Você pode alterá-lo ajustando a linha:

```python
TIMEZONE = pytz.timezone('America/Sao_Paulo')
```

Uso

1. Execute o Script

```bash
python seu_script.py
```

2. Digite os Hosts

Insira os IPs ou nomes dos hosts que deseja monitorar, separados por vírgula.

3. Exemplo de Entrada

```bash
Digite os IPs ou nomes dos hosts para verificar a conectividade, separados por vírgula: 192.168.1.1, google.com, 8.8.8.8
```

Como Funciona

- **Verificação de Conectividade**: O script envia pings para os hosts especificados e verifica se eles estão acessíveis.
- **Envio de Alertas**: Se um host não responder, um e-mail de alerta é enviado para o endereço especificado. Um segundo alerta só será enviado após 15 minutos de inacessibilidade contínua.
- **Logging**: Logs detalhados são mantidos no arquivo `ping_monitor.log` e também exibidos no terminal.

Problemas Conhecidos

- Se `EMAIL_PASSWORD` não estiver definida, o script lançará um erro e interromperá a execução.
- Se muitos hosts forem monitorados simultaneamente, o uso de recursos pode aumentar significativamente.

Segurança

- Assegure-se de que a senha de e-mail está sendo tratada de forma segura, usando variáveis de ambiente e evitando deixá-la exposta no código.

Contribuição

Sinta-se à vontade para fazer contribuições para melhorar o código ou adicionar novas funcionalidades. Faça um fork do repositório, implemente suas mudanças e envie um pull request.
