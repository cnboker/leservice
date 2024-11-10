import torch
from TTS.api import TTS

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# # List available 🐸TTS models
# print(TTS().list_models())

# # Init TTS
tts = TTS("tts_models/zh-CN/baker/tacotron2-DDC-GST").to(device)

tts.tts_to_file(text="您可以tts直接在终端上运行并合成语音。 黄晓明，1977年11月13日出生于山东省青岛市，毕业于北京电影学院表演系。中国内地男演员、流行乐歌手。1998年，主演首部都市剧《爱情不是游戏》。2001年，凭借古装历史剧《大汉天子》获得关注。2004年，凭借古装剧《大汉天子2》获得第4届中国电视艺术双十佳演员奖。2005年，入选福布斯中国名人榜",
                file_path="output.wav",
             
                split_sentences=True
                )