import time
from typing import Any, Dict, List

import attr


@attr.s(auto_attribs=True)
class ImageTrainingStep:
    n_epochs: int
    lr: float
    augmentation: int
    freeze: bool
    compile_params: Dict[str, Any]


@attr.s(auto_attribs=True)
class ImageTrainer:
    learner: int
    data_container: int
    steps: List[ImageTrainingStep]
    template: str = """
        Name: {} Train Time: {:.1f} min. Eval Time: {:.2f}s Loss: {:.4f} Accuracy: {:.2%}
    """

    def __call__(self):
        start_time = time.time()
        for step in self.steps:
            self.learner.freeze() if step.freeze else self.learner.unfreeze()
            self.learner.compile(**step.compile_params)
            self.learner.train(step.n_epochs)
        end_time = time.time()

        eval_start_time = time.time()
        evaluation_results = self.learner.evaluate_dataset(verbose=0)
        eval_end_time = time.time()

        print("-".center(80, "-"))
        print(
            self.template.format(
                self.learner.base_model.name,
                (end_time - start_time) / 60,
                (eval_end_time - eval_start_time),
                *evaluation_results,
            )
        )
        print("-".center(80, "-"))

