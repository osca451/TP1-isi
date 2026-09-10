# TP1-isi

Servidor HTTP

Este servidor permite trabajar con tareas usando los verbos HTTP GET, POST, PATCH y DELETE.

GET: sirve para obtener las tareas. Se puede obtener la lista completa o una tarea específica.

POST: sirve para crear una tarea nueva. Cada tarea creada recibe un ID.

PATCH: sirve para modificar una tarea. Se pueden cambiar solamente algunos de sus datos sin modificar los demás.

DELETE: sirve para eliminar una tarea.

Porque POST no es idempotente
POST no es idempotente porque si hacemos la misma petición varias veces, se crean varias tareas.
PE: si mandamos dos veces el mismo POST, no se modifica la misma tarea, sino que se crean dos tareas diferentes con distintos ids.

Para ejecutar el servidor:
uv run python server.py

El servidor queda disponible en "http://localhost:9292".
