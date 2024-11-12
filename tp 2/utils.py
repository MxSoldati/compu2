import asyncio
import socket
from PIL import Image
import io

async def process_image(image_data):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _convert_to_grayscale, image_data)

def _convert_to_grayscale(image_data): #funcion para convertir la imagen en escala de grises
    image = Image.open(io.BytesIO(image_data)).convert("L")
    output = io.BytesIO()
    image.save(output, format="JPEG")
    return output.getvalue()

async def send_to_scale_server(image_data, scale_factor): #aca mandamos la imagen al servidor de escalado, asi podemos procesarla y hacer lo que queramos
    try:
        reader, writer = await asyncio.open_connection('localhost', 9999)

        data_size = len(image_data)
        writer.write(data_size.to_bytes(4, byteorder='big'))
        writer.write(image_data)
        writer.write(scale_factor.to_bytes(4, byteorder='big'))
        await writer.drain()

        # Leer la imagen escalada del servidor de escalado
        scaled_image_size_bytes = await reader.read(4)
        scaled_image_size = int.from_bytes(scaled_image_size_bytes, byteorder='big')
        scaled_image_data = await reader.read(scaled_image_size)

        writer.close()
        await writer.wait_closed()

        return scaled_image_data
    except Exception as e:
        print(f"Error al comunicarse con el servidor de escalado: {e}")
        return None