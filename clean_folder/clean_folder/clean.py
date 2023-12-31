from pathlib import Path
import shutil
import sys
import re

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = (
    "a",
    "b",
    "v",
    "g",
    "d",
    "e",
    "e",
    "j",
    "z",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "r",
    "s",
    "t",
    "u",
    "f",
    "h",
    "ts",
    "ch",
    "sh",
    "sch",
    "",
    "y",
    "",
    "e",
    "yu",
    "u",
    "ja",
    "je",
    "ji",
    "g",
)
TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def normalize(name: str) -> str:
    t_name = name.translate(TRANS)
    t_name = re.sub(r"\W", "_", t_name)
    last = t_name.rfind("_")
    t_name = f"{t_name[:last]}.{t_name[last+1:]}"
    return t_name


JPEG_IMAGES = []
JPG_IMAGES = []
PNG_IMAGES = []
SVG_IMAGES = []
AVI_VIDEO = []
MP4_VIDEO = []
MOV_VIDEO = []
MKV_VIDEO = []
DOC_DOCUMENTS = []
DOCX_DOCUMENTS = []
TXT_DOCUMENTS = []
PDF_DOCUMENTS = []
XLSX_DOCUMENTS = []
PPTX_DOCUMENTS = []
MP3_AUDIO = []
OGG_AUDIO = []
WAV_AUDIO = []
AMR_AUDIO = []
ZIP_ARCHIVES = []
GZ_ARCHIVES = []
TAR_ARCHIVES = []
MY_OTHER = []


REGISTER_EXTENSION = {
    "JPEG": JPEG_IMAGES,
    "JPG": JPG_IMAGES,
    "PNG": PNG_IMAGES,
    "SVG": SVG_IMAGES,
    "AVI": AVI_VIDEO,
    "MP4": MP4_VIDEO,
    "MOV": MOV_VIDEO,
    "MKV": MKV_VIDEO,
    "DOC": DOC_DOCUMENTS,
    "DOCX": DOCX_DOCUMENTS,
    "TXT": TXT_DOCUMENTS,
    "PFD": PDF_DOCUMENTS,
    "XLSX": XLSX_DOCUMENTS,
    "PPTX": PPTX_DOCUMENTS,
    "MP3": MP3_AUDIO,
    "OGG": OGG_AUDIO,
    "WAV": WAV_AUDIO,
    "AMR": AMR_AUDIO,
    "ZIP": ZIP_ARCHIVES,
    "GZ": GZ_ARCHIVES,
    "TAR": TAR_ARCHIVES,
}

FOLDERS = []
EXTENSION = set()
UNKNOWN = set()


def get_extension(filename: str) -> str:
    return (
        Path(filename).suffix[1:].upper()
    )  # перетворюємо розширення файлу на назву папки jpg -> JPG


def scan(folder: Path) -> None:
    for item in folder.iterdir():
        # Якщо це папка то додаємо її до списку FOLDERS і переходимо до наступного елемента папки
        if item.is_dir():
            # перевіряємо, щоб папка не була тією в яку ми складаємо вже файли
            if item.name not in (
                "archives",
                "video",
                "audio",
                "documents",
                "images",
                "MY_OTHER",
            ):
                FOLDERS.append(item)
                # скануємо вкладену папку
                scan(item)  # рекурсія
            continue  # переходимо до наступного елементу в сканованій папці

        #  Робота з файлом
        ext = get_extension(item.name)  # беремо розширення файлу
        fullname = folder / item.name  # беремо шлях до файлу
        if not ext:  # якщо файл немає розширення то додаєм до невідомих
            MY_OTHER.append(fullname)
        else:
            try:
                container = REGISTER_EXTENSION[ext]
                EXTENSION.add(ext)
                container.append(fullname)
            except KeyError:
                # Якщо ми не зареєстрували розширення у REGISTER_EXTENSION, то додаємо до невідомих
                UNKNOWN.add(ext)
                MY_OTHER.append(fullname)


