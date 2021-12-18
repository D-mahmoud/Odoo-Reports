from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class ReportWarehouseReportView(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.dalia.warehouse_report_wizard_view'

    @api.model
    def _get_report_values(self, docids, data=None):
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        print('date ---------------', date_start)
        from_warehouse = data['form']['from_warehouse']
        to_warehouse = data['form']['to_warehouse']

        PO = self.env['purchase.order']
        POL = self.env['purchase.order.line']
        start_date = datetime.strptime(date_start, DATE_FORMAT)
        end_date = datetime.strptime(date_end, DATE_FORMAT)
        delta = timedelta(days=1)

        docs = []
        while start_date <= end_date:
            date = start_date
            start_date += delta

            print(date, start_date)
            orders = PO.search([
                ('date_approve', '>=', date.strftime(DATETIME_FORMAT)),
                ('date_approve', '<', start_date.strftime(DATETIME_FORMAT)),
                ('invoice_status', 'in', ['purchase', 'invoiced'])
            ])
            for order in orders:
                product = POL.search([('product_id', '=', order.product_id.id)])
               
                for rec in product:
                    
                    product_id = rec.product_id.name
                    product_qty = rec.product_qty
                    unit_price = rec.price_unit
                    warehouse = order.picking_type_id.display_name
                    net_amount = rec.price_subtotal
                    print("--------------------------",product_id)
                docs.append({
                    'date': date.strftime("%Y-%m-%d"),

                    'product_code': product_id,
                    'quantity': product_qty,
                    'unit_price': unit_price,
                    'net_amount': net_amount,
                    'warehouse': warehouse,

                })

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'date_start': date_start,
            'date_end': date_end,
            'from_warehouse': from_warehouse,
            'to_warehouse': to_warehouse,

            'docs': docs,
        }
