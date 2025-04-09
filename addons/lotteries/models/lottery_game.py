from odoo import models, fields


class LotteryGame(models.Model):
    _name = 'lottery.game'
    _description = 'Lottery Game'

    name = fields.Char(required=True)
    description = fields.Html()
    website = fields.Char()
    active = fields.Boolean(default=True)

    _sql_constraints = [
        (
            'name_unique',
            'UNIQUE(name)',
            'The name of the lottery game must be unique!'
        )
    ]