def handle_media(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_other(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_archive(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)  # робимо папку для архіва
    folder_for_file = target_folder / normalize(
        filename.name.replace(filename.suffix, "")
    )
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(filename, folder_for_file)  # TODO: Check!
    except shutil.ReadError:
        print("It is not archive")
        folder_for_file.rmdir()
    filename.unlink()


def handle_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f"Can't delete folder: {folder}")


def main(folder: Path):
    scan(folder)
    for file in JPEG_IMAGES:
        handle_media(file, folder / "images" / "JPEG")
    for file in JPG_IMAGES:
        handle_media(file, folder / "images" / "JPG")
    for file in PNG_IMAGES:
        handle_media(file, folder / "images" / "PNG")
    for file in SVG_IMAGES:
        handle_media(file, folder / "images" / "SVG")
    for file in AVI_VIDEO:
        handle_media(file, folder / "videos" / "AVI")
    for file in MP4_VIDEO:
        handle_media(file, folder / "videos" / "MP4")
    for file in MOV_VIDEO:
        handle_media(file, folder / "videos" / "MOV")
    for file in MKV_VIDEO:
        handle_media(file, folder / "videos" / "MKV")
    for file in DOC_DOCUMENTS:
        handle_media(file, folder / "documents" / "DOC")
    for file in DOCX_DOCUMENTS:
        handle_media(file, folder / "documents" / "DOCX")
    for file in TXT_DOCUMENTS:
        handle_media(file, folder / "documents" / "TXT")
    for file in PDF_DOCUMENTS:
        handle_media(file, folder / "documents" / "PDF")
    for file in XLSX_DOCUMENTS:
        handle_media(file, folder / "documents" / "SLXS")
    for file in PPTX_DOCUMENTS:
        handle_media(file, folder / "documents" / "PPTX")
    for file in MP3_AUDIO:
        handle_media(file, folder / "audio" / "MP3")
    for file in OGG_AUDIO:
        handle_media(file, folder / "audio" / "OGG")
    for file in WAV_AUDIO:
        handle_media(file, folder / "audio" / "WAV")
    for file in AMR_AUDIO:
        handle_media(file, folder / "audio" / "AMR")
    for file in ZIP_ARCHIVES:
        handle_archive(file, folder / "archives" / "ZIP_ARCHIVES")
    for file in GZ_ARCHIVES:
        handle_archive(file, folder / "archives" / "GZ_ARCHIVES")
    for file in TAR_ARCHIVES:
        handle_archive(file, folder / "archives" / "TAR_ARCHIVES")

    for file in MY_OTHER:
        handle_other(file, folder / "MY_OTHER")

    for folder in FOLDERS[::-1]:
        handle_folder(folder)


# def run():
#     if sys.argv[1]:
#         folder_for_scan = Path(sys.argv[1])
#         print(f"Start in folder: {folder_for_scan.resolve()}")
#         main(folder_for_scan.resolve())


def clean():
    if sys.argv[1]:
        folder_for_scan = Path(sys.argv[1])
        print(f"Clean in folger {folder_for_scan.resolve()}")
        main(folder_for_scan.resolve())


if __name__ == "__main__":
    # Set-ExecutionPolicy Bypass
    # run()
    clean()
    folder_to_scan = sys.argv[1]
    print(f"Start in folder {folder_to_scan}")
    scan(Path(folder_to_scan))
    print(f"Images jpeg: {JPEG_IMAGES}")
    print(f"Images jpg: {JPG_IMAGES}")
    print(f"Images svg: {SVG_IMAGES}")
    print(f"Images png: {PNG_IMAGES}")
    print(f"Videos avi: {AVI_VIDEO}")
    print(f"Videos mov: {MOV_VIDEO}")
    print(f"Videos mkv: {MKV_VIDEO}")
    print(f"Videos mp4: {MP4_VIDEO}")
    print(f"Documents doc: {DOC_DOCUMENTS}")
    print(f"Documents docx: {DOCX_DOCUMENTS}")
    print(f"Documents txt: {TXT_DOCUMENTS}")
    print(f"Documents pdf: {PDF_DOCUMENTS}")
    print(f"Documents xlsx: {XLSX_DOCUMENTS}")
    print(f"Documents pptx: {PPTX_DOCUMENTS}")
    print(f"Audio mp3: {MP3_AUDIO}")
    print(f"Audio ogg: {OGG_AUDIO}")
    print(f"Audio wav: {WAV_AUDIO}")
    print(f"Audio amr: {AMR_AUDIO}")
    print(f"Archives zip: {ZIP_ARCHIVES}")
    print(f"Archives gz: {GZ_ARCHIVES}")
    print(f"Archives tar: {TAR_ARCHIVES}")

    print(f"Types of files in folder: {EXTENSION}")
    print(f"Unknown files of types: {UNKNOWN}")
    print(f"MY_OTHER: {MY_OTHER}")

    print(FOLDERS)
