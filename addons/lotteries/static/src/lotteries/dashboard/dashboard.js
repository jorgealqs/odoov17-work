/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";
import { DashboardLastDraw } from "./last_draw/last_draw";
import { DashboardCryptoCoin } from "./crypto/crypto";

class DashboardGames extends Component {
    static template = "lotteries.Dashboard";
    static components = { Layout, DashboardItem, PieChart, DashboardLastDraw, DashboardCryptoCoin };

    setup() {
        this.action = useService("action");
        this.rpc = useService("rpc");
        this.display = {
            controlPanel: {},
        };
        this.statistics = useState(useService("lotteries.statistics"));
    }

    openLotteriesDraws(){
        this.action.doAction("lotteries.action_lottery_draw");
    }

    openCryptoCoins(){
        this.action.doAction("lotteries.action_crypto_coin");
    }

    openCryptoHistory(){
        this.action.doAction("lotteries.action_crypto_price_history");
    }

    onClickGame(idGame, lottery){
        this.action.doAction({
            type: "ir.actions.act_window",
            name: `Sorteos por Juego: ${lottery}`,
            res_model: "lottery.draw",
            views: [[false, "list"]],
            domain: [["game_id.id", "=", parseInt(idGame)]],
        });
    }

}

registry.category("lazy_components").add("DashboardGamesLottery", DashboardGames);