from io import BytesIO
from random import randint

from pydub.audio_segment import AudioSegment

from src.plugins.song_guess import get_song_path
from src.plugins.song_guess.model import get_random_song


# length: 歌曲片段长度（秒）
# 第一个返回值为歌曲名，第二个返回值为原曲片段，第三个返回值为背景音乐片段
async def generate_problem(length: int) -> tuple[str, BytesIO, BytesIO]:
    answer = await get_random_song()
    original_path, instrumental_path = get_song_path(answer + ".mp3")
    original_audio: AudioSegment = AudioSegment.from_file(original_path, format="mp3")
    instrumental_audio: AudioSegment = AudioSegment.from_file(instrumental_path, format="mp3")
    start = randint(0, len(original_audio) - length * 1000)
    original_bytes = BytesIO()
    original_audio[start:start + length * 1000].export(original_bytes, format="mp3")
    instrumental_bytes = BytesIO()
    instrumental_audio[start: start + length * 1000].export(instrumental_bytes, format="mp3")
    return (answer, original_bytes, instrumental_bytes)