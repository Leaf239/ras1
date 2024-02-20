import socket

# 서버 주소와 포트 설정
server_address = ('127.0.0.1', 5555)

# 소켓 생성
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # 서버에 연결
    client_socket.connect(server_address)
    print("서버에 연결됨.")

    while True:
        # 서버로부터 데이터 수신
        data = client_socket.recv(1024).decode('utf-8')

        # 수신된 데이터 출력 (실제로는 이 값을 활용하여 작업을 수행)
        print("수신된 데이터:", data)

except KeyboardInterrupt:
    print("사용자에 의해 종료됨.")

finally:
    # 소켓 닫기
    client_socket.close()
