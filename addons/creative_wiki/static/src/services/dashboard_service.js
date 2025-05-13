/** @odoo-module */

import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";

const serviceKnowledge = {
    dependencies: ["rpc"],
    start(env, { rpc }) {
        const statistics = reactive({ hasData: false });

        async function loadData({ url = "/wiki/resources", params = {} } = {}) {
            try {
                const updates = await rpc(url, params);
                Object.assign(statistics, updates, { hasData: true });
            } catch (error) {
                console.error("Error loading sports data:", error);
            }
        }

        // Auto-load every minute
        setInterval(loadData, 10*60*1000);
        loadData();

        // ✅ Expose both the state and the function
        return statistics;
    },
};

registry.category("services").add("creative_wiki.statistics", serviceKnowledge);