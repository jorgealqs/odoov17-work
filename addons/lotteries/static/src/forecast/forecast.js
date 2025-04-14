/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { SelectGame } from "../utils/select/select";
import { ForescastItems } from "./forecast_items/forecast_items";

class ForescastGames extends Component {
    static template = "lotteries.Forecast";
    static components = { Layout, SelectGame, ForescastItems };

    setup() {
        this.display = {
            controlPanel: {},
        };
        this.state = useState({
            selectedGameValue: "",
            selectedOptionValue: "",
        });
        this.notification = useService("notification");
        this.action = useService("action");
        this.statistics = useState(useService("lotteries.forecast"));
        console.log(this.statistics);
    }

    onSelectChange(ev) {
        const { title, value } = ev;
        if (title === "Game") {
            this.state.selectedGameValue = value;
        } else if (title === "Option") {
            this.state.selectedOptionValue = value;
        }
    }

    async applyFilters() {
        const { selectedGameValue, selectedOptionValue } = this.state;

        if (!selectedGameValue || !selectedOptionValue) {
            this.notification.add("Please select both a game and an option.", {
                title: "Missing Filters",
                type: "warning",
            });
            return;
        }

        const url = "/lottery/forecast/results";
        const params = {
            game_id: selectedGameValue,
            option_id: selectedOptionValue,
        };

        await this.statistics.loadData(url, params);
        console.log("✅ Filters applied with:", this.statistics);
    }

    openLotteriesDraws(){
        this.action.doAction("lotteries.action_lottery_draw");
    }

}

registry.category("lazy_components").add("ForescastGames", ForescastGames);