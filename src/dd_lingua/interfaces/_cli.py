import json
from multiprocessing import JoinableQueue, Process
from pathlib import Path

from loguru import logger

from dd_lingua.core.model import Lingua
from dd_lingua.schemas.settings import settings


def read_json(file_path:Path) -> dict:
    with open(file_path, 'r') as file:
        return json.load(file)

def write_json(data:dict, file_path:Path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


class Processor:
    def __init__(
            self, 
            in_dir: Path, 
            num_workers: int = 1, 
            multilingual: bool = True,
            max_chars: int = 1000,
            simplified: bool = True,
        ):
        self.in_dir = in_dir
        self.num_workers = num_workers
        self.queue = JoinableQueue()
        self.model = Lingua(
            eager_mode=settings.eager_mode,
            low_accuracy=settings.low_accuracy,
            script=settings.script,
            languages=settings.languages
        )
        self.multilingual = multilingual
        self.max_chars = max_chars
        self.simplified = simplified


    def get_files(self):
        num_files = 0
        logger.info(f"Searching for files in {self.in_dir}")
        for file_path in self.in_dir.rglob("*.json"):
            if file_path.is_file():
                self.queue.put(file_path)
                num_files += 1
        logger.info(f"Found {num_files} files")

    def process_file(self, file_path: Path):
        logger.info(f"Processing {file_path}")
        data = read_json(file_path)
        text = data.get('text')

        if text:
            output = self.model.infer(
                text=text["source"], 
                multilingual=self.multilingual, 
                max_chars=self.max_chars, 
                simplified=self.simplified
            )
            _ = output.pop('languages', None)
            if output:
                language = output.pop('language')
                output['languages'] = [language]
                data |= output

            write_json(data, file_path)

    def worker(self):
        while True:
            file_path = self.queue.get()
            if file_path is None:
                break
            try:
                self.process_file(file_path)
            except Exception as e:
                logger.error(f"Error processing {file_path}: {e}")
            finally:
                self.queue.task_done()

    def run(self):
        """Run the processor"""
        logger.info(f"Starting {self.num_workers} workers")
        workers = []
        for _ in range(self.num_workers):
            worker = Process(target=self.worker)
            worker.start()
            workers.append(worker)

        self.get_files()
        self.queue.join()

        logger.info("Stopping workers")
        for _ in range(self.num_workers):
            self.queue.put(None)
        for worker in workers:
            worker.join()

if __name__ == "__main__":
    import argparse

    def str2bool(v):
        if isinstance(v, bool):
            return v
        if v.lower() in ('yes', 'true', 't', 'y', '1'):
            return True
        elif v.lower() in ('no', 'false', 'f', 'n', '0'):
            return False
        else:
            raise argparse.ArgumentTypeError('Boolean value expected.')

    parser = argparse.ArgumentParser(description="Detect language of text in json files")
    parser.add_argument("in_dir", type=Path, help="Directory containing json files")
    parser.add_argument("--num_workers", type=int, default=1, help="Number of workers")
    parser.add_argument("--multilingual", type=str2bool, default=False, help="Whether to detect multiple languages (ie. code-switching)")
    parser.add_argument("--max_chars", type=int, default=10_000, help="Maximum number of characters to use for prediction")
    parser.add_argument("--simplified", type=str2bool, default=True, help="Whether to condense multilingual output to an array of languages")
    args = parser.parse_args()
    logger.info(f"Running with args: {args}")
    processor = Processor(
        in_dir=args.in_dir,
        num_workers=args.num_workers,
        multilingual=args.multilingual,
        max_chars=args.max_chars,
        simplified=args.simplified
    )
    processor.run()



