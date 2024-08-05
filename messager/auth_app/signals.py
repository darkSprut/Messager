from pathlib import Path
from django.conf import settings
import shutil
import os


def del_image(sender, instance,  **kwargs):
    path_to_file = Path(settings.MEDIA_ROOT).joinpath(Path(str(instance.image)))
    if Path(path_to_file).exists():
        shutil.rmtree(path_to_file.parent)

