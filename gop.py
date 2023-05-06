from pydub import AudioSegment
import pydub

pydub.AudioSegment.ffmpeg = "/absolute/path/to/ffmpeg"
sound = AudioSegment.from_file("Tong.mp3", format="mp3")
new_pitch = 1.2 # Ví dụ: tăng pitch lên 1.5 lần
new_speed = 1.1
new_sound = sound._spawn(sound.raw_data, overrides={"pitch": new_pitch, "frame_rate": int(sound.frame_rate * new_speed)})
new_sound = new_sound.set_frame_rate(sound.frame_rate)
# Phát file âm thanh
new_sound.export("new_Tong.mp3", format="mp3")