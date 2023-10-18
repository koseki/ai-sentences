import glob
import os
import re
import shlex
import sys

"""
MP3 ファイルに ID3v2 タグを設定します。
"""

def main():
    sentence_file = sys.argv[1]
    number = os.path.splitext(os.path.basename(sentence_file))[0]
    dir = os.path.dirname(sentence_file)
    sentences = parse_sentence_file(sentence_file)

    for key, value in sentences.items():
        track = int(key)
        title = shlex.quote(value[0])
        uslt = shlex.quote(f":{value[1]}:eng")
        target_mp3 = glob.glob(f"{dir}/{number}/{key}-*")[0]
        print(f"id3v2 -D {target_mp3}")
        print(f"id3v2 --TPE1 koseki --TALB \"ElevenEnglish {number}\" --TRCK {track}/30 --TYER 2023 --TIT2 {title} --USLT {uslt} {target_mp3}")


def parse_sentence_file(file):
    result = {}
    current_no = ""
    title = ""
    with open(file, 'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        lines = filter(None, lines)
        for line in lines:
            m = re.match(r'# ((\d+) .+)', line)
            if m:
                current_no = m.group(2)
                title = m.group(1)
            else:
                result[current_no] = (title, line)

    return result
