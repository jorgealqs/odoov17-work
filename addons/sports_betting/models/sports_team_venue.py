from odoo import models, fields  # type: ignore


class SportsTeamVenue(models.Model):
    _name = "sports.team.venue"
    _description = "Sports Team Venue"

    name = fields.Char(string="Venue Name", required=True)
    address = fields.Char(string="Address")
    city = fields.Char(string="City")
    capacity = fields.Integer(string="Capacity")
    surface = fields.Char(string="Surface")
    image = fields.Char(string="Venue Image")  # URL de la imagen del estadio
