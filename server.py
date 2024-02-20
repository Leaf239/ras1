import socket
import time

# 소켓 생성
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버 주소와 포트 설정
server_address = ('127.0.0.1', 5555)
server_socket.bind(server_address)

# 클라이언트의 연결 대기
server_socket.listen(1)
print("connecting to server...")

# 클라이언트와 연결
client_socket, client_address = server_socket.accept()
print("client connected:", client_address)

# 특정 변수 초기화
detection = 0 #여기에 감지 결과 넣기

try:
    while True:
        # 특정 변수 값을 전송
        data = str(detection)
        client_socket.sendall(data.encode('utf-8'))

        # 1초 대기
        time.sleep(1)



except KeyboardInterrupt:
    print("사용자에 의해 종료됨.ㄹ ")

finally:
    # 소켓 닫기
    client_socket.close()
    server_socket.close()
