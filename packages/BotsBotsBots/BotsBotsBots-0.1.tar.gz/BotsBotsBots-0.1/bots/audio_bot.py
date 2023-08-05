from pydub import AudioSegment
from pydub.utils import which

# sometimes ffmpeg is not the default converter
AudioSegment.converter = which("ffmpeg")


def sound_file_to_array(sound_path):
    return AudioSegment.from_file(sound_path)


def array_to_sound_file(sound_array, destination_path, file_format='mp3'):
    sound_array.export(destination_path, format=file_format)
