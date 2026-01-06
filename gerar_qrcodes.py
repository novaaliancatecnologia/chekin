import qrcode
import os

# --- Pasta para salvar os QR Codes ---
PASTA_QR = "qrcodes"
os.makedirs(PASTA_QR, exist_ok=True)

# --- Lista de pessoas (exemplo) ---
pessoas = [
    {"nome": "João Silva", "tipo": "Voluntário", "ministério": "Evangelismo"},
    {"nome": "Maria Souza", "tipo": "Visitante", "ministério": ""},
    {"nome": "Carlos Oliveira", "tipo": "Obreiro(a)", "ministério": "Louvor"},
    {"nome": "Ana Lima", "tipo": "Voluntário", "ministério": "Recepção"},
    {"nome": "Paulo Santos", "tipo": "Visitante", "ministério": ""}
]

# --- Gerar QR Codes ---
for pessoa in pessoas:
    dados_qr = f"{pessoa['nome']};{pessoa['tipo']};{pessoa['ministério']}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(dados_qr)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    nome_arquivo = f"{pessoa['nome'].replace(' ', '_')}_{pessoa['tipo']}.png"
    img.save(os.path.join(PASTA_QR, nome_arquivo))
    print(f"QR Code gerado: {nome_arquivo}")

print("Todos os QR Codes foram gerados na pasta 'qrcodes/'")
