import asyncio
from aiohttp import web
from utils import process_image, send_to_scale_server

async def handle(request):
    reader = await request.multipart()
    field = await reader.next()
    if field.name == 'file':
        filename = field.filename
        content = await field.read()

        # Convertimos la imagen a escala de grises
        grayscale_image = await process_image(content)

        # Enviar la imagen al servidor de escalado
        scale_factor = 2  # Ejemplo de factor de escala
        scaled_image = await send_to_scale_server(grayscale_image, scale_factor)

        if scaled_image:
            return web.Response(body=scaled_image, content_type='image/jpeg')
        else:
            return web.Response(text="Error al escalar la imagen.", status=500)
    return web.Response(text="Error: No se recibió un archivo de imagen.", status=400)

async def init_app():
    app = web.Application()
    app.router.add_post('/process', handle)
    return app

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Servidor asíncrono de procesamiento de imágenes.")
    parser.add_argument("-i", "--ip", type=str, required=True, help="Dirección IP de escucha")
    parser.add_argument("-p", "--port", type=int, required=True, help="Puerto de escucha")
    args = parser.parse_args()

    app = asyncio.run(init_app())
    web.run_app(app, host=args.ip, port=args.port)

if __name__ == "__main__":
    main()