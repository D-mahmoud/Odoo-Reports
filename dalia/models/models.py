from odoo import models, fields, api
from logging import NullHandler



class dalia(models.Model):
    _name = 'dalia.dalia'
    _description = 'dalia.dalia'

    name = fields.Char(string="Name", required=False, help="Write your name")
    phone = fields.Integer(string="Phone", required=True, help="Write your phone")
    description = fields.Text(string="Description")


class WarehouseReportWizard(models.TransientModel):
    _name = 'warehouse.report.wizard'

    date_start = fields.Date(string='Start Date', required=True, default=fields.Date.today)
    date_end = fields.Date(string='End Date', required=True, default=fields.Date.today)

    from_warehouse = fields.Many2one(comodel_name='stock.warehouse', string='From Warehouse')
    to_warehouse = fields.Many2one(comodel_name='stock.warehouse', string='To Warehouse')

    @api.constrains()
    def get_report(self):
        data = {
            'model': self._name,
            'ids': self.ids,
            'form': {
                'date_start': self.date_start,
                'date_end': self.date_end,
                'from_warehouse': self.from_warehouse.id,
                'to_warehouse': self.to_warehouse.id,
                
            },
        }

        # ref `module_name.report_id` as reference.
        return self.env.ref('dalia.warehouse_report_wizard').report_action(self, data=data)


class ItemTransReportWizard(models.TransientModel):
    _name = 'item.trans.report.wizard'

    date_start = fields.Date(string='Start Date', required=True, default=fields.Date.today)
    date_end = fields.Date(string='End Date', required=True, default=fields.Date.today)

    from_warehouse = fields.Many2one(comodel_name='stock.warehouse', string='From Warehouse')
    to_warehouse = fields.Many2one(comodel_name='stock.warehouse', string='To Warehouse')

    @api.constrains()
    def get_report(self):
        data = {
            'model': self._name,
            'ids': self.ids,
            'form': {
                'date_start': self.date_start,
                'date_end': self.date_end,
                'from_warehouse': self.from_warehouse.id,
                'to_warehouse': self.to_warehouse.id,
                
            },
        }

        # ref `module_name.report_id` as reference.
        return self.env.ref('dalia.item_trans_report_wizard').report_action(self, data=data)



class VendorBalanceReportWizard(models.TransientModel):
    _name = 'vendor.balance.report.wizard'

    date_start = fields.Date(string='Start Date', required=True, default=fields.Date.today)
    date_end = fields.Date(string='End Date', required=True, default=fields.Date.today)

    from_warehouse = fields.Many2one(comodel_name='stock.warehouse', string='From Warehouse')
    to_warehouse = fields.Many2one(comodel_name='stock.warehouse', string='To Warehouse')

    @api.constrains()
    def get_report(self):
        data = {
            'model': self._name,
            'ids': self.ids,
            'form': {
                'date_start': self.date_start,
                'date_end': self.date_end,
                'from_warehouse': self.from_warehouse.id,
                'to_warehouse': self.to_warehouse.id,
                
            },
        }

        # ref `module_name.report_id` as reference.
        return self.env.ref('dalia.vendor_balance_report_wizard').report_action(self, data=data)
