/** @odoo-module **/

import { Component } from "@odoo/owl";
import { CryptoCoinItem } from "./item/item";

export class DashboardCryptoCoin extends Component {
    static template = "lotteries.DashboardCryptoCoin";
    static components = { CryptoCoinItem };
    static props = {
        cryptoList: { type: Object },
    };
}