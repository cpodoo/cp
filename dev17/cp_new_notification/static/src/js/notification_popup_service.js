/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Dialog } from "@web/core/dialog/dialog";

export const notificationPopupService = {
    dependencies: ["rpc", "dialog"],

    async start(env, { rpc, dialog }) {
        try {
            const result = await rpc.query({
                route: "/check/new/notification",
                params: {},
            });

            if (result && result.popmodal) {
                // Use the dialog service to display the popup
                dialog.add(Dialog, {
                    title: result.title || env._t("Notification"),
                    size: 'medium', 
                    technical: false, 
                    $content: $(result.popmodal), 
                    footer: true,
                });
            }
        } catch (error) {
             
        }
    },
};

// Register the service to run when the web client starts
registry.category("services").add("notificationPopupService", notificationPopupService);

