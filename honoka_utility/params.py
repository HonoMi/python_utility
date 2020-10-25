from dataclasses import dataclass
import json

from typed_json_dataclass import TypedJsonMixin


"""json
{
  "params": {
    "skip": false,
    "replace": false,
    "sources": {
      "redshift": {
        "host": "dw1-rs-stg-mktpf-jp.cbve6tkzvddi.ap-northeast-1.redshift.amazonaws.com",
        "database": "mktpf",
        "port": 5439,
        "user": "etl",
        "schema_name": "datainfra_test",
        "tables": {
          "retarget_lists": {
            "name": "retarget_lists_v3",
            "has_new": true
          },
          "retarget_elements_0": {
            "name": "retarget_elements_0_v3",
            "has_stage": true
          },
          "retarget_elements_1": {
            "name": "retarget_elements_1_v3",
            "has_stage": true
          }
        }
      },
      "s3_po": {
        "bucket": "etl-tmp-pp-stg-mktpf-jp",
        "region": "ap-northeast-1",
        "retarget_lists_key_prefix": "retarget_lists"
      },
      "s3_pp": {
        "bucket": "etl-tmp-pp-stg-mktpf-jp",
        "region": "ap-northeast-1",
        "log_key_prefix": "logs/tm2/rcor/",
        "job_datetime": "1990/07/19/14",
        "jsonpaths_key": "retarget/transform_format/stage_rcor.json"
      },
      "s3_rs": {
        "bucket": "etl-tmp-pp-stg-mktpf-jp",
        "region": "ap-northeast-1",
        "retarget_lists_object_key": "pigimarutty/local_retarget_lists.tsv",
        "retarget_lists_with_s3_updated_at_object_key_out": "pigimarutty/local_out_retarget_lists_with_s3_updated_at.tsv",
        "retarget_lists_with_s3_updated_at_object_key_in": "pigimarutty/local_in_retarget_lists_with_s3_updated_at.tsv"
      }
    }
  }
}
"""


class ParameterError(ValueError):
    pass


class UsageError(ValueError):
    pass


@dataclass
class Table(TypedJsonMixin):  # type: ignore
    name: str
    has_new: bool = False
    has_stage: bool = False
    suffix: str = '_v3'

    def __post_init__(self) -> None:
        if not self.name.endswith(self.suffix):
            raise ParameterError("The table name does not have the correct suffix!!")

    @property
    def new(self) -> str:
        """対象テーブルを1から作り直してあとでrenameするパターンのときに使う一時テーブルのテーブル名"""
        if not self.has_new:
            raise UsageError("This table is not supposed to have _new_ table.")
        return f'_new_{self.name}'

    @property
    def stage(self) -> str:
        """新規データをstageテーブルにまとめてから、後で一気にinsertするパターンの時に使う、stageテーブル名
        """
        if not self.has_stage:
            raise UsageError("This table is not supposed to have _stage_ table.")
        return f'_stage_{self.name}'

    @property
    def tmp(self) -> str:
        """localでの統合テストのために作る一時的なテーブル名"""
        return f'_tmp_{self.name}'

    def __str__(self) -> str:
        """テーブル名取得時に.nameを省略してもいいように"""
        return self.name


@dataclass
class Tables(TypedJsonMixin):  # type: ignore
    retarget_lists: Table
    retarget_elements_0: Table
    retarget_elements_1: Table


@dataclass
class Redshift(TypedJsonMixin):  # type: ignore
    host: str
    database: str
    port: int
    user: str
    schema_name: str
    tables: Tables


@dataclass
class S3(TypedJsonMixin):  # type: ignore
    bucket: str
    region: str


@dataclass
class S3PO(S3):
    retarget_lists_key_prefix: str


@dataclass
class S3PP(S3):
    log_key_prefix: str
    job_datetime: str  # e.g. 1990/07/19/14
    # crois workflowでは $(job_datetime, hours=-1, format=%Y/%m/%d/%H) と指定する想定
    jsonpaths_key: str


@dataclass
class S3RS(S3):
    retarget_lists_object_key: str
    retarget_lists_with_s3_updated_at_object_key_out: str
    retarget_lists_with_s3_updated_at_object_key_in: str

    def __post_init__(self) -> None:
        if (self.retarget_lists_with_s3_updated_at_object_key_out
                != self.retarget_lists_with_s3_updated_at_object_key_in):
            print("Warning: S3Rs.retarget_lists_with_s3_updated_at_object_keys are"
                  "supposed to be matched unless the local execution.")


@dataclass
class Sources(TypedJsonMixin):  # type: ignore
    redshift: Redshift
    s3_po: S3PO
    s3_pp: S3PP
    s3_rs: S3RS


@dataclass
class Params(TypedJsonMixin):  # type: ignore
    skip: bool  # queryを投げずに簡単な動作確認をする場合
    replace: bool  # trueの場合既存テーブルを上書きしてしまう (定期実行ではtrue, debug時はfalse)
    sources: Sources


def load() -> Params:
    with open('/work/order/config.json') as f:
        params_dict = json.load(f)['params']
        params: Params = Params.from_dict(params_dict)
    return params
