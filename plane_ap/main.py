import usocket as socket


html = """<!DOCTYPE html>
<html>
    <head> <title>ESP8266 Server</title> </head>
    <body>
    <h1>Welcome to ESP8266 Server</h1>
    </body>
</html>
"""


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 80))
s.listen(5)


while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    conn_file = conn.makefile('rwb', 0)
    while True:
        line = conn_file.readline()
        if not line or line == b'\r\n':
            break
    response = html
    conn_file.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    conn_file.send(response)
    conn_file.close()
