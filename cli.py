import argparse
from opennotify.api import OpenNotify
from config import CLI_DESCRIPTION
from datetime import datetime


class OpenNotifyCLI:
    """A CLI wrapper for the Open Notify API client"""
    def __init__(self):
        self.api = OpenNotify()
        self.parser = argparse.ArgumentParser(
            description=CLI_DESCRIPTION,
        )
        self.add_args()

    def add_args(self):
        """
        Adds arguments to the parser upon initialization
        :return: None
        """
        self.parser.add_argument('arg', choices=['loc', 'people'])

    def run(self):
        """
        Run the CLI and return defined information for the input args
        :return:
        """
        args = self.parser.parse_args()

        # Route args to their correct handler function
        if args.arg == 'loc':
            return self.loc()
        if args.arg == 'people':
            return self.people()

    def loc(self):
        """
        Formats a response from the api.loc() endpoint into and prints a readable string.
        :return: None
        """
        response = self.api.loc()
        position = response['iss_position']
        iss_latitude = position['latitude']
        iss_longitude = position['longitude']
        posix_timestamp = response['timestamp']
        timestamp = datetime.fromtimestamp(posix_timestamp)
        print(f'The ISS current location at {timestamp} is {iss_latitude}, {iss_longitude}')

    def people(self):
        """
        Formats are response from the api.people() endpoint and prints readable strings.
        :return: None
        """
        response = self.api.people()
        people_in_space = response['people']

        crafts = {}
        for person in people_in_space:  # map people to their craft in the event there is more than one craft
            craft = person.get('craft', 'Unknown')  # Mark craft as unknown if person has none listed
            craft_occupants = crafts.setdefault(craft, [])
            craft_occupants.append(person['name'])

        for craft, people in crafts.items():  # Print a line detailing each craft
            names = [name for name in people]
            names = ', '.join(name for name in names)
            print(f"There are {len(people)} people aboard the {craft}. They are {names}")


if __name__ == '__main__':
    cli = OpenNotifyCLI()
    cli.run()
