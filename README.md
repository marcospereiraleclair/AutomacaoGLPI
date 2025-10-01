# Automação de Chamados GLPI

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Playwright](https://img.shields.io/badge/Playwright-1.41-purple?logo=playwright&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-Automation-orange)
![Status](https://img.shields.io/badge/Status-Ativo-brightgreen)


# Summary
Automação de abertura de chamados no GLPI para agilizar processos da equipe de TI e Infraestrutura.

## Description
Este projeto automatiza a criação de chamados no GLPI usando Python e Playwright. Ele permite integração com Google Sheets, gera logs de status de cada chamado e simplifica o acompanhamento das solicitações. Ideal para equipes de Facilites e Manutenção que precisam aumentar a eficiência. Assim abrindo o chamado para o pessoal da manutençao atraves do Qrcode que esta com o link do formulario. 

## Autores/Equipe

| Nome           | Função                   | GitHub |
|----------------|-------------------------|--------|
| ![Marcos](https://img.icons8.com/color/48/000000/user.png) Marcos Pereira | Analista de TI JR     | [@marcospereira](https://github.com/marcospereiraleclair) |
| ![Rafael](https://img.icons8.com/color/48/000000/user.png) Rafael Ramos | Analista de Infraestrutura  JR   | [@rafaelramos](https://github.com/Rafaelgomes976) |
| ![Cezar](https://img.icons8.com/color/48/000000/user.png) Cezar Mussoi | Assistente de Desenvolvimento de Sistemas  | [@cezarmussoi](https://github.com/cezarmussoilec) |


## 1. Identificação do Software
- **Nome do Sistema:** Automação de Chamados GLPI  
- **Área:** Tecnologia da Informação – Infraestrutura e Desenvolvimento  
- **Versão:** 1.0  
- **Data de Criação:** 2025  
- **Empresa:** Leclair Industria e Comercio de Perfumes e Cosmeticos Ltda

## 2. Objetivo
O software foi desenvolvido para automatizar a abertura de chamados no sistema GLPI, utilizando informações armazenadas em planilhas do Google Sheets.  
O sistema visa reduzir o tempo de atendimento e melhorar a rastreabilidade dos chamados relacionados à manutenção predial.

## 3. Escopo
- Automatização da captura de dados de planilhas do Google Sheets.  
- Abertura automática de chamados no GLPI, preenchendo os campos necessários.  
- Registro de status do chamado na própria planilha.  
- Suporte a execução contínua, verificando periodicamente se há novos registros.

## 4. Descrição Técnica

### 4.1 Tecnologias Utilizadas
- **Linguagem:** Python 3.x  
- **Automação de Navegador:** Playwright  
- **Integração com Google Sheets:** gspread + oauth2client  
- **Armazenamento temporário de perfil de navegador:** Diretório local (`user_data_dir`)  

### 4.2 Estrutura do Código
1. **Configuração do Google Sheets**
   - Arquivo de credenciais JSON (tratar como criptografado/confidencial).  
   - Nome da planilha e coluna de controle (`Chamado Aberto`).  
   - Escopo da API do Google Drive e Sheets.
   - (https://prnt.sc/8YDJfXpqstGR)
   - (https://prnt.sc/DNp-ZpXwO_zA)

2. **Autenticação**
   - Login no GLPI utilizando credenciais (não incluídas nesta documentação).  
   - Seleção do caminho do navegador Chrome entre possíveis localizações.
   - (https://prnt.sc/apIDYkZ8s5ne)

3. **Automação do Navegador**
   - Inicialização do navegador Chromium com Playwright em modo headless.  
   - Preenchimento de formulário no GLPI com dados do Google Sheets.  
   - Registro de erros com captura de tela e HTML da página.
   - (https://prnt.sc/95mzQLGqhDWC)

### 4.3 Loop Contínuo
- Iteração sobre todas as linhas da planilha.  
- Verificação de registros pendentes.  
- Marcação de chamados abertos para evitar duplicidade.  
- Intervalo de 3 minutos entre verificações consecutivas.

### 4.4 Fluxo de Operação
1. Inicialização do script Python.  
2. Conexão com Google Sheets usando credenciais criptografadas.  
3. Verificação do Chrome instalado e inicialização do navegador.  
4. Login no GLPI.  
5. Loop contínuo:  
   - Leitura das linhas da planilha.  
   - Para cada registro pendente:  
     - Preenchimento automático do formulário GLPI.  
     - Envio do chamado.  
     - Atualização da coluna de controle na planilha.  
   - Pausa de 3 minutos antes da próxima verificação.

### 4.5 Considerações de Segurança
- **Credenciais:** Usuário e senha do GLPI não estão presentes no código distribuído. Devem ser armazenadas de forma segura (ex.: variáveis de ambiente).  
- **Arquivo JSON do Google Sheets:** Deve ser tratado como criptografado e seguro, nunca exposto em repositórios públicos.  
- **Logs de erros:** Contêm dados do formulário preenchido, portanto devem ser armazenados em ambiente seguro.

### 4.6 Configurações Relevantes

| Configuração       | Descrição                                                      |
|--------------------|----------------------------------------------------------------|
| SHEET_JSON         | Caminho para credenciais JSON do Google Sheets (criptografado) |
| SHEET_NAME         | Nome da planilha no Google Sheets                              |
| COLUNA_CHAMADO     | Nome da coluna que indica se o chamado foi aberto              |
| CHROME_PATHS       | Possíveis caminhos do executável do Chrome                     |
| headless           | Define se o navegador será executado em segundo plano          |
| Intervalo de verificação | 180 segundos (3 minutos)                                 |

### 4.7 Bibliotecas Python
- **os** – manipulação de caminhos e arquivos  
- **time** – controle de pausas e temporização  
- **gspread** – integração com Google Sheets  
- **oauth2client.service_account** – autenticação via conta de serviço Google  
- **playwright.sync_api** – automação de navegador Chromium  

## 5. Execução
1. Garantir que o Python 3.x esteja instalado.  
2. Instalar dependências:  
   ```bash
   pip install gspread oauth2client playwright
   playwright install
