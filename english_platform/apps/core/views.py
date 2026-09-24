import mimetypes
import re
from pathlib import Path
from typing import Iterator

from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse, StreamingHttpResponse


def serve_media_with_range(
    request: HttpRequest, path: str
) -> HttpResponse | StreamingHttpResponse:
    media_root = Path(settings.MEDIA_ROOT).resolve()
    target_path = (media_root / path).resolve()

    if not target_path.is_relative_to(media_root) or not target_path.is_file():
        raise Http404("Media file not found.")

    file_size: int = target_path.stat().st_size
    content_type, _ = mimetypes.guess_type(str(target_path))
    content_type = content_type or "application/octet-stream"

    range_header: str = request.headers.get("Range", "").strip()
    range_match = re.match(r"bytes=(\d+)-(\d*)", range_header)

    if range_match:
        start_byte: int = int(range_match.group(1))
        end_byte: int = (
            int(range_match.group(2)) if range_match.group(2) else file_size - 1
        )
        end_byte = min(end_byte, file_size - 1)
        content_length: int = end_byte - start_byte + 1

        def file_iterator(
            start_pos: int, chunk_len: int, chunk_size: int = 65536
        ) -> Iterator[bytes]:
            with open(target_path, "rb") as file_handle:
                file_handle.seek(start_pos)
                remaining: int = chunk_len
                while remaining > 0:
                    read_len = min(chunk_size, remaining)
                    chunk = file_handle.read(read_len)
                    if not chunk:
                        break
                    remaining -= len(chunk)
                    yield chunk

        response = StreamingHttpResponse(
            file_iterator(start_byte, content_length),
            status=206,
            content_type=content_type,
        )
        response["Content-Range"] = f"bytes {start_byte}-{end_byte}/{file_size}"
        response["Content-Length"] = str(content_length)
    else:

        def simple_iterator(chunk_size: int = 65536) -> Iterator[bytes]:
            with open(target_path, "rb") as file_handle:
                while chunk := file_handle.read(chunk_size):
                    yield chunk

        response = StreamingHttpResponse(
            simple_iterator(),
            status=200,
            content_type=content_type,
        )
        response["Content-Length"] = str(file_size)

    response["Accept-Ranges"] = "bytes"
    return response
