import logging
from datetime import datetime
from typing import Any

_v0_API_KEY_FOR_PAY = "for_pay"
_v1_API_KEY_FOR_PAY = "ppvz_for_pay"
_API_KEYS_FOR_PAY = {_v0_API_KEY_FOR_PAY, _v1_API_KEY_FOR_PAY}
_API_KEY_OPERATION = "supplier_oper_name"
_API_VALUE_OPERATION_DELIVERY = "Логистика"
_API_VALUE_OPERATION_FINE = "Штраф МП"
_API_VALUE_OPERATION_SALE = "Продажа"
_API_VALUE_OPERATION_REFUND = "Возврат"
_API_OPERATIONS_WITHOUT_PAY = [
    _API_VALUE_OPERATION_DELIVERY,
    _API_VALUE_OPERATION_FINE,
]

API_OPERATIONS_SALE_REFUND_DELIVERY_FINE: list[str] = [
    _API_VALUE_OPERATION_SALE,
    _API_VALUE_OPERATION_REFUND,
    _API_VALUE_OPERATION_DELIVERY,
    _API_VALUE_OPERATION_FINE
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
map_versions = {
    1: map_v1,
    0: map_v0
}


class Transformer:
    @classmethod
    def transform(cls, data: dict, api_key: str) -> dict:
        defaults = dict(api_version=None, document=data, api_key=api_key)

        for ver, map_v in map_versions.items():
            try:
                versioned = cls._get_mapped(data, map_default | map_v)
                versioned["created"] = (
                    (created := versioned["created"])
                    and datetime.strptime(created, "%Y-%m-%dT%H:%M:%SZ")
                )
                return defaults | versioned | dict(api_version=ver)
            except KeyError:
                continue

        logging.error("New WB API version")

        return defaults

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
