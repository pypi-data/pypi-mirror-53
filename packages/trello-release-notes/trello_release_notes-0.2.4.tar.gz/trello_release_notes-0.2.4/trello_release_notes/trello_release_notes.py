# -*- coding: utf-8 -*-

"""Main module."""
from datetime import date
from trello import TrelloClient
from loguru import logger

"""
# given a list of boards
# for each board
# given a "done" list
# given a "released" list
# if there are items in the done list,
    create a release card for this date in the releases list
# for each item in the done list
# get the release card for this date
# append the title as list item to the description of the release card
# add the title and details as a comment on the release card
# archive the done item
# post process - send an email or do something with the release detail
"""


class Trellist(object):
    """The main object - initialize and use run()

    :param apikey: Your api-key.
    :param apisecret: Your api secret token. Get it from a protected file that you don't commit. Keep it secret!
    :param boardname: Name of the board to work on.
    :param done_list_name: The name of the done list on your board. Only one.
    :param releases_list_name: The name of the list to put release cards on.
    :param create_comments: True by default. Create a comment on the release card for each done card
    :param create_release_if_zero_done: If nothing is done, should you make a sad empty release card?
    """

    def __init__(
        self,
        apikey,
        apisecret,
        boardname,
        done_list_name="done",
        releases_list_name="releases",
        create_comments=True,
        create_release_if_zero_done=False,
    ):
        self.client = TrelloClient(api_key=apikey, api_secret=apisecret)
        self.board = self.get_board(boardname)
        self.done = self.get_list_by_name(done_list_name)
        self.releases = self.get_list_by_name(releases_list_name)
        self.release_template = "{date} release: {count} done"
        self.create_comment_per_item = create_comments
        self.create_release_if_zero_done = create_release_if_zero_done

    def run(self):
        """Runs through all the methods to perform the work"""
        logger.info(f"get all cards in the done board: {self.done.name}")
        cards = self.get_done_cards()
        logger.info(f"got {len(cards)} cards")
        if cards or self.create_release_if_zero_done:
            release_card = self.create_release_card(cards, self.release_template)
            for card in cards:
                if self.create_comment_per_item:
                    self.add_comment_to_release(release_card, card)
                card.set_closed(True)
        logger.info("finished run")

    def get_board(self, board_name):
        """Gets the open board object by a name, otherwise returns None

        :param board_name: actual name of a board you have access to
        """
        return self.first(
            self.client.list_boards(), lambda b: b.name == board_name and not b.closed
        )

    def get_list_by_name(self, name):
        """Iterate lists and get the first one matching the name passed in

        :param name: Name of a list on the board you've passed in
        """
        return self.first(self.board.list_lists(), lambda l: l.name == name)

    def first(self, iterable, condition):
        """Iterates an iterable and returns the first item that meets a condition or None

        :param iterable: An iterable to fetch the first itemm that meets condition
        :param condition: The condition to evaluate per item
        """
        return next((i for i in iterable if condition(i)), None)

    def get_done_cards(self):
        """Get every card from the done list"""
        return self.done.list_cards()

    @classmethod
    def summarize_these(self, cards, template="- {card.name}"):
        """Run a list of cards through a template and return those joined by newlines

        :param cards: Card objects to summarize
        :param template: A template for each card. We pass the full card to format
        """
        summary = "\n".join([template.format(card=card) for card in cards])
        return summary

    def create_release_card(self, cards, template):
        """Returns a new release card, with a title from template and description based on a summary of the cards

        :param cards: Cards in this release
        :param template: A format string that we pass in date and length of cards
        """
        release_card_name = template.format(date=date.today(), count=len(cards))
        # turn list of names of cards into a summary
        summary = self.summarize_these(cards)
        logger.info(f"{summary}")
        release_card = self.releases.add_card(release_card_name, summary)
        return release_card

    def add_comment_to_release(
        self,
        release_card,
        card,
        comment_format="{card.name}\n{card.url}\n{card.description}",
    ):
        """add_comment_to_release

        :param release_card: A card to comment on
        :param card: A card to summarize in a comment
        :param comment_format: The template, passed in the card.
        """
        comment_text = comment_format.format(card=card)
        release_card.comment(comment_text)
