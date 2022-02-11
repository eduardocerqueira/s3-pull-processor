from io import BytesIO


def tarfile_mock(file_name):
    file_path = "/tmp"
    buf = BytesIO(b"e" * (1024**1))  # small file KB for 1MB ** 2
    with open(f"{file_path}/{file_name}", "wb") as file_tmp:
        file_tmp.write(buf.getbuffer())
    return f"{file_path}/{file_name}"
