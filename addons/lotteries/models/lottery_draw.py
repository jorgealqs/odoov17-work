from odoo import models, fields  # type: ignore


class LotteryDraw(models.Model):
    _name = 'lottery.draw'
    _description = 'Lottery Draw'
    _order = 'draw_number desc, draw_date desc'

    name = fields.Char(string='Draw Name', required=True)
    draw_number = fields.Integer(string='Sorteo', required=True)
    draw_date = fields.Date(string='Draw Date')
    game_id = fields.Many2one(
        'lottery.game',
        string='Game',
        required=True,
        ondelete='restrict'
    )
    jackpot = fields.Float(string='Jackpot Amount', digits=(12, 2))
    win = fields.Boolean(string='Win', default=False)

    number_ids = fields.One2many(
        'lottery.draw.number',
        'draw_id',
        string='Numbers'
    )

    _sql_constraints = [
        (
            'name_unique',
            'UNIQUE(name)',
            'The name of the lottery draw must be unique!'
        )
    ]
