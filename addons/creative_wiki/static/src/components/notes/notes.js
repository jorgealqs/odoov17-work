/** @odoo-module **/

import { Component, markup } from "@odoo/owl"; // ¡aquí está!

export class WikiNotes extends Component {
    static template = "creative_wiki.DashboardNotes";
    static props = {
        notes: Array
    };

    get formattedNotes() {
        return this.props.notes.map(note => ({
            ...note,
            htmlContent: markup(note.content), // ⬅️ ¡Aquí se convierte a Markup seguro!
        }));
    }
}