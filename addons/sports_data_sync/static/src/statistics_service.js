/** @odoo-module */

import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";

const serviceDashboard = {
    dependencies: ["rpc"],
    start(env, { rpc }) {
        const statistics = reactive({ isReady: false });

        async function loadData({ url = "/sports_data/dashboard", params = {} } = {}) {
            try {
                const updates = await rpc(url, params);
                Object.assign(statistics, updates, { isReady: true });
            } catch (error) {
                console.error("Error loading sports data:", error);
            }
        }

        // Auto-load every minute
        setInterval(loadData, 1*60*1000);
        loadData();

        // ✅ Expose both the state and the function
        return statistics;
    },
};

registry.category("services").add("sports_sync_data.statistics", serviceDashboard);