from sotabencheval.core import BaseEvaluator
from sotabencheval.utils import calculate_batch_hash, change_root_if_server, is_server
from sotabencheval.machine_translation.languages import Language
from sotabencheval.machine_translation.metrics import TranslationMetrics
from typing import Dict
from pathlib import Path
from enum import Enum
import time

class WMTDataset(Enum):
    News2014 = "newstest2014"
    News2019 = "newstest2019"


class WMTEvaluator(BaseEvaluator):
    task = "Machine Translation"
    _datasets = {
        (WMTDataset.News2014, Language.English, Language.German),
        (WMTDataset.News2019, Language.English, Language.German),
        (WMTDataset.News2014, Language.English, Language.French),
    }

    def __init__(self,
                 dataset: WMTDataset,
                 source_lang: Language,
                 target_lang: Language,
                 local_root: str = '.',
                 source_dataset_filename: str = None,
                 target_dataset_filename: str = None,
                 model_name: str = None,
                 paper_arxiv_id: str = None,
                 paper_pwc_id: str = None,
                 paper_results: dict = None,
                 model_description=None):
        super().__init__(model_name, paper_arxiv_id, paper_pwc_id, paper_results, model_description)
        self.root = change_root_if_server(root=local_root,
                                          server_root=".data/nlp/wmt")
        self.dataset = dataset
        self.source_lang = source_lang
        self.target_lang = target_lang

        default_src_fn, default_dst_fn = self._get_source_dataset_filename()
        if source_dataset_filename is None or is_server():
            source_dataset_filename = default_src_fn

        if target_dataset_filename is None or is_server():
            target_dataset_filename = default_dst_fn

        self.source_dataset_path = Path(self.root) / source_dataset_filename
        self.target_dataset_path = Path(self.root) / target_dataset_filename

        self.metrics = TranslationMetrics(self.source_dataset_path, self.target_dataset_path)

        self.start_time = time.time()

    def _get_source_dataset_filename(self):
        if self.dataset == WMTDataset.News2014:
            other_lang = self.source_lang.value if self.target_lang == Language.English else self.target_lang.value
            source = "{0}-{1}en-src.{2}.sgm".format(self.dataset.value, other_lang, self.source_lang.value)
            target = "{0}-{1}en-ref.{2}.sgm".format(self.dataset.value, other_lang, self.target_lang.value)
        elif self.dataset == WMTDataset.News2019:
            source = "{0}-{1}{2}-src.{1}.sgm".format(self.dataset.value, self.source_lang.value, self.target_lang.value)
            target = "{0}-{1}{2}-ref.{2}.sgm".format(self.dataset.value, self.source_lang.value, self.target_lang.value)
        else:
            raise ValueError("Unknown dataset: {}".format(self.dataset))
        return source, target

    def _get_dataset_name(self):
        cfg = (self.dataset, self.source_lang, self.target_lang)
        if cfg not in WMTEvaluator._datasets:
            raise ValueError("Unsupported dataset configuration: {} {} {}".format(
                self.dataset.name,
                self.source_lang.name,
                self.target_lang.name
            ))

        ds_names = {WMTDataset.News2014: "WMT2014", WMTDataset.News2019: "WMT2019"}
        return "{0} {1}-{2}".format(ds_names.get(self.dataset), self.source_lang.fullname, self.target_lang.fullname)

    def update_inference_time(self):

        if not self.metrics._results and self.inference_time.count < 1:
            # assuming this is the first time the evaluator is called
            self.inference_time.update(time.time() - self.start_time)
        elif not self.metrics._results and self.inference_time.count > 0:
            # assuming the user has reset outputs, and is then readding (evaluation post batching)
            pass
        else:
            # if there are outputs and the inference time count is > 0
            self.inference_time.update(time.time() - self.start_time)

    def add(self, answers: Dict[str, str]):

        self.update_inference_time()

        self.metrics.add(answers)

        if not self.first_batch_processed and self.metrics.has_data:
            self.speed_mem_metrics['Tasks Per Second (Partial)'] = len(self.metrics.answers) / self.inference_time.sum
            self.batch_hash = calculate_batch_hash(
                self.cache_values(answers=self.metrics.answers,
                                  metrics=self.metrics.get_results(ignore_missing=True))
            )
            self.first_batch_processed = True

        self.start_time = time.time()

    def reset(self):
        self.metrics.reset()

    def get_results(self):
        if self.cached_results:
            return self.results
        self.results = self.metrics.get_results()
        self.speed_mem_metrics['Tasks Per Second (Total)'] = len(self.metrics.answers) / self.inference_time.sum

        return self.results

    def save(self):
        dataset = self._get_dataset_name()
        return super().save(dataset=dataset)

