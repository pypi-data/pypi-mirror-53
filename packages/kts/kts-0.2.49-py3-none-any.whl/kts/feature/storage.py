from .. import config
from ..storage import source_utils
from ..storage import cache_utils
from ..storage import caching
from ..storage import dataframe
from ..utils import captcha
from .selection.selector import BuiltinImportance
import glob
import os
import pandas as pd
import numpy as np
import inspect
from typing import Optional, Union, List, Tuple, Dict, Any


class FeatureConstructor:
    def __init__(self, function, cache_default=True, stl=False):
        self.function = function
        self.cache_default = cache_default
        self.__name__ = function.__name__
        self.source = source_utils.get_source(function)
        self.stl = stl
        self.args = dict()

    # needs refactoring because of direct storing source
    def __call__(self, df, cache=None, **kwargs):
        if not self.stl:
            self = caching.cache.load_obj(self.__name__ + '_fc')
        ktdf = dataframe.DataFrame(df=df)
        if type(cache) == type(None):
            cache = self.cache_default
        if not cache or config.preview_call:  # written to avoid caching when @preview function uses @registered function inside
            return self.function(ktdf, **kwargs)

        name = f"{self.function.__name__}__{cache_utils.get_hash_df(ktdf)[:4]}__{ktdf.slice_id[-4:]}"
        name_metadata = name + "_meta"
        if caching.cache.is_cached_df(name):
            if caching.cache.is_cached_obj(name_metadata):
                cached_encoders = caching.cache.load_obj(name_metadata)
                for key, value in cached_encoders.items():
                    ktdf.encoders[key] = value
            return dataframe.DataFrame(df=caching.cache.load_df(name), train=ktdf.train, encoders=ktdf.encoders, slice_id=ktdf.slice_id)
        else:
            result = self.function(ktdf)
            try:
                caching.cache.cache_df(result, name)
            except MemoryError:
                print(f'The dataframe is too large to be cached. '
                      f'It is {cache_utils.get_df_volume(result)}, '
                      f'but current memory limit is {config.memory_limit}.')
                print(f'Setting memory limit to {cache_utils.get_df_volume(result) * 2}')
                ans = input('Please confirm memory limit change. Enter "No" to cancel it.')
                do_change = True
                if ans.lower() == 'no':
                    if captcha():
                        do_change = False
                if do_change:
                    caching.cache.set_memory_limit(cache_utils.get_df_volume(result) * 2)
                    caching.cache.cache_df(result, name)
                    print("Done. Please don't forget to update your kts_config.py file.")
                else:
                    print('Cancelled')
            if ktdf.encoders:
                caching.cache.cache_obj(ktdf.encoders, name_metadata)
            return dataframe.DataFrame(df=result, train=ktdf.train, encoders=ktdf.encoders, slice_id=ktdf.slice_id)

    def __repr__(self):
        if self.stl:
            return self.source
        else:
            return f'<Feature Constructor "{self.__name__}">'

    def __str__(self):
        return self.__name__

    def __sub__(self, other):
        assert isinstance(other, list)
        from . import stl
        return stl.compose([self, stl.column_dropper(other)])

    def __add__(self, other):
        assert isinstance(other, list)
        from . import stl
        return stl.compose([self, stl.column_selector(other)])

    def __mul__(self, other):
        assert isinstance(other, FeatureConstructor)
        from . import stl
        return stl.compose([self, other])

FeatureListType = Union[FeatureConstructor, List[FeatureConstructor], Tuple[FeatureConstructor], List["FeatureListType"], Tuple["FeatureListType"]]

from . import stl


