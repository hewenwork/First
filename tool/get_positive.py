class GetReport:

    def __init__(self, report):
        for line in report.split("\n"):
            print(line)


if __name__ == "__main__":
    report = input(u"put in")
    GetReport(report)