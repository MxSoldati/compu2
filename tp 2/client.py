import aiohttp
import asyncio
import sys

async def send_image(ip, port, image_path):
    # Construimo la URL del servidor asíncrono
    url = f'http://{ip}:{port}/process'
    async with aiohttp.ClientSession() as session: # Crear una sesión HTTP asíncrona
        #se lee la imagen desde el archivo
        with open(image_path, 'rb') as f:
            image_data = f.read()
        
        #le creamos un formulario de datos para enviar la imagen
        data = aiohttp.FormData()
        data.add_field('file', image_data, filename='image.jpg', content_type='image/jpeg')
        
        async with session.post(url, data=data) as response:
            # vemos que tan exitosa fue lo que mandamos
            if response.status == 200: # si es buena la procesamos , sino un error al procesarla y avisamos sobre el error
                print("Imagen enviada al servidor y procesada correctamente.")
                processed_image = await response.read()
                with open('processed_image.jpg', 'wb') as f:
                    f.write(processed_image)
                print("Imagen procesada guardada como 'processed_image.jpg'.")
            else:
                print(f"Error al procesar la imagen: {response.status}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python client.py <IP> <PORT> <IMAGE_PATH>")
        sys.exit(1)

    # Aca tenemos los argumentos que se pasan por consola
    ip = sys.argv[1]
    port = int(sys.argv[2])
    image_path = sys.argv[3]

    # Corremos el cliente
    asyncio.run(send_image(ip, port, image_path))