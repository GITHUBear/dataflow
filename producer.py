import logging
import random
from typing import List, Tuple
import time
from filelock import FileLock

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class DataProducer:
    def __init__(
        self, 
        name: str,
        data: List[Tuple[float, float]], 
        file: str,
        miu_interval: int,
        delta_interval: int, 
    ):
        if delta_interval > miu_interval:
            raise ValueError("delta_interval must less than miu_interval")
        
        self.name = name
        self.data = data
        self.file = file
        self.miu_interval = miu_interval
        self.delta_interval = delta_interval
    
    def product(self):
        for (x, y) in self.data:
            delta = random.randint(-self.delta_interval, self.delta_interval)
            time.sleep((self.miu_interval + delta) / 1000.0)
            with open(self.file, 'w') as file:
                file.write(f"{x} {y}\n")
            print(f"process-{self.name}: write ({x}, {y}) to {self.file}")
                
