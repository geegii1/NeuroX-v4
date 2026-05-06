import time
from system.controller import NeuroXController

# how often to run (seconds)
INTERVAL = 3600   # 1 hour

def main():
    while True:
        try:
            NeuroXController().run()
        except Exception as e:
            print(f"[ERROR] {e}")

        print(f"\nSleeping for {INTERVAL} seconds...\n")
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
