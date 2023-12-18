# from transformers import pipeline, WhisperTokenizer, WhisperFeatureExtractor
# import gradio as gr
# import librosa
# from audiocap import WhisperForAudioCaptioning
# import os

# checkpoint = "MU-NLPC/whisper-tiny-audio-captioning"
# # checkpoint = "novecentos/whisper-small-hi"
# model = WhisperForAudioCaptioning.from_pretrained(checkpoint)
# tokenizer = WhisperTokenizer.from_pretrained(checkpoint, language="en", task="transcribe")
# feature_extractor = WhisperFeatureExtractor.from_pretrained(checkpoint)
# inputDir = 'generated_dataset/data/'

# # for filename in os.listdir(inputDir):
# # Load and preprocess audio
# filename = 'The.Big.Bang.Theory.S05E01_285.mp3'
# input_file =os.path.join(inputDir,filename)
# audio, sampling_rate = librosa.load(input_file, sr=feature_extractor.sampling_rate)
# features = feature_extractor(audio, sampling_rate=sampling_rate, return_tensors="pt").input_features

# # Prepare caption style
# # style_prefix = str(filename) + " > caption: "
# # style_prefix = "audiocaps > caption:"
# # style_prefix = "clotho > caption:"
# style_prefix = "audioset > keywords:"

# # style_prefix = '['
# style_prefix_tokens = tokenizer("", text_target=style_prefix, return_tensors="pt", add_special_tokens=False).labels

# # Generate caption
# model.eval()
# outputs = model.generate(
#     inputs=features.to(model.device),
#     forced_ac_decoder_ids=style_prefix_tokens,
#     max_length=100,
# )
# # print(str(filename) + ": ")
# print(tokenizer.batch_decode(outputs, skip_special_tokens=True)[0])# def transcribe(audio):
# # print(tokenizer.batch_decode(outputs, skip_special_tokens=True)[0] + "]")# def transcribe(audio):


# import gradio as gr
# from transformers import pipeline, AutoModel, AutoTokenizer, WhisperTokenizer, WhisperFeatureExtractor
# checkpoint = "novecentos/whisper-small-hi"
# # checkpoint = "openai/whisper-small"
# # checkpoint = "MU-NLPC/whisper-tiny-audio-captioning"

# tokenizer = WhisperTokenizer.from_pretrained(checkpoint, language="en", task="transcribe")
# feature_extractor = WhisperFeatureExtractor.from_pretrained(checkpoint)
# # tokenizer = WhisperTokenizer.from_pretrained(checkpoint, language="pt", task="audio-classification")
# # feature_extractor = WhisperFeatureExtractor.from_pretrained(checkpoint)
# pipe = pipeline(model=checkpoint, tokenizer=tokenizer, feature_extractor=feature_extractor, task="automatic-speech-recognition")

# def transcribe(audio):
#     print(pipe(audio))
#     text = pipe(audio)["text"]
#     return text

# iface = gr.Interface(
#     fn=transcribe, 
#     # inputs=gr.File(file_count="data/test/The.Big.Bang.Theory.S03E22.720p.AMZN.WEBRip.x264-GalaxyTV_152.mp3"),
#     # inputs=gr.Audio("dataset/data/test/The.Big.Bang.Theory.S03E22.720p.AMZN.WEBRip.x264-GalaxyTV_152.mp3"), 
#     inputs=gr.Audio(sources="upload", type="filepath"), 
#     outputs="text",
#     title="Whisper Small CC",
#     description="Realtime demo for sound recognition using a fine-tuned Whisper small model.",
# )

# iface.launch(share=True)

# import os
# import librosa
# import gradio as gr
# from transformers import pipeline, AutoModel, AutoTokenizer, WhisperTokenizer, WhisperFeatureExtractor
# # checkpoint = "novecentos/whisper-small-hi"
# checkpoint = "openai/whisper-small"
# # checkpoint = "MU-NLPC/whisper-tiny-audio-captioning"

# tokenizer = WhisperTokenizer.from_pretrained(checkpoint, language="pt-BR", task="transcribe")
# feature_extractor = WhisperFeatureExtractor.from_pretrained(checkpoint)
# # tokenizer = WhisperTokenizer.from_pretrained(checkpoint, language="pt", task="audio-classification")
# # feature_extractor = WhisperFeatureExtractor.from_pretrained(checkpoint)
# pipe = pipeline(model=checkpoint, tokenizer=tokenizer, feature_extractor=feature_extractor, task="automatic-speech-recognition")

# def transcribe(audio):
#     # print(pipe(audio))
#     text = pipe(audio)["text"]
#     return text


# def run():
#     inputDir = 'audios'
#     while True:
#         if len(os.listdir(inputDir)) > 0:
#             for filename in os.listdir(inputDir):
#                 f = os.path.join(inputDir, filename)
#                 if os.path.isfile(f) and filename.endswith('.mp3'):
#                     audio, sampling_rate = librosa.load(f, sr=feature_extractor.sampling_rate)
#                     features = feature_extractor(audio, sampling_rate=sampling_rate, return_tensors="pt").input_features
#                     print(transcribe(audio))
#                     os.remove(f)

# if __name__ == '__main__':
# 	run()
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import whisper
import torch
import cv2
import os
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:100'
torch.cuda.empty_cache() 

vid = cv2.VideoCapture(0) 

model = whisper.load_model("medium")
def run():
    inputDir = 'audios'
    font = cv2.FONT_HERSHEY_COMPLEX 
    fontScale = 0.6
    color = (255, 255, 255) 
    thickness = 2

    text_to_show = ""
    while True:
        ret, frame = vid.read() 
    
        if len(os.listdir(inputDir)) > 0:
            for filename in os.listdir(inputDir):
                f = os.path.join(inputDir, filename)
                if os.path.isfile(f) and filename.endswith('.mp3'):
                    # load audio and pad/trim it to fit 30 seconds
                    audio = whisper.load_audio(f)
                    audio = whisper.pad_or_trim(audio)

                    # make log-Mel spectrogram and move to the same device as the model
                    mel = whisper.log_mel_spectrogram(audio).to(model.device)

                    # detect the spoken language
                    _, probs = model.detect_language(mel)
                    detected_language = max(probs, key=probs.get)
                    # print(f"Detected language: {detected_language}")
                    if detected_language == 'pt':
                        # decode the audio
                        options = whisper.DecodingOptions(language="pt")
                        result = whisper.decode(model, mel, options)

                        # print the recognized text
                        text_to_show = result.text
                        print(result.text)
                        
                    os.remove(f)
        height, width, channels = frame.shape
        org = (int(width * 0.5), int(height * 0.9)) 

        # frame = cv2.putText(frame, text_to_show, org, font,  
                            # fontScale, color, thickness, cv2.LINE_AA) 
        
        frame = Image.fromarray(frame)
        draw = ImageDraw.Draw(frame)
        draw.text(org, text_to_show, align='center')
        frame = np.asarray(frame)
        cv2.imshow('frame', frame) 
      
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break


if __name__ == '__main__':
	run()
     
