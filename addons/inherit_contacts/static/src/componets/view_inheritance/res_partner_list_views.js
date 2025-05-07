/** @odoo-module */

import { registry } from "@web/core/registry"
import { listView } from "@web/views/list/list_view"
import { ListController } from "@web/views/list/list_controller"
import { useService } from "@web/core/utils/hooks"


class ResPartnerListController extends ListController {

    setup(){
        super.setup();
        this.action = useService("action");
        this.options = [
            {
                label: "English Learning",
                res_model: "english_learning.action_english_level",
                views: [[false, "kanban"], [false, "tree"], [false, "form"]],
            },
            {
                label: "Sports",
                res_model: "sports_data_sync.DashboardActionSportsSyncData",
                views: [[false, "kanban"], [false, "tree"], [false, "form"]],
            },
            {
                label: "Lotteries",
                res_model: "lotteries.dashboardAction",
                views: [[false, "kanban"], [false, "tree"], [false, "form"]],
            }
        ];
    }

    onClickOption(ev) {
        const model = ev.currentTarget.dataset.model;
        this.action.doAction(model);
    }

}

export const resPartnerListView = {
    ...listView,
    Controller: ResPartnerListController,
    buttonTemplate: 'owl.ResPartnerListView.Buttons',
}

registry.category("views").add("res_partner_list_view", resPartnerListView)