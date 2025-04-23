/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class CryptoCoinItem extends Component {
    static template = "lotteries.CryptoCoinItem";
    static props = {
        cryptoItem: { type: Object },
    };
}