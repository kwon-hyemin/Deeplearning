# context, fname, train, test, id, label
import json
from dataclasses import dataclass
from abc import *
import pandas as pd
import googlemaps
from typing import TypeVar

PandasDataFrame = TypeVar('pandas.core.frame.DataFrame')
GooglemapsClient = TypeVar('googlemaps.Client')


@dataclass
class Dataset:
    dname: str
    sname: str
    fname: str
    train: str
    test: str
    id: str
    label: str

    @property
    def dname(self) -> str: return self._dname

    @dname.setter
    def dname(self, dname): self._dname = dname

    @property
    def sname(self) -> str: return self._sname

    @sname.setter
    def sname(self, sname): self._sname = sname

    @property
    def fname(self) -> str: return self._fname

    @fname.setter
    def fname(self, fname): self._fname = fname

    @property
    def train(self) -> str: return self._train

    @train.setter
    def train(self, train): self._train = train

    @property
    def test(self) -> str: return self._test

    @test.setter
    def test(self, test): self._test = test

    @property
    def id(self) -> str: return self._id

    @id.setter
    def id(self, id): self._id = id

    @property
    def label(self) -> str: return self._label

    @label.setter
    def label(self, label): self._label = label


@dataclass
class File(object):
    context: str
    fname: str
    dframe: object

    @property
    def context(self) -> str: return self._context

    @context.setter
    def context(self, context): self._context = context

    @property
    def fname(self) -> str: return self._fname

    @fname.setter
    def fname(self, fname): self._fname = fname

    @property
    def dframe(self) -> str: return self._dframe

    @dframe.setter
    def dframe(self, dframe): self._dframe = dframe


class PrinterBase(metaclass=ABCMeta):
    @abstractmethod
    def dframe(self):
        pass
    # new_file, csv, xls, json


class ReaderBase(metaclass=ABCMeta):
    @abstractmethod
    def new_file(self, file) -> str:
        pass

    @abstractmethod
    def csv(self) -> object:
        pass

    @abstractmethod
    def xls(self) -> object:
        pass

    @abstractmethod
    def json(self) -> object:
        pass


# Reader
# Printer
class Reader(ReaderBase):
    def new_file(self, file) -> str:
        return file.context + file.fname

    # file.context = './data/'
    # file.fname = 'cctv_in_seoul'
    # file 객체에 있는 context와 fname이 필요하다.

    def csv(self, path: str) -> PandasDataFrame:
        o = pd.read_csv(f'{self.new_file(path)}', encoding='UTF-8', thousands=',')
        print(f'type: {type(o)}')
        return o

    def xlsx(self, file, header) -> str:
        return pd.read_excel(f'{self.new_file(file)}.xlsx', header=header)

    def xls(self, path: str, header: str, cols: str, skiprows) -> PandasDataFrame:
        return pd.read_excel(f'{self.new_file(path)}.xls', header=header, usecols=cols, skiprows=skiprows)

    def json(self, path: str) -> PandasDataFrame:
        return pd.read_json(f'{self.new_file(path)}.json', encoding='UTF-8')

    def map_json(self, path: str) -> object:
        return json.load(open(f'{self.new_file(path)}.json', encoding='UTF-8'))

    @staticmethod
    def gmaps() -> GooglemapsClient:
        a = googlemaps.Client(key='')
        print(type(a))
        return a

    def myprint(self, this):
        print('*' * 100)
        print(f'1. Target type \n {type(this)} ')
        print(f'2. Target column \n {this.columns} ')
        print(f'3. Target top 1개 행\n {this.head(1)} ')
        print(f'4. Target bottom 1개 행\n {this.tail(1)} ')
        print(f'4. Target null 의 갯수\n {this.isnull().sum()}개')
        print('*' * 100)
