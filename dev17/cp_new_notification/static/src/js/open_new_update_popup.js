// @odoo-module 
import SystrayMenu from 'web.SystrayMenu';
import Widget from 'web.Widget';

var OpenNewUpdatePopup = Widget.extend({
    sequence: 1000,
    name: 'dropdownMenuButtonNotification',
    template: 'mtech_new_notification.open_new_update_popup',
    events: {
        'click .dropdown-item': 'OpenPopUp'
    },

    init: function() {
        this.notificationdatas = [];
        this.notificationdatascounter = 0;
        this._super.apply(this, arguments);
    },
    willStart: function() {
        var self = this;
        return this._super.apply(this, arguments).then(function() {
            return self.load();
        });
    },
    load: function() {
        var self = this;
        return this._rpc({model: 'new.update.notification', method: 'get_users_notify_datas'}).then(function(data){
            self.notificationdatas = data.notifydatas;
            self.notificationdatascounter = data.notifycounter;
        });
    },
    OpenPopUp: function(ev) {
        var self = this;
        var res_id = parseInt(ev.currentTarget.dataset.id, 10);
        return this._rpc({model: 'new.update.notification', method: 'action_open_wizard', args: [res_id]})
                .then(function(data) {
                    if($('.notification_popup_cl_main').length){
                        $('.notification_popup_cl_main').remove();
                    }
                    if(data && data.popmodal){
                        $('body').append(data.popmodal);
                        $('.notification_popup_cl_main').modal('show');
                    }
                    
                });
    }
});

SystrayMenu.Items.push(OpenNewUpdatePopup);

export default OpenNewUpdatePopup;