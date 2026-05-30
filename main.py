import sys
from app import AutoClickerApp

def main():
    try:
        app = AutoClickerApp()
        app.mainloop()
    except KeyboardInterrupt:
        print("Application interrupted.")
        sys.exit(0)

if __name__ == "__main__":
    main()
