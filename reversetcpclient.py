import socket
import struct
import random
import argparse
from datetime import datetime

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


def generate_chunks(data, lmin, lmax, seed):

    random.seed(seed)

    pos = 0

    chunks = []

    while pos < len(data):

        size = random.randint(lmin, lmax)

        if pos + size > len(data):
            size = len(data) - pos

        chunks.append(data[pos:pos + size])

        pos += size

    return chunks


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("serverIP")
    parser.add_argument("serverPort", type=int)

    parser.add_argument("file")

    parser.add_argument("Lmin", type=int)
    parser.add_argument("Lmax", type=int)

    parser.add_argument("seed", type=int)

    args = parser.parse_args()

    with open(args.file, "r", encoding="ascii") as f:
        content = f.read()

    chunks = generate_chunks(
        content,
        args.Lmin,
        args.Lmax,
        args.seed
    )

    N = len(chunks)

    print("Total Chunks =", N)

    client = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    client.connect(
        (args.serverIP, args.serverPort)
    )

    # ========= Initialization =========
    init_packet = struct.pack(
        "!HI",
        1,
        N
    )

    client.sendall(init_packet)

    write_log(f"SEND Initialization N={N}")

    # ========= Agree =========
    agree = recv_all(client, 2)

    msg_type = struct.unpack("!H", agree)[0]

    if msg_type != 2:
        print("agree failed")
        return

    write_log("RECV Agree")

    result_blocks = []

    for idx, block in enumerate(chunks):

        data = block.encode()

        packet = struct.pack(
            "!HI",
            3,
            len(data)
        ) + data

        client.sendall(packet)

        write_log(
            f"SEND ReverseRequest block={idx+1} len={len(data)}")

        header = recv_all(client, 6)

        msg_type, length = struct.unpack(
            "!HI",
            header
        )

        reverse_data = recv_all(
            client,
            length
        ).decode()

        write_log(
            f"RECV ReverseAnswer block={idx+1} len={length}")

        print(
            f"{idx+1}: {reverse_data}"
        )

        result_blocks.append(reverse_data)

    client.close()

    final_text = ''.join(result_blocks[::-1])

    with open(
        "output.txt",
        "w",
        encoding="ascii"
    ) as f:
        f.write(final_text)

    print("\nSaved to output.txt")


if __name__ == "__main__":
    main()