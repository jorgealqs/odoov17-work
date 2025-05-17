/** @odoo-module **/


export const ButtonsModels = [
    {name: "Countries", model: "sports_data_sync.action_sports_track_country"},
    {name: "Leagues", model: "sports_data_sync.action_sports_track_league"},
    {name: "Teams", model: "sports_data_sync.action_sports_track_team"},
    {name: "Standings", model: "sports_data_sync.action_sports_track_standing"},
    {name: "Fixtures", model: "sports_data_sync.action_sports_track_fixture"},
]


export const HeaderCvs = ["Liga", "Fecha", "Equipo Local", "Puntos Local", "Equipo Visitante", "Puntos Visitante", "Predicción", "Ganador"]