import torch

from sonosco.inference.asr import SonoscoASR
from sonosco.decoders import GreedyDecoder
from sonosco.datasets.processor import AudioDataProcessor
from sonosco.models.seq2seq_las import Seq2Seq
from sonosco.common.global_settings import DEVICE


class LasInference(SonoscoASR):

    def __init__(self, model_path):
        """
        LAS inference implementation.
        Args:
            model_path: path to LAs model
        """
        super().__init__(model_path)
        self.model, self.config = self.loader.deserialize(Seq2Seq, model_path, with_config=True)
        self.model.eval()
        self.processor = AudioDataProcessor(**self.config)
        self.decoder = GreedyDecoder(self.config["labels"])

    def infer_from_path(self, path: str) -> str:
        """
        Infer speech from audio under path
        Args:
            path: path to audio

        Returns: inferred text

        """
        spect, lens = self.processor.parse_audio_for_inference(path)
        spect = spect.to(DEVICE)

        with torch.no_grad():
            output = self.model.recognize(spect[0], lens, self.config["labels"], self.config["recognizer"])[0]

        transcription = self.decoder.convert_to_strings(torch.tensor([output['yseq']]))[0]

        return transcription
