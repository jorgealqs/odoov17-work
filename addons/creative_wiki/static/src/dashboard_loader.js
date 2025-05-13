/** @odoo-module */

import { registry } from "@web/core/registry";
import { LazyComponent } from "@web/core/assets";
import { Component, xml } from "@odoo/owl";

class DashboardKnowledge extends Component {
    static components = { LazyComponent };
    static template = xml`
        <LazyComponent bundle="'creative_wiki_knowledge.dashboard'" Component="'DashboardWikiKnowledge'" props="props"/>
    `;
}

registry.category("actions").add("creative_wiki.ActionDashboardKnowledge", DashboardKnowledge);