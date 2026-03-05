import cv2
from pyzbar.pyzbar import decode
from datetime import datetime
import csv
import os

# Lista de coleta
coletas = {}

# Caminho do arquivo TXT
ARQUIVO_TXT = "coletas.txt"

def salvar_txt():
    with open(ARQUIVO_TXT, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter="\t")
        for codigo, qtd in coletas.items():
            writer.writerow([codigo, qtd])

def processar_codigo(codigo):
    if codigo in coletas:
        resposta = input(f"Código {codigo} já existe. Somar quantidade? (s/n): ")
        if resposta.lower() == "s":
            coletas[codigo] += 1
        else:
            qtd = int(input("Digite quantidade: "))
            coletas[codigo] = qtd
    else:
        qtd = int(input(f"Digite quantidade para {codigo}: "))
        coletas[codigo] = qtd

# Inicializa a câmera
cap = cv2.VideoCapture(0)

print("Pressione ESC para sair.")
while True:
    ret, frame = cap.read()
    for obj in decode(frame):
        codigo = obj.data.decode("utf-8")
        print(f"Detectado: {codigo}")
        processar_codigo(codigo)
    cv2.imshow("Coletor Centro", frame)
    if cv2.waitKey(1) == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()

# Salva a coleta
salvar_txt()
print("Coletas salvas em", ARQUIVO_TXT)