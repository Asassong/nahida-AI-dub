from pydub import AudioSegment
from pydub.silence import split_on_silence
from pypinyin import lazy_pinyin, Style
import os
import re


def combine_audio(path1, path2):
    audio1 = AudioSegment.from_wav(path1)
    audio2 = AudioSegment.from_wav(path2)
    audio = audio1 + audio2
    audio.export(path1, format="wav")


def split_audio(path, ts):
    audio = AudioSegment.from_wav(path)
    audio1 = audio[:ts*1000]
    audio2 = audio[ts*1000:]
    init_num = path[-6:-4]
    num = int(init_num) + 1
    position = len(path) - 6
    path2 = path[position:]
    path2 = re.sub(init_num, "%02d" % num, path2, 1)  # 用flags会出错
    path2 = path[:position] + path2
    audio1.export(path, format="wav")
    audio2.export(path2, format="wav")


def gen_multispeaker_datasets(file_path, output_file_path):
    speakers = os.listdir(file_path)
    j = 0
    for speaker in speakers:
        if os.path.isdir(file_path + "/" + speaker):
            files = os.listdir(file_path + "/" + speaker)
            if not os.path.exists(output_file_path + "/" + speaker):
                os.mkdir(output_file_path + "/" + speaker)
            else:
                state = input("文件已存在，请输入y/n确认是否继续")
                if state == "n":
                    exit(-1)
            label = open(r"%s\%s\labels.txt" % (output_file_path, speaker), "w")
            for audio_file in files:
                if audio_file.endswith(".wav"):
                    text = re.sub(".wav", "", audio_file)
                    text = re.sub("[「」~。？，…！：—、.]", "", text)
                    audio = AudioSegment.from_wav(file_path + "/" + speaker + "/" + audio_file)
                    audio.export(r"%s\%s\%06d.wav" % (output_file_path, speaker, j), format="wav")
                    pinyin_list = lazy_pinyin(text, style=Style.TONE3, neutral_tone_with_five=True)
                    for i, pinyin in enumerate(pinyin_list):
                        if pinyin == "n2":
                            pinyin_list[i] = "en2"
                    pinyin_str = " ".join(pinyin_list)
                    label.write("%06d|%s\n" % (j, pinyin_str))
                    j += 1




# audio_path = r"D:\clouddrivedownload\nahida"
# if not os.path.exists("%s\\nahida-voice" % os.getcwd()):
#     os.mkdir("%s\\nahida-voice" % os.getcwd())
#     os.mkdir("%s\\nahida-voice\\reliable" % os.getcwd())
#     os.mkdir("%s\\nahida-voice\\unreliable" % os.getcwd())
#     os.mkdir("%s\\nahida-voice\\unknown" % os.getcwd())
# label = open(r"D:\paddlespeech_nahida_tts3\input\nahida\labels.txt", "w")
# audio_files = os.listdir(audio_path)
# j = 0
# for audio_file in audio_files:
#     if audio_file.endswith(".wav"):
#         text = re.sub(".wav", "", audio_file)
#         text = re.sub("[「」~。？，…！：—、.]", "", text)
#         # print("%s\\%s D:\\paddlespeech_nahida\\input\\nahida\\%06d.wav" % (audio_path, audio_file, j))
#         # text = re.sub("[「」~]", "", text)
#         # texts = re.split("[。？，…！]", text)
#         # texts = [split_text for split_text in texts if len(split_text) > 2]
#         audio = AudioSegment.from_wav(audio_path + "\\" + audio_file)
#         # if audio.duration_seconds > 1:
#         #     silence_len = 420
#         #     thresh = -40
#         #     chunks = split_on_silence(audio, min_silence_len=silence_len, silence_thresh=thresh)
#         #     chunks = [chunk for chunk in chunks if chunk.duration_seconds > 1]
#         #     if len(chunks) > len(texts):
#         #         silence_len = 500
#         #         chunks2 = split_on_silence(audio, min_silence_len=silence_len, silence_thresh=thresh)
#         #         chunks2 = [chunk for chunk in chunks2 if chunk.duration_seconds > 1]
#         #         if len(chunks2) == len(texts):
#         #             for i, chunk_audio in enumerate(chunks2):
#         #                 chunk_audio.export("%s\\nahida-voice\\unreliable\\%04d_%02d.wav" % (os.getcwd(), j, i),
#         #                                    format="wav")
#         #                 pinyin_list = lazy_pinyin(texts[i], style=Style.TONE3, neutral_tone_with_five=True)
#         #                 pinyin_str = " ".join(pinyin_list)
#         #                 label.write("%04d%02d|%s\n" % (j, i, pinyin_str))
#         #         else:
#         #             for i, chunk_audio in enumerate(chunks2):
#         #                 chunk_audio.export("%s\\nahida-voice\\unknown\\%04d_%02d.wav" % (os.getcwd(), j, i),
#         #                                    format="wav")
#         #             for i, chunk_text in enumerate(texts):
#         #                 pinyin_list = lazy_pinyin(chunk_text, style=Style.TONE3, neutral_tone_with_five=True)
#         #                 pinyin_str = " ".join(pinyin_list)
#         #                 label.write("%04d%02d|%s\n" % (j, i, pinyin_str))
#         #     elif len(chunks) < len(texts):
#         #         silence_len = 340
#         #         chunks2 = split_on_silence(audio, min_silence_len=silence_len, silence_thresh=thresh)
#         #         chunks2 = [chunk for chunk in chunks2 if chunk.duration_seconds > 1]
#         #         if len(chunks2) == len(texts):
#         #             for i, chunk_audio in enumerate(chunks2):
#         #                 chunk_audio.export("%s\\nahida-voice\\unreliable\\%04d_%02d.wav" % (os.getcwd(), j, i),
#         #                                    format="wav")
#         #                 pinyin_list = lazy_pinyin(texts[i], style=Style.TONE3, neutral_tone_with_five=True)
#         #                 pinyin_str = " ".join(pinyin_list)
#         #                 label.write("%04d%02d|%s\n" % (j, i, pinyin_str))
#         #         else:
#         #             for i, chunk_audio in enumerate(chunks2):
#         #                 chunk_audio.export("%s\\nahida-voice\\unknown\\%04d_%02d.wav" % (os.getcwd(), j, i),
#         #                                    format="wav")
#         #             for i, chunk_text in enumerate(texts):
#         #                 pinyin_list = lazy_pinyin(chunk_text, style=Style.TONE3, neutral_tone_with_five=True)
#         #                 pinyin_str = " ".join(pinyin_list)
#         #                 label.write("%04d%02d|%s\n" % (j, i, pinyin_str))
#         #     else:
#                 # for i, chunk_audio in enumerate(chunks):
#         audio.export(r"D:\paddlespeech_nahida_tts3\input\nahida\%06d.wav" % j, format="wav")
#         pinyin_list = lazy_pinyin(text, style=Style.TONE3, neutral_tone_with_five=True)
#         pinyin_str = " ".join(pinyin_list)
#         label.write("%06d|%s\n" % (j, pinyin_str))
#         j += 1
# label.close()

gen_multispeaker_datasets(r"D:\clouddrivedownload\yuanshen_audio", r"D:\paddlespeech_nahida_tts3\input")