class FeatureSet:
    def __init__(self,
                 fc_before: FeatureListType,
                 fc_after: FeatureListType = stl.empty_like,
                 df_input: Optional[pd.DataFrame] = None,
                 target_columns: Optional[Union[List[str], str]] = None,
                 auxiliary_columns: Optional[Union[List[str], str]] = None,
                 name: Optional[str] = None,
                 description: Optional[str] = None,
                 desc: Optional[str] = None,
                 encoders: Optional[Dict[str, Any]] = None):
        if type(fc_before) == list:
            self.fc_before = stl.concat(fc_before)
        elif type(fc_before) == tuple:
            self.fc_before = stl.compose(fc_before)
        else:
            self.fc_before = fc_before
        if type(fc_after) == list:
            self.fc_after = stl.concat(fc_after)
        elif type(fc_after) == tuple:
            self.fc_after = stl.compose(fc_after)
        else:
            self.fc_after = fc_after
        self.target_columns = target_columns
        if isinstance(self.target_columns, str):
            self.target_columns = [self.target_columns]
        elif self.target_columns is None:
            self.target_columns = []
        self.auxiliary_columns = auxiliary_columns
        if isinstance(self.auxiliary_columns, str):
            self.auxiliary_columns = [self.auxiliary_columns]
        elif self.auxiliary_columns is None:
            self.auxiliary_columns = []
        self.encoders = (encoders if encoders is not None else dict())
        if df_input is not None:
            self.set_df(df_input)
        self._first_name = name
        self.__doc__ = None
        if desc is not None and description is not None:
            raise ValueError("desc is an alias of description. You can't use both")
        if description is not None:
            self.__doc__ = description
        elif desc is not None:
            self.__doc__ = desc
        self.altsource = None

    def set_df(self, df_input):
        self.df_input = dataframe.DataFrame(df=df_input)
        self.df_input.train = True
        self.df_input.encoders = self.encoders
        self.df = self.fc_before(self.df_input)

    def __call__(self, df):
        ktdf = dataframe.DataFrame(df=df)
        ktdf.encoders = self.encoders
        return stl.merge([
            self.fc_before(ktdf),
            self.fc_after(ktdf)
        ])

    def __getitem__(self, idx):
        if isinstance(self.df_input, type(None)):
            raise AttributeError("Input DataFrame is not defined")
        return stl.merge([
            self.df.iloc[idx],
            self.fc_after(dataframe.DataFrame(df=self.df_input.iloc[idx], train=1))  # BUG: should have .train=True?
        ])  # made .train=1 only for preview purposes
        # actually, FS[a:b] functionality is made only for debug
        # why not write config.preview_call = 1 then?

    def empty_copy(self):
        res = FeatureSet(fc_before=self.fc_before,
                        fc_after=self.fc_after,
                        target_columns=self.target_columns,
                        auxiliary_columns=self.auxiliary_columns,
                        encoders=self.encoders,
                        name=self.__name__,
                        description=self.__doc__)
        res.altsource = self.altsource
        return res

    def slice(self, idx_train, idx_test):
        return FeatureSlice(self, idx_train, idx_test)

    @property
    def target(self):
        if len(self.target_columns) > 0:
            if set(self.target_columns) < set(self.df_input.columns):
                return self.df_input[self.target_columns]
            elif set(self.target_columns) < set(self.df_input.columns):
                return self.df[self.target_columns]
            else:
                raise AttributeError("Target columns are neither given as input nor computed")
        else:
            raise AttributeError("Target columns are not defined.")

    @property
    def auxiliary(self):
        if len(self.auxiliary_columns) > 0:
            if set(self.auxiliary_columns) < set(self.df_input.columns):
                return self.df_input[self.auxiliary_columns]
            elif set(self.auxiliary_columns) < set(self.df_input.columns):
                return self.df[self.auxiliary_columns]
            else:
                raise AttributeError("Auxiliary columns are neither given as input nor computed")
        else:
            raise AttributeError("Auxiliary columns are not defined.")

    @property
    def aux(self):
        return self.auxiliary

    def __get_src(self, fc):
        if fc.__name__ == 'empty_like':
            return 'stl.empty_like'
        if not isinstance(fc, FeatureConstructor):
            return source_utils.get_source(fc)
        if fc.stl:
            return fc.source
        else:
            return fc.__name__

    def _source(self, short=True):
        fc_before_source = self.__get_src(self.fc_before)
        fc_after_source = self.__get_src(self.fc_after)
        if short:
            fc_before_source = source_utils.shorten(fc_before_source)
            fc_after_source = source_utils.shorten(fc_after_source)
        prefix = 'FeatureSet('
        fs_source = prefix + 'fc_before=' + fc_before_source + ',\n' \
                    + ' ' * len(prefix) + 'fc_after=' + fc_after_source + ',\n' \
                    + ' ' * len(prefix) + 'target_columns=' + repr(self.target_columns) + ', auxiliary_columns=' + repr(self.auxiliary_columns if 'auxiliary_columns' in dir(self) else None) + ')'
        return fs_source

    @property
    def source(self):
        return self._source(short=False)

    def recover_name(self):
        if self._first_name:
            return self._first_name
        ans = []
        frame = inspect.currentframe()
        tmp = {}
        for i in range(7):
            try:
                tmp = {**tmp, **frame.f_globals}
            except:
                pass
            try:
                frame = frame.f_back
            except:
                pass

        for k, var in tmp.items():
            if isinstance(var, self.__class__):
                if hash(self) == hash(var) and k[0] != '_':
                    ans.append(k)
        if len(ans) != 1:
            print(f"The name cannot be uniquely defined. Possible options are: {ans}. Choosing {ans[0]}. You can set the name manually via FeatureSet(name=...) or using .set_name(...)")
        self._first_name = ans[0]
        return self._first_name

    @property
    def __name__(self):
        return self.recover_name()

    def set_name(self, name):
        self._first_name = name

    def __repr__(self):
        if 'altsource' in self.__dict__ and self.altsource is not None:
            return self.altsource
        else:
            return self._source(short=True)

    def select(self, n_best, experiment, calculator=BuiltinImportance(), mode='max'):
        good_features = list(experiment.feature_importances(importance_calculator=calculator).agg(mode).sort_values(ascending=False).head(n_best).index)
        res = FeatureSet(fc_before=self.fc_before + good_features,
                         fc_after=self.fc_after + good_features,
                         df_input=self.df_input,
                         target_columns=self.target_columns,
                         auxiliary_columns=self.auxiliary_columns,
                         encoders=self.encoders,
                         name=f"{self.__name__}_{calculator.short_name}_{n_best}",
                         description=f"Select {n_best} best features from {self._first_name} using {calculator.__class__.__name__}")
        res.altsource = self.__repr__() + f".select({n_best}, lb['{experiment.identifier}'], {calculator.__repr__()})"
        return res


