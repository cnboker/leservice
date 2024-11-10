import re
from TTS.utils.synthesizer import Synthesizer
from TTS.utils.manage import ModelManager
import numpy as np
import torch
import re
from logmmse import logmmse

manager = ModelManager()

# 测试中英文混合文本
# text = "根据 2023 年 1 月联合国世界人口展望，very good中国的人口估计为 14.26 亿, Hello, 这是一个测试。This is a test."
# mixed_audio = split_text(text)
# output ['根据', '2023', '年', '1', '月联合国世界人口展望', 'very good', '中国的人口估计为', '14.26', '亿', 'Hello', '这是一个测试', 'This is a test']

def split_text(text):
   
    # 分割规则：匹配中文段落、数字（含小数点）、英文单词及短语
    segments = re.findall(r'[\u4e00-\u9fff]+(?:[0-9\u4e00-\u9fff]+)?|[a-zA-Z\s]+|[\d.]+', text)
    
    # 清理段落之间的多余空格，并移除仅包含标点符号的片段
    cleaned_segments = [segment.strip() for segment in segments if segment.strip() and not re.fullmatch(r'[\W_]+', segment)]
    print("cleaned_segments", cleaned_segments)
    return cleaned_segments


def detected_language(text):
    if re.search(r'[\u4e00-\u9fff]|\d',text):
        return "zh"
    else:
        return "en"    

def create_synthesizer(model_name):
    model_path, config_path, model_item = manager.download_model(model_name)
    synthesizer = Synthesizer(
        model_path, config_path, None, None, None,
    )
    return synthesizer

#12.5转为12点5
def convert_digital(str):
    match = re.match(r'(\d{2})\.(\d{2})', str)
    if match:
        d1 = int(match.group(1))
        d2 = match.group(2)
       
        return f"{d1}点{d2}"
    else:
        return str  # 如果不匹配格式，保持原样

# 示例
# time_str = "14.26"
# converted_time = convert_time_24_to_12(time_str)
# print(converted_time)  # 输出: 12点26


en_synthesizer = create_synthesizer("tts_models/en/ljspeech/tacotron2-DDC")
cn_synthesizer = create_synthesizer("tts_models/zh-CN/baker/tacotron2-DDC-GST")

def synthese(text,callback):
    sentences = split_text(text)
    for sentence in sentences:
        if sentence.strip():       
            sentence = convert_digital(sentence)    
            language = detected_language(sentence)
            print(f"Generating audio for: {sentence}",language)
            synthesizer = cn_synthesizer if language == "zh" else en_synthesizer          
            tail =  "。" if language == "zh" else "."
            audio_data = synthesizer.tts(sentence + tail)
            # if tensor convert to numpy
            if torch.is_tensor(audio_data):
                audio_data = audio_data.cpu().numpy()
            if isinstance(audio_data, list):
                audio_data = np.array(audio_data)
                # Optional: Normalize the audio to make it louder if the levels are low
            audio_data = audio_data * (32767 / max(0.01, np.max(np.abs(audio_data))))

            audio_data = audio_data.astype(np.int16)
            print("synthesizer.output_sample_rate,",synthesizer.output_sample_rate,)
            #enhanced = logmmse(audio_data, synthesizer.output_sample_rate, output_file=None, initial_noise=1, window_size=160, noise_threshold=0.15)
            if callback:
                callback(audio_data.tobytes())