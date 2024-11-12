# TP2 - Procesamiento de Imágenes
#### Maximo Soldati Lopez
----
## 📝 Descripción

Este proyecto implementa un servidor de procesamiento de imágenes que se comunica con un segundo servidor para escalar imágenes. El primer servidor utiliza `asyncio` para manejar conexiones asíncronas, mientras que el segundo servidor utiliza `multiprocessing` y `socketserver` para manejar solicitudes de escalado de imágenes.

## 📋 Requisitos

- Python 3.8+
- Pillow
- aiohttp

## 👣 Primeros Pasos
```bash
pip install -r requirements.txt
```

## 🛠️ Uso

### Servidor HTTP Asíncrono
- `python async_server.py -i <IP> -p <PORT>`

### Servidor de Escalado
- `python scale_server.py -i <IP> -p 9999`
---

### Ejemplo para poder escalar la aplicacion:

#### Paso 1: Ejecutar el servidor asíncrono
En una terminal, ejecuta el servidor asíncrono:
`python async_server.py -i 127.0.0.1 -p 8888`

####  Paso 2: Ejecutar el servidor de escalado
En *otra terminal*, ejecuta el servidor de escalado:
`python scale_server.py -i 127.0.0.1 -p 9999`

#### Paso 3: Enviar la imagen desde el cliente
En una *tercera terminal*, ejecuta el cliente para enviar la imagen al servidor asíncrono:
`python client.py 127.0.0.1 8888 "/path/to/your/image.jpg"`

---
## Referencias
- AsyncIO Documentation
- Multiprocessing Documentation
- SocketServer Documentation

`requirements.txt` contiene las dependencias del projecto.

## Conclusion 
Con esta estructura y código, se cumple con los requisitos del trabajo práctico, incluyendo el procesamiento de imágenes en escala de grises, la comunicación entre servidores y la interacción del cliente solo con el primer servidor. Asegúrate de probar y ajustar el código según sea necesario para tu entorno específico.