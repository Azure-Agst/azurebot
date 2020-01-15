import os
import time
import sys
from datetime import datetime

if not os.path.exists("out"):
    os.makedirs("out")

while 1:
    logname = datetime.now().strftime("%d-%m-%Y_%H.%M.%S")
    os.system(f"python3 azurebot.py > ./out/{logname}.txt")
    try:
        time.sleep(0.5)  # 200ms to CTR+C twice
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)
