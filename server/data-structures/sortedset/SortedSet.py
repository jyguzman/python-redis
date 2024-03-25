from typing import List, Dict
from SkipList import SkipList

class SortedSet:
    def __init__(self):
        self.list = SkipList()
        self.members = {}

    def add(self, member: str, score: float) -> None:
        if member in self.members:
            self.list.delete(member)
        self.members[member] = score
        self.list.insert(member, score)

    def get(self, member: str) -> Dict[str, int] | None:
        if member in self.members:
            return {member: self.members[member]}
        return None

    def remove(self, member: str) -> None:
        if member not in self.members:
            return
        self.list.delete(member)
        del self.members[member]

    def range(self, min_score: float, max_score: float) -> List[str]:
        return self.list.query_range(min_score, max_score)

if __name__ == "__main__":
    pass
