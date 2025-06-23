from tinytag import TinyTag
from os.path import basename, isdir, join


def extract_thumbnail_file_from_mp3(mp3_filename: str, dest_dir: str):
    if not isdir(dest_dir):
        raise ValueError("Destination directory must be a valid directory.")
    tag = TinyTag.get(mp3_filename, image=True)
    data = tag.images.any.data
    ext = tag.images.any.mime_type.split("/")[-1]
    filename = basename(mp3_filename).replace("mp3", ext)
    path = join(dest_dir, filename)
    with open(path, "wb") as f:
        f.write(data)
    return path
