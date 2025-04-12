/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class ForescastItems extends Component {
    static template = "lotteries.ForecastItems";
    static props = {
        results: Array,
    };

    // Estado para mostrar/ocultar fechas
    setup() {
        this.state = useState({
            showDates: false,  // Inicialmente las fechas están ocultas
        });

        // Función para alternar la visibilidad de las fechas
        this.toggleDates = () => {
            this.state.showDates = !this.state.showDates;
        };
    }

}