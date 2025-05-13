/** @odoo-module */

import { registry } from "@web/core/registry";
import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { WikiNotes } from "../components/notes/notes"
import { WikiResources } from "../components/resources/resources"

class DashboardWikiKnowledgeData extends Component {
    static template = "creative_mind.DashboardData";

    static components = {
        Layout,
        WikiNotes,
        WikiResources
    };

    setup() {
        this.display = {
            controlPanel: {},
        };
        this.action = useService("action");
        this.statistics = useState(useService("creative_wiki.statistics"));
    }

    openModule(ev) {
        const option = ev.target?.dataset?.option;
        if (option) {
            this.action.doAction(option);
        } else {
            console.warn("No se encontró opción para ejecutar.");
        }
    }
}

registry.category("lazy_components").add("DashboardWikiKnowledge", DashboardWikiKnowledgeData);