import socketserver
from multiprocessing import Process
from PIL import Image
import io

class ScaleHandler(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            print("Conexión recibida.")
            
            # Vemos que tan grande son los datos que vamos a recibir
            data_size_bytes = self.request.recv(4)
            if not data_size_bytes:
                print("Error: No se recibió el tamaño de los datos.")
                return

            data_size = int.from_bytes(data_size_bytes, byteorder='big')
            print(f"Tamaño de la imagen recibido: {data_size} bytes")

            # Si el tamaño es negativo o 0, no podemos hacer nada
            if data_size <= 0:
                print("Error: Tamaño de los datos inválido.")
                return

            # Recibimos los datos
            data = b""
            while len(data) < data_size:
                packet = self.request.recv(data_size - len(data))
                if not packet:
                    print("Error: Conexión cerrada antes de recibir todos los datos de la imagen.")
                    return
                data += packet

            
            image = Image.open(io.BytesIO(data)) # asi podemos procesar la imagen con 
            print("Imagen recibida y procesada correctamente.")

            # Le damos la escalada a la imagen
            scale_factor_bytes = self.request.recv(4)
            scale_factor = int.from_bytes(scale_factor_bytes, byteorder='big')
            width, height = image.size
            new_size = (width // scale_factor, height // scale_factor)
            scaled_image = image.resize(new_size)

            # convertimos la imagen en la escalada que le dimos y la enviamos al cliente
            output = io.BytesIO()
            scaled_image.save(output, format='JPEG')
            scaled_image_data = output.getvalue()
            output.close()

            scaled_image_size = len(scaled_image_data)
            self.request.sendall(scaled_image_size.to_bytes(4, byteorder='big'))
            self.request.sendall(scaled_image_data)

        except Exception as e:
            print(f"Error en ScaleHandler: {e}")

def start_scale_server(host, port):
    with socketserver.TCPServer((host, port), ScaleHandler) as server:
        print(f"Servidor de escalado escuchando en {host}:{port}")
        server.serve_forever()

if __name__ == "__main__":
    import argparse

    #estos argumentos son para poder correr el servidor (son lineas de comandos y descripciones)
    parser = argparse.ArgumentParser(description="Servidor de escalado de imágenes.")
    parser.add_argument("-i", "--ip", type=str, required=True, help="Dirección IP de escucha")
    parser.add_argument("-p", "--port", type=int, required=True, help="Puerto de escucha")
    args = parser.parse_args()

    process = Process(target=start_scale_server, args=(args.ip, args.port)) #creamos y ejecutamos el proceso para el escalado
    
    process.start()
    process.join()
