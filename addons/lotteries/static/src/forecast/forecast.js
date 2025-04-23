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
    static props = {};

    setup() {
        this.display = {
            controlPanel: {},
        };
        this.state = useState({
            selectedGameValue: "",
            selectedOptionValue: "",
            selectedNumberValue: "",
        });
        this.notification = useService("notification");
        this.action = useService("action");
        this.statistics = useState(useService("lotteries.forecast"));
        this.combinations = [
            { name: "3", value: "3" },
            { name: "4", value: "4" },
            { name: "5", value: "5" },
            { name: "6", value: "6" },
        ];
    }

    onSelectChange(ev) {
        const { title, value } = ev;
        if (title === "Game") {
            this.state.selectedGameValue = value;
        } else if (title === "Option") {
            this.state.selectedOptionValue = value;
        } else if (title === "Number") {
            this.state.selectedNumberValue = value;
        }
    }

    async applyFilters() {
        const { selectedGameValue, selectedOptionValue, selectedNumberValue } = this.state;

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
            number: selectedNumberValue,
        };

        await this.statistics.loadData(url, params);
    }

    openLotteriesDraws(){
        this.action.doAction("lotteries.action_lottery_draw");
    }

}

registry.category("lazy_components").add("ForescastGames", ForescastGames);