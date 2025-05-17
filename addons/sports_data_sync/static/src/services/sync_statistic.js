/** @odoo-module **/


import { useState } from  "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export const useStatistics = () => {
    return useState(useService("sports_sync_data.statistics"));
};
