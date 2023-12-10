import os

from fastapi import FastAPI

api = FastAPI()

"""
TODO_TABLE = os.getenv("TODO_TABLE")
todo_service: TodoService = TodoService(todo_table=TODO_TABLE)
"""


"""
@api.middleware("http")
async def log_requests(request: Request, call_next):
    idem = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = "{0:.2f}".format(process_time)
    logger.info(
        f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}"
    )

    return response
"""


@api.get("/ping")
def ping():
    return f"{os.getenv('HOSTNAME')}: pong"


"""

@api.post("/", status_code=status.HTTP_200_OK)
def create(src: Todo) -> Todo:
    return todo_service.save(src)


@api.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def update(todo_id: str, src: Todo):
    return todo_service.update(todo_id, src)


@api.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(todo_id: str):
    todo_service.delete(todo_id)


@api.get("/", status_code=status.HTTP_200_OK)
def get_all():
    return todo_service.list()


@api.get("/{todo_id}", status_code=status.HTTP_200_OK)
def get(todo_id: str) -> Todo:
    return todo_service.get(todo_id)
"""
