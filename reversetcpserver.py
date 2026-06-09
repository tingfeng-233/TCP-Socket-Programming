import socket
import struct
import threading
from datetime import datetime

HOST = "0.0.0.0"
PORT = 8888

LOG_FILE = "run_log.txt"


def write_log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        t = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        f.write(f"[{t}] {msg}\n")


def recv_all(sock, length):
    data = b''

    while len(data) < length:
        packet = sock.recv(length - len(data))

        if not packet:
            return None

        data += packet

    return data


def handle_client(conn, addr):
    print("Client connected:", addr)

    try:

        # ========= Initialization =========
        header = recv_all(conn, 6)

        if not header:
            return

        msg_type, N = struct.unpack("!HI", header)

        write_log(
            f"RECV Initialization from {addr}, Type={msg_type}, N={N}")

        print(f"N = {N}")

        # ========= Agree =========
        agree_packet = struct.pack("!H", 2)

        conn.sendall(agree_packet)

        write_log(f"SEND Agree to {addr}")

        # ========= Reverse =========
        for i in range(N):

            header = recv_all(conn, 6)

            if not header:
                break

            msg_type, length = struct.unpack("!HI", header)

            data = recv_all(conn, length)

            text = data.decode("ascii")

            write_log(
                f"RECV ReverseRequest block={i+1}, len={length}")

            reversed_text = text[::-1]

            response = struct.pack(
                "!HI",
                4,
                len(reversed_text.encode())
            ) + reversed_text.encode()

            conn.sendall(response)

            write_log(
                f"SEND ReverseAnswer block={i+1}, len={len(reversed_text)}")

    except Exception as e:
        print(e)

    finally:
        conn.close()
        print("Disconnected:", addr)


def main():

    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server.bind((HOST, PORT))

    server.listen(10)

    print(f"Server Listening {PORT}")

    while True:
        conn, addr = server.accept()

        threading.Thread(
            target=handle_client,
            args=(conn, addr),
            daemon=True
        ).start()


if __name__ == "__main__":
    main()