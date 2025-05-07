/** @odoo-module */

import { registry } from "@web/core/registry"
import { kanbanView } from "@web/views/kanban/kanban_view"
import { KanbanController } from "@web/views/kanban/kanban_controller"
import { useService } from "@web/core/utils/hooks"

const { onWillStart } = owl

class ResPartnerKanbanController extends KanbanController {

    static template = "owl.ResPartnerKanbanView";

    setup(){
        super.setup();
        this.action = useService("action");
        this.orm = useService("orm");
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
        onWillStart(async()=>{
            this.customerLocations = await this.orm.readGroup("res.partner", [], ["state_id"], ["state_id"])
        })
    }

    selectLocations(state){
        const id = state[0];
        // const name = state[1];
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Partners",
            res_model: "res.partner",
            views: [[false, "kanban"]],
            target: "current", // evita abrir nueva pestaña
            domain: [['state_id', '=', id]],
        }, {
            clearBreadcrumbs: true,
        });
    }

    onClickOption(ev) {
        const model = ev.currentTarget.dataset.model;
        this.action.doAction(model);
    }

}

export const resPartnerKanbanView = {
    ...kanbanView,
    Controller: ResPartnerKanbanController,
    buttonTemplate: 'owl.ResPartnerKanbanView.Buttons',
}

registry.category("views").add("res_partner_kanban_view", resPartnerKanbanView)