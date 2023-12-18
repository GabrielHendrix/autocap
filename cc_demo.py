from transformers import pipeline, WhisperTokenizer, WhisperFeatureExtractor
import gradio as gr
import librosa
from audiocap import WhisperForAudioCaptioning
import os

checkpoint = "MU-NLPC/whisper-tiny-audio-captioning"
# checkpoint = "novecentos/whisper-small-hi"
model = WhisperForAudioCaptioning.from_pretrained(checkpoint)
tokenizer = WhisperTokenizer.from_pretrained(checkpoint, language="en", task="transcribe")
feature_extractor = WhisperFeatureExtractor.from_pretrained(checkpoint)
# def transcribe(audio):
# print(tokenizer.batch_decode(outputs, skip_special_tokens=True)[0] + "]")# def transcribe(audio):

import whisper
import os


def run():
    inputDir = 'audios'
    while True:
        if len(os.listdir(inputDir)) > 0:
            for filename in os.listdir(inputDir):
                f = os.path.join(inputDir, filename)
                if os.path.isfile(f) and filename.endswith('.mp3'):
                    audio, sampling_rate = librosa.load(f, sr=feature_extractor.sampling_rate)
                    features = feature_extractor(audio, sampling_rate=sampling_rate, return_tensors="pt").input_features

                    # Prepare caption style
                    # style_prefix = str(filename) + " > caption: "
                    # style_prefix = "audiocaps > caption:"
                    style_prefix = "clotho > caption:"
                    # style_prefix = "audioset > keywords:"

                    # style_prefix = '['
                    style_prefix_tokens = tokenizer("", text_target=style_prefix, return_tensors="pt", add_special_tokens=False).labels

                    # Generate caption
                    model.eval()
                    outputs = model.generate(
                        inputs=features.to(model.device),
                        forced_ac_decoder_ids=style_prefix_tokens,
                        max_length=100,
                    )
                    # print(str(filename) + ": ")
                    print(tokenizer.batch_decode(outputs, skip_special_tokens=True)[0])
                    os.remove(f)


if __name__ == '__main__':
	run()
     
