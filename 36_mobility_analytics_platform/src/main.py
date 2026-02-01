from mobility_platform import MobilityPlatformApp

def main():
    app = MobilityPlatformApp()

    try:
        app.run()
    finally:
        app.stop()

if __name__ == "__main__":
    main()
