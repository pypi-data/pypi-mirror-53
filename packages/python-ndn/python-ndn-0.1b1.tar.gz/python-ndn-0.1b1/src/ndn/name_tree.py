import asyncio as aio
from pygtrie import Trie
from typing import List, Optional, Tuple
from .encoding import InterestParam, FormalName, MetaInfo, BinaryStr
from .types import InterestNack, ValidationFailure, Validator, Route


class NameTrie(Trie):
    def _path_from_key(self, key: FormalName) -> FormalName:
        # bytes(x) will copy x if x is memoryview or bytearray but will not copy bytes
        return [x if isinstance(x, memoryview) and x.readonly else bytes(x)
                for x in key]

    def _key_from_path(self, path: FormalName) -> FormalName:
        return path


class InterestTreeNode:
    pending_list: List[Tuple[aio.Future, int, bool, bool]] = None
    validator: Optional[Validator] = None

    def __init__(self):
        self.pending_list = []

    def append_interest(self, future: aio.Future, param: InterestParam):
        self.pending_list.append((future, param.lifetime, param.can_be_prefix, param.must_be_fresh))

    def nack_interest(self, nack_reason: int) -> bool:
        for future, _, _, _ in self.pending_list:
            future.set_exception(InterestNack(nack_reason))
        return True

    def satisfy(self, name: FormalName, meta_info: MetaInfo, content: Optional[BinaryStr], is_prefix: bool) -> bool:
        exact_match_interest = False
        for future, _, can_be_prefix, _ in self.pending_list:
            if can_be_prefix or not is_prefix:
                future.set_result((name, meta_info, content))
            else:
                exact_match_interest = True
        if exact_match_interest:
            self.pending_list = [ele for ele in self.pending_list if not ele[2]]
            return False
        else:
            return True

    def invalidate(self, name: FormalName, meta_info: MetaInfo, content: Optional[BinaryStr]) -> bool:
        for future, _, _, _ in self.pending_list:
            future.set_exception(ValidationFailure(name, meta_info, content))
        return True

    def timeout(self, future: aio.Future):
        self.pending_list = [ele for ele in self.pending_list if ele[0] is not future]
        return not self.pending_list

    def cancel(self):
        for future, _, _, _ in self.pending_list:
            future.cancel()


class PrefixTreeNode:
    callback: Route = None
    validator: Optional[Validator] = None
