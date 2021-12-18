from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class VendorBalanceReportView(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.dalia.vendor_balance_report_wizard_view'
    @api.model
    def _get_report_values(self, docids, data=None):
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        
        from_warehouse = data['form']['from_warehouse']
        to_warehouse = data['form']['to_warehouse']

        PO = self.env['purchase.order']
        
        start_date = datetime.strptime(date_start, DATE_FORMAT)
        end_date = datetime.strptime(date_end, DATE_FORMAT)
        delta = timedelta(days=1)

        vendors = []
        warehouses =[]
        group=[]
        vendor_warehouse = []
        items = []
       

        while start_date <= end_date:
            date = start_date
            start_date += delta
            
            purchases = PO.search([
                ('create_date', '>=', date.strftime(DATETIME_FORMAT)),
                ('create_date', '<', start_date.strftime(DATETIME_FORMAT)),
                #('state', 'in', ['stock', 'done'])
            ]) 


            for purchase in purchases: 
                POL = self.env['purchase.order.line']
                products = POL.search([('product_id', '=', purchase.product_id.id)])
                # print("----------------------",purchase.partner_id, purchase.id)
                

                purchase_id = purchase.id
                
                invoice_id = purchase.name
                product_id = purchase.product_id.name
                
                warehouse = purchase.picking_type_id.display_name
                vendor = purchase.partner_id.name
                
                
                for product in products:
                    product_uom_qty = product.product_qty
                    
                    price_subtotal = product.price_subtotal
                    # print("#######",product)
                    # print("--------------------------",product_id)

                    #items array contains all item details
                    items.append({
                            "warehouse": warehouse,
                            "product_id" : product_id,
                            "price_subtotal" : price_subtotal,
                            'date': date.strftime("%Y-%m-%d"),
                            "vendor":vendor,
                            'quantity': product_uom_qty,
                            'invoice_id': invoice_id,
                            "purchase_id":purchase_id
                        })
        #vendors array contains warehouse and vendor only
                vendor_warehouse.append({
                        'vendor':vendor,
                        'warehouse': warehouse,
                       
                    })
            
        if {'vendor': vendor} not in vendor_warehouse :
        #vendors array contains unrepeated vendors 
                vendors.append({'vendor': vendor})
        for i in vendors :
        #count till number of unique vendors
            for j in vendor_warehouse :
                if j['vendor']  == i['vendor'] : 
                    if {'warehouse': j['warehouse']} not in warehouses :
        #append unrepeated warehouses in warehouses
                        warehouses.append({'warehouse': j['warehouse']})
         #append vendors + warehouses in group        
            group.append({'vendor':i['vendor'],'warehouse': warehouses,} )
            print ("++++++++++=",group)
            #initialize warehouses every time
            warehouses=[]
            
            

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'date_start': date_start,
            'date_end': date_end,
            'from_warehouse': from_warehouse,
            'to_warehouse': to_warehouse,
            'vendor_warehouse':group,
            'items': items,

        }
