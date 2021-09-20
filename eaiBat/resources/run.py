import argparse
import logging
import sys

from behave.__main__ import main as behave_main


def main():
    """
    Run behave with a log rolling.
    As default create output.html report, a plain text plain_output.txt and JUnit report files in
    junit_report folder.

    By default run in non debug mode.

    Controls the run behaviour using tags and other sets
    :return: 0 if everything is fine, 1 or number of Assertion Failed found in plain_output.txt
    """
    # Prepare run
    logging.getLogger(__name__).debug("Preparing run")
    description = ""
    # Get options from command line input
    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-t",
                        "--tags",
                        type=str,
                        help="The scenario tags to run",
                        action="append",
                        nargs='+')
    parser.add_argument("--debug",
                        help="Set the logs to debug. Otherwise the logs are at warning level ",
                        action="store_true")
    parser.add_argument("--display",
                        help=("Display the html report after the "
                              "execution using the default browser"),
                        action="store_true")
    parser.add_argument("-e",
                        "--environment",
                        type=str,
                        help="AHEAD environment",
                        default="localhost")
    parser.add_argument("-b",
                        "--browser",
                        type=str,
                        help="The browser you want to use for running test on",
                        choices=["chrome", "headless-chrome", "headless-chromium", "firefox", "edge"],
                        default="chrome")
    args = parser.parse_args()
    behave_arguments = ["./features",
                        "-fhtml",
                        "-ooutput.html",
                        "-fplain",
                        "-oplain_output.txt",
                        "-fallure",
                        "-oallure_report",
                        "--no-capture",
                        f"-DmodeDebug={args.debug}",
                        f"-Denvironment={args.environment}",
                        f"-Dbrowser={args.browser}"]

    if args.tags:
        for tags in args.tags:
            behave_arguments.append("-t {}".format("".join(tags)))

    value = behave_main(behave_arguments)

    # Result management: return value is 0 if everything is fine
    # 1 or the number of 'Assertion Failed' found in the plain text output
    results = 0
    sys.exit(value if results == 0 else results)


if __name__ == "__main__":
    main()
