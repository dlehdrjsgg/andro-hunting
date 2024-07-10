# main.py
from modules.run import multiRun
from modules.file_handler.text import readText


def main():
    al = readText("applist.txt")
    # al = ["com.glyde.app.android"]
    multiRun(al)


if __name__ == "__main__":
    # if len(sys.argv) != 2:
    #     print("Usage: python main.py <package_name>")
    #     sys.exit(1)

    # package_name = sys.argv[1]
    main()
