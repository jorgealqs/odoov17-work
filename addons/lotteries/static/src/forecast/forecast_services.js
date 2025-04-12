/** @odoo-module */

import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";

const forecastService = {
    dependencies: ["rpc"],
    start(env, { rpc }) {
        const statistics = reactive({ isReady: false });
        async function loadData(url = "/lottery/forecast", params = {}) {
            const updates = await rpc(url, {
                method: "call",
                args: [params],
            });
            Object.assign(statistics, updates, { isReady: true });
        }

        statistics.loadData = loadData; // exponemos el método

        loadData(); // cargamos por defecto
        return statistics;
    },
};

registry.category("services").add("lotteries.forecast", forecastService);