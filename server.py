from wsgiref.simple_server import make_server
import json

tasks = {}

next_id = 4


def application(environ, start_response):

    global next_id

    method = environ["REQUEST_METHOD"]
    path = environ["PATH_INFO"]

    print(method, path)

    parts = path.strip("/").split("/")

    if method == "GET":

        if path == "/tasks":

            value = json.dumps(tasks)

            start_response(
                "200 OK",
                [("Content-Type", "application/json")]
            )

            return [value.encode("utf-8")]

        if len(parts) == 2 and parts[0] == "tasks":

            task_id = int(parts[1])
            value = tasks.get(task_id)

            if value != None:

                start_response(
                    "200 OK",
                    [("Content-Type", "application/json")]
                )

                return [json.dumps(value).encode("utf-8")]

            start_response(
                "404 Not Found",
                [("Content-Type", "application/json")]
            )

            return [json.dumps(
                {"error": "Tarea no encontrada"}
            ).encode("utf-8")]

    elif method == "POST":

        if path == "/tasks":

            length = int(environ.get("CONTENT_LENGTH", 0))
            body = environ["wsgi.input"].read(length)

            data = json.loads(body.decode("utf-8"))

            data["id"] = next_id
            tasks[next_id] = data

            value = json.dumps(data)

            next_id += 1

            start_response(
                "201 Created",
                [("Content-Type", "application/json")]
            )

            return [value.encode("utf-8")]

    elif method == "PATCH":

        if len(parts) == 2 and parts[0] == "tasks":

            task_id = int(parts[1])

            if task_id in tasks:

                length = int(environ.get("CONTENT_LENGTH", 0))
                body = environ["wsgi.input"].read(length)

                data = json.loads(body.decode("utf-8"))

                tasks[task_id].update(data)

                start_response(
                    "200 OK",
                    [("Content-Type", "application/json")]
                )

                return [json.dumps(
                    tasks[task_id]
                ).encode("utf-8")]

            start_response(
                "404 Not Found",
                [("Content-Type", "application/json")]
            )

            return [json.dumps(
                {"error": "Tarea no encontrada"}
            ).encode("utf-8")]

    elif method == "DELETE":

        if len(parts) == 2 and parts[0] == "tasks":

            task_id = int(parts[1])

            if task_id in tasks:

                del tasks[task_id]

                start_response(
                    "200 OK",
                    [("Content-Type", "application/json")]
                )

                return [json.dumps(
                    {"message": "Tarea eliminada"}
                ).encode("utf-8")]

            start_response(
                "404 Not Found",
                [("Content-Type", "application/json")]
            )

            return [json.dumps(
                {"error": "Tarea no encontrada"}
            ).encode("utf-8")]

    start_response(
        "404 Not Found",
        [("Content-Type", "application/json")]
    )

    return [json.dumps(
        {"error": "Ruta no encontrada"}
    ).encode("utf-8")]


with make_server("", 9292, application) as httpd:
    print("se ejecuta en http://localhost:9292")
    httpd.serve_forever()
