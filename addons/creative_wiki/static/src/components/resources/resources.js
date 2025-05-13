/** @odoo-module **/

import { Component, markup } from "@odoo/owl";

export class WikiResources extends Component {
    static template = "creative_wiki.DashboardResources";
    static props = {
        resources: Array
    };

    get formattedResources() {
        return this.props.resources.map(res => ({
            ...res,
            htmlDescription: markup(res.description || ""),
        }));
    }
}