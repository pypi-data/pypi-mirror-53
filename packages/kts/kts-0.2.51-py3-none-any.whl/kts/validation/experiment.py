import re
from collections import MutableSequence

import pandas as pd
import texttable as tt
from fastprogress import progress_bar as pb

from ..eda.importance import plot_importances
from ..feature.selection.selector import BuiltinImportance
from ..modelling import ArithmeticMixin
from ..storage import cache
from ..utils import hash_str


class Experiment(ArithmeticMixin):
    """ """
    def __init__(
            self,
            pipeline,
            oof,
            score,
            std,
            description,
            validator,
            feature_list,
            helper_list,
    ):
        self.pipeline = pipeline
        self.model = self.pipeline.models[0].model.model  # TODO: test out
        self.model_name = self.model.__class__.__name__
        self.parameters = self.model.get_params()
        self.models = [model.model.model for model in self.pipeline.models]
        self.featureset = self.pipeline.models[0].model.featureslice.featureset
        self.tie_featuresets()
        self.oof = oof
        self.score = score
        self.std = std
        self.identifier = hash_str(f"{pipeline.__name__}")[:6].upper()
        self.oof.columns = [
            col_name.replace("prediction", self.identifier)
            for col_name in self.oof.columns
        ]
        self.__doc__ = description if description is not None else "no description"
        self.__name__ = f"{self.identifier}-{round(score, 4)}-{pipeline.__name__}"
        self.validator = validator
        self.features = list(feature_list)
        self.helpers = list(helper_list)

    def __str__(self):
        string = f"({round(self.score, 5)}, std:{round(self.std, 3)}: \n\tModel: {self.pipeline.__name__})"
        return string

    def predict(self, df):
        """

        Args:
          df: 

        Returns:

        """
        return self.pipeline.predict(df)

    def __repr__(self):
        fields = {
            "Score":
            f"{round(self.score, 7)}, std: {round(self.std, 7)} ({self.validator.metric.__name__})",
            "Identifier": self.identifier,
            "Description": self.__doc__,
            # 'Model': self.model_name + f'\tx{len(self.models)}',
            # 'Model parameters': self.parameters,
            "Model": f"{self.model.__name__}\t x{len(self.models)}",
            "|- source ": self.model.
            source,  # be careful with refactoring: if you remove this space,
            "FeatureSet": self.featureset.__name__,  #
            "|- description": self.featureset.__doc__,  #
            "|- source": self.featureset.__repr__(
            ),  # both "source" rows will be considered identical
            "Splitter": self.validator.splitter,
        }

        table = tt.Texttable(max_width=80)
        for field in fields:
            table.add_row([field, fields[field]])
        return table.draw()

    def as_dict(self):
        """ """
        fields = {
            "Score": self.score,
            "std": self.std,
            "ID": self.identifier,
            "Model": self.model.__name__,
            "FS": self.featureset.__name__,
            "Description": self.__doc__,
            "FS description": self.featureset.__doc__,
            "Model source": self.model.source,
            "FS source": self.featureset.__repr__(),
            "Splitter": repr(self.validator.splitter),
        }
        for field in fields:
            fields[field] = [fields[field]]
        return fields

    def as_df(self):
        """ """
        return pd.DataFrame(self.as_dict()).set_index("ID")

    def feature_importances(self,
                            plot=False,
                            importance_calculator=BuiltinImportance(),
                            **kw):
        """

        Args:
          plot:  (Default value = False)
          importance_calculator:  (Default value = BuiltinImportance())
          **kw: 

        Returns:

        """
        if plot:
            return plot_importances(self,
                                    calculator=importance_calculator,
                                    **kw)
        res = pd.DataFrame()
        for w_model in pb(self.pipeline.models):
            fsl = w_model.model.featureslice
            model = w_model.model.model
            importances = importance_calculator.calc(model, fsl, self)
            importances = {k: [v] for k, v in importances.items()}
            res = res.append(pd.DataFrame(importances), ignore_index=True)
        return res

    def set_df(self, df_input):
        """

        Args:
          df_input: 

        Returns:

        """
        self.tie_featuresets()
        self.featureset.set_df(df_input)

    def tie_featuresets(self):
        """ """
        for i in range(len(self.pipeline.models)):
            self.pipeline.models[
                i].model.featureslice.featureset = self.featureset


class ExperimentList(MutableSequence):
    """ """
    def __init__(self):
        self.experiments = []
        self.name_to_idx = dict()

    def recalc(self):
        """ """
        self.experiments = []
        self.name_to_idx = dict()
        names = [obj for obj in cache.cached_objs() if obj.endswith("_exp")]
        for idx, name in enumerate(names):
            # print(idx, name)
            experiment = cache.load_obj(name)
            self.experiments.append(experiment)
            self.name_to_idx[experiment.__name__] = idx
        self.experiments.sort(key=lambda e: e.score, reverse=True)

    def __getitem__(self, item):
        """
        Implements calling to experiments by score, name and index
        :param item: str(name) or float(score), slice(score range or index range)
        :return: experiment or list of experiments
        """
        raise DeprecationWarning("Use kts.lb, kts.experiments is deprecated")
        self.recalc()
        if isinstance(item, str):
            if bool(re.match("[0-9A-F]{6}", item)):
                ans = [
                    experiment for experiment in self.experiments
                    if "identifier" in dir(experiment)
                    and experiment.identifier == item
                ]
            else:
                ans = [
                    experiment for experiment in self.experiments
                    if experiment.__name__.count(item) > 0
                ]
        elif isinstance(item, float):
            mul = 10**len(str(item).split(".")[1])
            ans = [
                experiment for experiment in self.experiments
                if int(experiment.score * mul) == int(item * mul)
            ]
        elif isinstance(item, int):
            return self.experiments[item]
        elif isinstance(item, slice):
            if type(item.start) == float:
                ans = [
                    experiment for experiment in self.experiments
                    if item.start <= experiment.score
                    and experiment.score < item.stop
                ]
            else:
                return self.experiments[item]
        else:
            raise TypeError("Item must be of str, number or slice type")

        if len(ans) > 1:
            return ans
        elif len(ans) == 1:
            return ans[0]
        else:
            return

    def __repr__(self):
        raise DeprecationWarning("Use kts.lb, kts.experiments is deprecated")
        self.recalc()
        string = ("Experiments: [\n" + "\n".join(
            [experiment.__str__() for experiment in self.experiments]) + "\n]")
        return string

    def __delitem__(self, key):
        raise AttributeError("This object is read-only")

    def __setitem__(self, key, value):
        raise AttributeError("This object is read-only")

    def insert(self, key, value):
        """

        Args:
          key: 
          value: 

        Returns:

        """
        raise AttributeError("This object is read-only")

    def register(self, experiment):
        """

        Args:
          experiment: 

        Returns:

        """
        cache.cache_obj(experiment, experiment.__name__ + "_exp")

    def __len__(self):
        raise DeprecationWarning("Use kts.lb, kts.experiments is deprecated")
        self.recalc()
        return len(self.experiments)


experiment_list = ExperimentList()
