import os


def _change_permissions(path: str, permissions=0o777) -> None:
    try:
        os.chmod(path, permissions)
    except Exception:
        # TODO: specific error messaging
        raise


def _path_exists(path: str) -> bool:
    return os.path.exists(path)


def _is_dir(path: str) -> bool:
    _change_permissions(path)
    return os.path.isdir(path)


def _is_file(path: str) -> bool:
    _change_permissions(path)
    return os.path.isfile(path)


def _get_file_extension(path: str) -> str:
    return os.path.splitext(path)[1].lower()


def resolve_path(*args: str) -> str:
    if len(args) == 0:
        return
    return os.path.abspath(os.path.join(os.getcwd(), *args))


def sanitize_input(input: str) -> str:
    if not input:
        return None

    # only using the first line
    return input.split("\n")[0].strip(" ")


# not an exhaustive list, just because it isn't here doesn't mean it's not allowed
DISALLOWED_FILE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"]


similar_paths = {
    "js": ["jsx", "js"],
    "jsx": ["js", "jsx"],
    "ts": ["tsx", "ts"],
    "tsx": ["ts", "tsx"],
}


def validate_file_path(abs_path: str) -> None:
    # TODO: specific error messaging
    abs_path = sanitize_input(abs_path)
    ext = _get_file_extension(abs_path)
    paths_to_try = similar_paths.get(ext, [])

    for path in paths_to_try:
        path = resolve_path(abs_path, path)

    if not _path_exists(abs_path):
        raise ValueError(f"{abs_path} does not exist")
    if _is_dir(abs_path):
        raise ValueError(f"{abs_path} is a directory, not a file")
    if not _is_file(abs_path):
        raise ValueError(f"{abs_path} is not a file")

    file_extension = _get_file_extension(abs_path)
    if file_extension in DISALLOWED_FILE_EXTENSIONS:
        raise ValueError(f"File extension {file_extension} is not allowed")


def validate_directory_path(abs_path: str) -> bool:
    # TODO: specific error messaging
    abs_path = sanitize_input(abs_path)

    created = False
    if not _path_exists(abs_path):
        os.makedirs(abs_path)
        created = True
    else:
        if _is_file(abs_path):
            raise ValueError(f"{abs_path} is a file, not a directory")
        if not _is_dir(abs_path):
            raise ValueError(f"{abs_path} is not a directory")

    return created
