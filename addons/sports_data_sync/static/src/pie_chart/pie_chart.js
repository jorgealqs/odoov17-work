/** @odoo-module */

import { loadJS } from "@web/core/assets";
import { getColor } from "@web/core/colors/colors";
import { Component, onWillStart, useRef, onMounted, onWillUnmount } from "@odoo/owl";

export class PieChart extends Component {
    static template = "sports_data_sync.PieChart";
    static props = {
        label: String,
        data: Object,
    };

    setup() {
        this.canvasRef = useRef("canvas");
        onWillStart(() => loadJS([
            "https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"
        ]));
        onMounted(() => {
            this.renderChart();
        });
        onWillUnmount(() => {
            this.chart.destroy();
        });
    }

    renderChart() {
        const followedNames = this.props.data.with_sessions.names;
        const followedCount = this.props.data.with_sessions.count;
        const notFollowedCount = this.props.data.without_sessions.count;
        const total = followedCount + notFollowedCount;

        const data = followedNames.map(() => 1);  // Valor fijo para visualizar los nombres

        const color = followedNames.map((_, index) => getColor(index));

        // Mostrar resumen arriba del gráfico
        const summaryEl = document.createElement("div");
        summaryEl.innerText = `Países seguidos: ${followedCount} / Total: ${total}`;
        summaryEl.style.textAlign = "center";
        summaryEl.style.marginBottom = "10px";
        summaryEl.style.fontWeight = "bold";
        summaryEl.style.fontSize = "14px";
        this.canvasRef.el.parentElement.prepend(summaryEl);

        // Crear gráfico solo con los países seguidos
        this.chart = new Chart(this.canvasRef.el, {
            type: "bar",
            data: {
                labels: followedNames,
                datasets: [{
                    label: this.props.label || "Países seguidos",
                    data: data,
                    backgroundColor: color,
                    borderColor: color,
                    borderWidth: 1,
                }],
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                scales: {
                    x: {
                        display: false,
                    },
                    y: {
                        ticks: {
                            autoSkip: false,
                            font: {
                                size: 12,
                            },
                            callback: function(value, index, ticks) {
                                return this.getLabelForValue(value);
                            },
                            // maxRotation: 45,
                            // minRotation: 45,
                        }
                    }
                },
                plugins: {
                    legend: { display: false },
                    title: {
                        display: true,
                        text: "Listado de países seguidos",
                    },
                },
            }
        });
    }
}