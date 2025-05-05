from odoo import models, fields


class EnglishSong(models.Model):
    _name = 'english.song'
    _description = 'English Song for Learning'
    _rec_name = "title"

    title = fields.Char(string="Title", required=True)
    artist = fields.Char(string="Artist")
    lyrics = fields.Html(string="Lyrics")
    youtube_url = fields.Char(string="YouTube URL")
    level_estimate = fields.Selection([
        ('A1', 'Beginner (A1)'),
        ('A2', 'Elementary (A2)'),
        ('B1', 'Intermediate (B1)'),
        ('B2', 'Upper Intermediate (B2)'),
        ('C1', 'Advanced (C1)'),
    ], string="Estimated Level")
    difficult_words = fields.Text(
        string="Difficult Words"
    )
    exercise_ids = fields.One2many(
        'english.exercise.song',
        'song_id',
        string="Exercises"
    )
