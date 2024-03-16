import threading
import socket
import random
import time

url = 'localhost'

process_addresses = {
    'p1': (url, 5001),
    'p2': (url, 5002),
    'p3': (url, 5003),
    'p4': (url, 5004)
}

num_processes = len(process_addresses)

clocks = {process: [0] * num_processes for process in process_addresses}

print(clocks)


def send_message(sender, receiver, message):
    """
    Envia uma mensagem de um processo para outro
    """
    sender_addr = process_addresses[sender]
    receiver_addr = process_addresses[receiver]
    sender_clock = clocks[sender][:]  # Cópia do vetor de relógio do processo emissor

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as skt:
        skt.sendto(str((sender_clock, message)).encode(), receiver_addr)
        print(f"Processo {sender}: Enviando mensagem para {receiver}. Vetor enviado: {sender_clock}")


def receive_message(process):
    """
    Recebimento e processamento de mensagens
    """
    process_addr = process_addresses[process]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(process_addr)
        while True:
            data, addr = sock.recvfrom(1024)
            sender_clock, message = eval(data.decode())  # Decodificar os dados recebidos
            print(f"Processo {process}: Mensagem recebida de {addr}. Vetor recebido: {sender_clock}")

            # Atualizar o vetor de relógio local
            for i in range(num_processes):
                clocks[process][i] = max(clocks[process][i], sender_clock[i])
            clocks[process][int(process[-1]) - 1] += 1  # Incrementar o relógio local do processo
            print(f"Processo {process}: Vetor local atualizado: {clocks[process]}")


def random_message_exchange():
    """
    Troca aleatória de mensagens entre os processos
    """
    while True:
        sender = random.choice(list(process_addresses.keys()))
        receiver = random.choice(list(process_addresses.keys()))
        if sender != receiver:
            send_message(sender, receiver, "Mensagem Aleatória")
        time.sleep(random.uniform(1, 4))


threads = []
for process in process_addresses:
    t = threading.Thread(target=receive_message, args=(process,))
    t.start()
    threads.append(t)

t = threading.Thread(target=random_message_exchange)
t.start()

for thread in threads:
    thread.join()
