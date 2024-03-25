from __future__ import annotations
from typing import List, Union
import random
import math


class Node:
    def __init__(self, member: str = '', score: float = -math.inf, level: int = -1):
        self.member = member
        self.score = score
        self.level = level
        self.forward: List = [None] * (self.level + 1)

    def __repr__(self):
        return f'({self.member}: {self.score})'

    def compare(self, member: str, score: float) -> int:
        if self.score < score or (self.score == score and self.member < member):
            return 0
        return 1

    @staticmethod
    def make_header(max_level: int) -> Node:
        header = Node(level=max_level)

        for i in range(max_level):
            header.forward[i] = Node(f's{i}', score=math.inf)

        return header


class SkipList:

    def __init__(self, p: float = 0.5, max_level: int = 16):
        self.p = p
        self.max_level = max_level
        self.curr_max_level = 0
        self.header = Node.make_header(self.max_level)

    def get_random_level(self) -> int:
        curr_level = 0
        while random.uniform(0, 1) <= self.p and curr_level < self.max_level:
            curr_level += 1
        return curr_level

    def search(self, member: str, score: float) -> Node | None:
        x = self.header
        for i in range(self.curr_max_level, -1, -1):
            while x.forward[i].score < score:
                if x.forward[i].member == member:
                    return x.forward[i]
                x = x.forward[i]
        return None

    def query_range(self, min_score: float, max_score: float) -> List[str]:
        x = self.header
        for i in range(self.curr_max_level, -1, -1):
            while x.forward[i] and x.forward[i].score < min_score:
                x = x.forward[i]

        members = []
        while x.forward[0] and min_score <= x.forward[0].score <= max_score:
            members.append(x.forward[0].member)
            x = x.forward[0]
        return members

    def insert(self, member: str, new_score: float) -> None:
        update: List[Node | None] = [None] * self.max_level
        x = self.header
        for i in range(self.curr_max_level, -1, -1):
            while x.forward[i].compare(member, new_score) == 0:
                x = x.forward[i]
            update[i] = x

        level = self.get_random_level()
        if level > self.curr_max_level:
            for i in range(self.curr_max_level + 1, level + 1):
                update[i] = self.header
            self.curr_max_level = level

        new_node = Node(member, new_score, level)
        for i in range(level + 1):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node

    def delete(self, member: str):
        pass

    def display(self) -> None:
        result = ""
        for i in range(self.curr_max_level, -1, -1):
            curr = self.header.forward[i]
            list_string = f"Level {i}: header -> "
            while curr:
                list_string += f"{str(curr)} -> "
                curr = curr.forward[i] if i < len(curr.forward) else None
            list_string += "None"
            result += list_string + '\n'
        print(result)


if __name__ == "__main__":
    sl = SkipList()
    sl.insert('aad', 15)
    sl.insert('aab', 15)
    sl.insert('aac', 15)
    sl.insert('abd', 15)
    sl.insert('acd', 15)
    sl.insert('jordan', 50)
    sl.insert('baaa', 0)
    sl.insert('john', 55)
    sl.insert('joha', 55)
    # sl.insert(20)
    # sl.insert(5)
    # sl.insert(8)
    # sl.insert(15)
    # print(sl.search(8))
    # print(sl.layers)
    sl.display()
    print(sl.query_range(-math.inf, 15))
