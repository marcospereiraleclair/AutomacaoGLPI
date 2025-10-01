import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os

# ---------- CONFIGURAÇÃO GOOGLE SHEETS ----------
SHEET_JSON = os.getenv("SHEET_JSON")
SHEET_NAME = "Chamados para Facilites"
COLUNA_CHAMADO = "Chamado Aberto"

# Escopo da API
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name(SHEET_JSON, scope)
client = gspread.authorize(creds)
sheet = client.open(SHEET_NAME).sheet1

# ---------- CONFIGURAÇÃO PLAYWRIGHT ----------
load_dotenv("key.env")  # carrega o key.env
# load_dotenv()  # usaria se o nome fosse .env

GLPI_URL = os.getenv("GLPI_URL")
USUARIO = os.getenv("GLPI_USER")
SENHA = os.getenv("GLPI_PASS")
SHEET_JSON = os.getenv("SHEET_JSON")
GLPI_FORM_URL = os.getenv("GLPI_FORM_URL")


# Possíveis caminhos do Chrome
CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
]

# Verifica qual Chrome existe
CHROME_PATH = None
for path in CHROME_PATHS:
    if os.path.exists(path):
        CHROME_PATH = path
        break

if not CHROME_PATH:
    raise FileNotFoundError("Google Chrome não encontrado em Program Files nem Program Files (x86)")

with sync_playwright() as pw:
    navegador = pw.chromium.launch_persistent_context(
        user_data_dir="userdata",     # cria uma pasta local para perfil temporário
        headless=False,               # se quiser rodar escondido, troque para True
        executable_path=CHROME_PATH,
        args = ["--disable-gpu", "--disable-dev-shm-usage", "--disable-software-rasterizer"]
    )

    page = navegador.new_page()
    page.goto(GLPI_URL)

    # -------- LOGIN --------
    page.get_by_role("textbox", name="Usuário").fill(USUARIO)
    page.get_by_role("textbox", name="Senha Esqueceu sua senha?").fill(SENHA)
    page.get_by_role("textbox", name="Senha Esqueceu sua senha?").press("Enter")

    # Esperar menu carregar
    page.wait_for_selector('role=link[name="Manutenção Predial"]', timeout=10000)
    page.get_by_role("link", name="Manutenção Predial").click()
    time.sleep(5)

    # ---------- LOOP CONTÍNUO ----------
    while True:
        todas_linhas = sheet.get_all_values()
        cabecalhos = todas_linhas[0]

        # Criar coluna "Chamado Aberto" se não existir
        if COLUNA_CHAMADO not in cabecalhos:
            sheet.update_cell(1, len(cabecalhos)+1, COLUNA_CHAMADO)
            cabecalhos.append(COLUNA_CHAMADO)

        coluna_chamado_idx = cabecalhos.index(COLUNA_CHAMADO)
        algum_pendente = False

        # Loop sobre cada linha
        for idx, linha in enumerate(todas_linhas[1:]):
            linha_planilha = idx + 2
            while len(linha) < len(cabecalhos):
                linha.append("")

            nome = linha[cabecalhos.index('Nome e sobrenome.')]
            # Verifica se já abriu chamado
            if linha[coluna_chamado_idx].strip() == 'Sim':
                continue  # já processado

            algum_pendente = True

            try:
                print(f"Abrindo chamado para {nome}")

                # Atualizar página antes de abrir novo chamado
                page.goto(GLPI_FORM_URL)
                page.wait_for_timeout(10)  # espera 10s para carregar

                # Preencher campos
                page.locator("[id^='formcreator_field_561']").fill(linha[cabecalhos.index('Departamento/Setor')])
                page.locator("[id^='formcreator_field_562']").fill(nome)
                page.locator("[id^='formcreator_field_563']").fill(linha[cabecalhos.index('Ramal / Telefone de Contato')])
                page.locator("[id^='formcreator_field_564']").fill(linha[cabecalhos.index('Email / Teams')])
                page.locator("[id^='formcreator_field_597']").fill(linha[cabecalhos.index('Qual o problema?')])
                page.locator("[id^='formcreator_field_598']").fill(linha[cabecalhos.index('Foto do problema')])
                page.get_by_role("button", name="Enviar").click()

                # Espera URL mudar para confirmar criação
                url_atual = page.url
                page.wait_for_url(lambda url: url != url_atual, timeout=15000)

                # Atualizar planilha
                sheet.update_cell(linha_planilha, coluna_chamado_idx + 1, 'Sim')
                print(f" Chamado registrado para {nome}")

            except Exception as e:
                print(f" Erro ao abrir chamado para {nome}: {e}")
                page.screenshot(path=f"erro_chamado_{idx + 1}.png")
                with open(f"erro_chamado_{idx + 1}.html", "w", encoding="utf-8") as f:
                    f.write(page.content())

        if not algum_pendente:
            print(" Nenhum chamado pendente.")
            with open("status.txt", "w", encoding="utf-8") as f:
                f.write("Nenhum chamado pendente")
        else:
            # grava status
            with open("status.txt", "w", encoding="utf-8") as f:
                f.write("Chamado pendente")

        print("Aguardando 3 minutos antes de verificar novamente...")
        time.sleep(180)  # 180 espera 3 minutos, 120 2min, 600 10min, 1800 30min, 3600 60min
