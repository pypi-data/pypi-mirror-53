"""Handle the commandline, perform the archiving and creating the release notes"""
from configargparse import ArgumentParser
from trello_release_notes.trello_release_notes import Trellist


def main():
    """Run through and execute the archiving"""
    parser = get_arg_parser()
    args = parser.parse_args()
    t = Trellist(
        args.apikey,
        args.apisecret,
        args.boardname,
        args.done_list,
        args.releases,
        args.create_empty_release,
    )
    t.run()


def get_arg_parser():
    parser = ArgumentParser(
        default_config_files=["~/.trello_release_settings.ini"],
        description="A tool to archive what you've done in trello to a release like Alice Goldfuss does",
    )
    parser.add_argument(
        "-c",
        "--config",
        is_config_file=True,
        help="A path to a config file for these options. The default is ~/.trello_release_settings.ini",
    )
    parser.add_argument(
        "--apikey",
        help="Your apikey for trello. Do not pass on the command line regularly, people can see this in your system.\
        Best to also store this in the config file.",
    )
    parser.add_argument(
        "--apisecret",
        help="Your secret token. Do not pass on the command line regularly, people can see this in your system.\
        Best to also store this in the config file.",
    )
    parser.add_argument(
        "--boardname", help="Name of the board we want to archive from."
    )
    parser.add_argument(
        "-d", "--done_list", help="Name of the list we want to archive from."
    )
    parser.add_argument(
        "-r", "--releases", help="Name of the list we want to archive to."
    )
    parser.add_argument(
        "-z",
        "--create_empty_release",
        action="store_true",
        help="specify if you want to create a release even if nothing got done",
    )
    return parser


if __name__ == "__main__":
    main()
