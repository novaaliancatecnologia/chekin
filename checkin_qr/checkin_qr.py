import cv2
import requests
import sys
from pyzbar import pyzbar

# --- Configurações ---
URL_CHECKIN = "http://127.0.0.1:5000/"  # URL do seu Flask (troque se for online)
TIPO_PADRAO = "Visitante"

def ler_qrcode():
    cap = cv2.VideoCapture(0)
    print("Aponte o QR Code para a câmera...")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erro ao acessar a câmera")
            break

        qrcodes = pyzbar.decode(frame)
        for qr in qrcodes:
            dados = qr.data.decode('utf-8')
            print(f"QR Code lido: {dados}")
            cap.release()
            cv2.destroyAllWindows()
            return dados

        cv2.imshow("Leitura QR Code", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    sys.exit()

def enviar_checkin(nome, tipo=TIPO_PADRAO, ministério=""):
    payload = {
        "nome": nome,
        "tipo": tipo,
        "ministério": ministério
    }
    try:
        resposta = requests.post(URL_CHECKIN, data=payload)
        if resposta.status_code == 200 or resposta.status_code == 302:
            print(f"Check-in realizado com sucesso para {nome} ({tipo})")
        else:
            print(f"Erro ao enviar check-in: {resposta.status_code}")
    except Exception as e:
        print(f"Erro de conexão: {e}")

if __name__ == "__main__":
    dados_qr = ler_qrcode()

    # Exemplo: o QR pode conter "nome;tipo;ministério"
    partes = dados_qr.split(";")
    nome = partes[0]
    tipo = partes[1] if len(partes) > 1 else TIPO_PADRAO
    ministério = partes[2] if len(partes) > 2 else ""

    enviar_checkin(nome, tipo, ministério)
