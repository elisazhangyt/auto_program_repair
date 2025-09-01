from typing import List, Tuple

class InfoDict:
    def __init__(self):
        self.info_dict = {}

    def create_info_dict(self, agent_role: str, agent_task: str, bug_locations: List[Tuple[str, List[Tuple[int, int]]]]):
        self.add_info("agent role", agent_role)
        self.add_info("agent task", agent_task)
        self.add_info("bug files and locations", bug_locations)

    def add_info(self, info_type, info):
        self.info_dict[info_type] = info

    def get_info(self, info_type):
        return self.info_dict[info_type]

