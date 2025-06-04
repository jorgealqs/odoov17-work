from odoo import models, fields  # type: ignore
import logging

_logger = logging.getLogger(__name__)


class EnglishDictionary(models.Model):
    _name = 'english.dictionary'
    _description = 'English Dictionary Entry'
    _rec_name = 'word'

    word = fields.Char(string="Word", required=True)
    part_of_speech = fields.Selection([
        ('noun', 'Noun'),
        ('verb', 'Verb'),
        ('adjective', 'Adjective'),
        ('adverb', 'Adverb'),
        ('pronoun', 'Pronoun'),
        ('preposition', 'Preposition'),
        ('conjunction', 'Conjunction'),
        ('interjection', 'Interjection'),
    ], string="Part of Speech", required=True)
    definition = fields.Text(string="Definition", required=True)
    example_sentence = fields.Text(string="Example Sentence")
    translation = fields.Char(string="Translation (Optional)")
    audio_url = fields.Char(string="Pronunciation URL (Optional)")
    tag_ids = fields.Many2many('english.tag', string="Tags")

    _sql_constraints = [
        (
            'unique_word',
            'unique(word)',
            'The word must be unique in the dictionary.'
        )
    ]

    def send_telegram(self):
        _logger.info("\n\n Llegaste \n")
