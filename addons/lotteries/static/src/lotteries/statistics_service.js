/** @odoo-module */

import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";

const statisticsService = {
    dependencies: ["rpc"],
    start(env, { rpc }) {
        const statistics = reactive({ isReady: false });
        async function loadDataLottery() {
            const updates = await rpc("/lottery/statistics");
            Object.assign(statistics, updates, { isReady: true });
        }
        setInterval(loadDataLottery, 1*60*1000);
        loadDataLottery();
        return statistics;
    },
};

registry.category("services").add("lotteries.statistics", statisticsService);