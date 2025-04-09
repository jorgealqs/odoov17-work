from odoo import models, fields


class LotteryDrawNumber(models.Model):
    _name = 'lottery.draw.number'
    _description = 'Winning Number'
    _rec_name = 'number'

    draw_id = fields.Many2one(
        'lottery.draw',
        string='Draw',
        required=True,
        ondelete='cascade'
    )
    number = fields.Integer(string='Number', required=True)
    color = fields.Integer()
