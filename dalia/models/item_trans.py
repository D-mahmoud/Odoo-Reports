from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class ReportItemTransReportView(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.dalia.item_trans_report_wizard_view'
    @api.model
    def _get_report_values(self, docids, data=None):
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        print('date ---------------', date_start)
        from_warehouse = data['form']['from_warehouse']
        to_warehouse = data['form']['to_warehouse']

         # POL = self.env['purchase.order.line']
        start_date = datetime.strptime(date_start, DATE_FORMAT)
        end_date = datetime.strptime(date_end, DATE_FORMAT)
        delta = timedelta(days=1)
        warehouses = []
        products =[]
        group=[]
        warehouse_product = []
        items = []
        index = 0
        temp = 0


        SM = self.env['stock.move']
        query='select sum (totalqtyin.product_uom_qty) + sum(totalqtyout.product_uom_qty) from totalqtyin join totalqtyout on totalqtyin.reference = totalqtyout.reference where totalqtyin.date < "start_date" and totalqtyout.date < "start_date"'

        self.env.cr.execute(query)
        opening=self.env.cr.fetchall()
        print ("opening", opening)


        # POL = self.env['purchase.order.line']
        start_date = datetime.strptime(date_start, DATE_FORMAT)
        end_date = datetime.strptime(date_end, DATE_FORMAT)
        delta = timedelta(days=1)
        warehouses = []
        products =[]
        group=[]
        warehouse_product = []
        items = []
        index = 0
        temp = 0
        # opening =  SM.search([
        #         ('date', '<', date.strftime(DATETIME_FORMAT))
        #     #before from date
        #     for i in opening:
        #         qty += product_uom_qty

        while start_date <= end_date:
            date = start_date
            start_date += delta

            print(date, start_date)
            transfers = SM.search([
                ('date', '>=', date.strftime(DATETIME_FORMAT)),
                ('date', '<', start_date.strftime(DATETIME_FORMAT)),
                #('state', 'in', ['stock', 'done'])
            ]) 
            
            print("////////////////",transfers)
            for transfer in transfers: 
                POL = self.env['purchase.order.line']
                product = POL.search([('product_id', '=', transfer.product_id.id)])
                print(transfer.reference, transfer.id)
                print (product)
                
                product_id = transfer.product_id.name
                product_uom_qty = transfer.product_uom_qty
                from_warehouse = transfer.location_id.complete_name
                warehouse = transfer.location_dest_id.complete_name
                reference = transfer.reference
                balance =transfer.availability
                # if (index = 1):
                #     temp = qty
                # else:
                #     temp =0
                # closing += temp + balance
                # index+=1





              
                
                
                for rec in product:
                    unit_price = rec.price_unit
                    net_amount = rec.price_subtotal
                    
                    print("--------------------------",product_id)
                    #items array contains all item details
                    items.append({
                            "warehouse": from_warehouse,
                            "product_id" : product_id,
                            "unit_price" : rec.price_unit,
                            "price_subtotal" : rec.price_subtotal,
                            'date': date.strftime("%Y-%m-%d"),
                            'reference':reference,
                            'quantity': product_uom_qty,
                            'to_warehouse': warehouse,
                            "balance":closing
                        })
        #ware array contains warehouse and product code only
                warehouse_product.append({
                        'product_code': product_id,
                        'warehouse': from_warehouse,
                       
                    })
            
        if {'warehouse': from_warehouse} not in warehouse_product :
        #wh array contains unrepeated warehouses 
                warehouses.append({'warehouse': from_warehouse})
        for i in warehouses :
        #count till number of unique warehouses
            for j in warehouse_product :
                if j['warehouse']  == i['warehouse'] : 
                    if {'products': j['product_code']} not in products :
        #append unrepeated products in pro
                        products.append({'products': j['product_code']})
         #append pro + warehouse in group        
            group.append({'warehouse': from_warehouse,'product':products} )
            #initialize pro every time
            products=[]
           
        

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'date_start': date_start,
            'date_end': date_end,
            'from_warehouse': from_warehouse,
            'to_warehouse': to_warehouse,

            'ware': group,
            'items': items,
        }
