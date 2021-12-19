import logging
from datetime import datetime
from typing import Any

_v0_API_KEY_FOR_PAY = "for_pay"
_v1_API_KEY_FOR_PAY = "ppvz_for_pay"
_API_KEYS_FOR_PAY = {_v0_API_KEY_FOR_PAY, _v1_API_KEY_FOR_PAY}
_API_KEY_OPERATION = "supplier_oper_name"
_API_VALUE_OPERATION_LOGISTIC = "Логистика"
_API_VALUE_OPERATION_MULCT = "Штраф МП"
_API_OPERATIONS_WITHOUT_PAY = [
    _API_VALUE_OPERATION_LOGISTIC,
    _API_VALUE_OPERATION_MULCT,
]
map_default = {
    "row_id": "rrd_id",
    "created": "rr_dt",
    "report_list_id": "realizationreport_id",
    "wb_id": "nm_id",
    "name": "sa_name",
    "brand": "brand_name",
    "barcode": "barcode",
    "type": "doc_type_name",
    "operation": _API_KEY_OPERATION,
    "delivery": "delivery_rub",
}
map_v0 = {
    "for_pay": _v0_API_KEY_FOR_PAY,
    "reward": "supplier_reward",
}
map_v1 = {
    "for_pay": _v1_API_KEY_FOR_PAY,
    "reward": "ppvz_reward",
}
map_versions = [map_v0, map_v1]


class Transformer:
    @classmethod
    def transform(cls, data: dict, api_key: str) -> dict:
        defaults = cls._get_mapped(data, map_default)

        for ind, map_v in enumerate(map_versions):
            try:
                versioned = cls._get_mapped(data, map_v)
                break
            except KeyError as e:
                logging.warning(e)
                continue
        else:
            raise KeyError(f"new api versions:\n{data}")

        if defaults["created"]:
            defaults["created"] = datetime.strptime(
                defaults["created"], "%Y-%m-%dT%H:%M:%SZ"
            )

        return defaults | versioned | dict(api_version=ind, document=data, api_key=api_key)

    @classmethod
    def _get_mapped(cls, data: dict, map_v: dict) -> dict:
        return {
            self_key: cls._get_value(data, api_key)
            for self_key, api_key in map_v.items()
        }

    @staticmethod
    def _get_value(data: dict, key: str) -> Any:
        try:
            return data[key]
        except KeyError as e:
            if key in _API_KEYS_FOR_PAY:
                if data[_API_KEY_OPERATION] in _API_OPERATIONS_WITHOUT_PAY:
                    return None
            raise e
