import torch
import librosa

from sonosco.inference.asr import SonoscoASR
from sonosco.decoders import GreedyDecoder
from sonosco.datasets.processor import AudioDataProcessor
from sonosco.models.deepspeech2_old import DeepSpeech2
from sonosco.common.global_settings import DEVICE


class DeepSpeech2Inference(SonoscoASR):

    def __init__(self, model_path):
        """
        DeepSpeech inference implementation.
        Args:
            model_path: path to DeepSpeech model
        """
        super().__init__(model_path)
        self.model = DeepSpeech2.load_model(model_path)
        self.model.eval()
        self.processor = AudioDataProcessor(**self.model.audio_conf)
        self.decoder = GreedyDecoder(self.model.labels, blank_index=self.model.labels.index('_'))

    def infer_from_path(self, path: str) -> str:
        """
        Infer speech from audio under path
        Args:
            path: path to audio

        Returns: inferred text

        """
        loaded, sr = librosa.load(path, sr=self.processor.sample_rate)
        spect = self.processor.parse_audio(sound=loaded, sample_rate=sr)
        spect = spect.view(1, 1, spect.size(0), spect.size(1))
        spect = spect.to(DEVICE)
        input_sizes = torch.IntTensor([spect.size(3)]).int()
        with torch.no_grad():
            out, output_sizes = self.model(spect, input_sizes)
        decoded_output, decoded_offsets = self.decoder.decode(out, output_sizes, remove_repetitions=True)
        return decoded_output[0]
