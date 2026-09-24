from threading import Lock

from apps.films.dataclasses import ProgressState


class ProgressTracker:
    def __init__(self) -> None:
        self._lock = Lock()
        self._tasks: dict[str, ProgressState] = {}

    def start_task(self, task_id: str) -> None:
        with self._lock:
            self._tasks[task_id] = ProgressState(
                status="starting", message="Initializing download..."
            )

    def update_task(
        self,
        task_id: str,
        status: str,
        percent: float = 0.0,
        speed: str = "",
        eta: str = "",
        message: str = "",
        film_id: int | None = None,
        error: str | None = None,
    ) -> None:
        with self._lock:
            state = self._tasks.get(task_id)
            if state is not None:
                state.status = status
                state.percent = percent
                state.speed = speed
                state.eta = eta
                if message:
                    state.message = message
                if film_id is not None:
                    state.film_id = film_id
                if error is not None:
                    state.error = error

    def get_task(self, task_id: str) -> ProgressState | None:
        with self._lock:
            return self._tasks.get(task_id)

    def cleanup_task(self, task_id: str) -> None:
        with self._lock:
            self._tasks.pop(task_id, None)


progress_tracker = ProgressTracker()