class FeatureSlice:
    def __init__(self, featureset, slice, idx_test):
        self.featureset = featureset
        self.slice = slice
        self.idx_test = idx_test
        self.slice_id = cache_utils.get_hash_slice(slice)
        self.first_level_encoders = self.featureset.encoders
        self.second_level_encoders = {}
        self.columns = None
        # self.df_input = copy(self.featureset.df_input)

    def __call__(self, df=None):
        if isinstance(df, type(None)):
            fsl_level_df = dataframe.DataFrame(df=self.featureset.df_input.iloc[self.slice],
                                               # ALERT: may face memory leak here
                                               slice_id=self.slice_id,
                                               train=True,
                                               encoders=self.second_level_encoders)
            result = stl.merge([
                self.featureset.df.iloc[self.slice],
                self.featureset.fc_after(fsl_level_df)
            ])
            self.columns = [i for i in result.columns if i not in self.featureset.target_columns \
                                                     and i not in self.featureset.auxiliary_columns]
            return result[self.columns]
        elif isinstance(df, slice) or isinstance(df, np.ndarray) or isinstance(df, list):
            fsl_level_df = dataframe.DataFrame(df=self.featureset.df_input.iloc[df],  # ALERT: may face memory leak here
                                               slice_id=self.slice_id,
                                               train=False,
                                               encoders=self.second_level_encoders)
            result = stl.merge([
                self.featureset.df.iloc[df],
                self.featureset.fc_after(fsl_level_df)
            ])
            for column in set(self.columns) - set(result.columns):
                result[column] = 0
            return result[self.columns]
        else:
            fs_level_df = dataframe.DataFrame(df=df,
                                              encoders=self.first_level_encoders)
            fsl_level_df = dataframe.DataFrame(df=df,
                                               encoders=self.second_level_encoders,
                                               slice_id=self.slice_id)
            result = stl.merge([
                self.featureset.fc_before(fs_level_df),  # uses FeatureSet-level encoders
                self.featureset.fc_after(fsl_level_df)  # uses FeatureSlice-level encoders
            ])
            for column in set(self.columns) - set(result.columns):
                result[column] = 0
            return result[self.columns]

    @property
    def target(self):
        return self.featureset.target.iloc[self.slice]

    def compress(self):
        self.featureset = self.featureset.empty_copy()


from collections import MutableSequence


class FeatureList(MutableSequence):
    def __init__(self):
        self.full_name = "kts.feature.storage.feature_list"  # such a hardcode
        self.names = [self.full_name]
        while self.names[-1].count('.'):
            self.names.append(self.names[-1][self.names[-1].find('.') + 1:])
        self.names.append('kts.features')
        while self.names[-1].count('.'):
            self.names.append(self.names[-1][self.names[-1].find('.') + 1:])
        self.functors = []
        self.name_to_idx = dict()

    def recalc(self):
        self.functors = []
        self.name_to_idx = dict()
        names = [obj for obj in caching.cache.cached_objs() if obj.endswith('_fc')]
        for idx, name in enumerate(names):
            functor = caching.cache.load_obj(name)
            self.functors.append(functor)
            self.name_to_idx[functor.__name__] = idx

    def __repr__(self):
        self.recalc()
        string = f"[{', '.join([f.__str__() for f in self.functors])}]"
        return string

    def __getitem__(self, key):
        self.recalc()
        if type(key) in [int, slice]:
            return self.functors[key]
        elif type(key) == str:
            return self.functors[self.name_to_idx[key]]
        else:
            raise TypeError('Index should be int, slice or str')

    def __delitem__(self, key):
        raise AttributeError('This object is read-only')

    def __setitem__(self, key, value):
        raise AttributeError('This object is read-only')

    def insert(self, key, value):
        raise AttributeError('This object is read-only')

    def define_in_scope(self, global_scope):
        self.recalc()
        for func in self.name_to_idx:
            for name in self.names:
                try:
                    exec(f"{func} = {name}['{func}']", global_scope)
                    break
                except BaseException:
                    pass

    def __len__(self):
        self.recalc()
        return len(self.functors)


feature_list = FeatureList()
