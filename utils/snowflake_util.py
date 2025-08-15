import random
import time

import short_unique_id as suid

"""
生成一个不重复（百分之99.99的情况不重复）且递增的id
"""


class SnowflakeIDGenerator:
    @staticmethod
    def generate_id():
        return str(suid.get_next_snowflake_id())
