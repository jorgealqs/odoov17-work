/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class ForescastItems extends Component {
    static template = "lotteries.ForecastItems";
    static props = {
        results: Array,
    };

    setup() {
        this.state = useState({
            showDatesMap: {},  // Diccionario para controlar cada fila por número
        });

        // Alternar visibilidad para un número específico
        this.toggleDates = (number) => {
            const current = this.state.showDatesMap[number] || false;
            this.state.showDatesMap[number] = !current;
        };
    }
}