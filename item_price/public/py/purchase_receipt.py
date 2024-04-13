import frappe
import json

@frappe.whitelist()
def update_item_prince(items, company):
    data = frappe.json.loads(items)

    for i in data: 
        item_price_data = frappe.db.sql("SELECT name, custom_price_type FROM `tabItem Price` WHERE item_code=%s and buying=1 ORDER BY modified DESC LIMIT 1", (i['item_code']), as_dict=True)

        if item_price_data[0]['custom_price_type'] == 'Item Average':
            data = frappe.db.sql("""
                SELECT b.valuation_rate
                FROM `tabBin` b
                INNER JOIN `tabWarehouse` w ON b.warehouse = w.name
                WHERE b.item_code = %s AND w.company = %s
            """, (i['item_code'], company), as_dict=True)

            total_sum = sum(item['valuation_rate'] for item in data)
            data_length = len(data)
            average = total_sum / data_length

            frappe.db.set_value('Item Price', item_price_data[0]['name'], 'price_list_rate', average)
        
        elif item_price_data[0]['custom_price_type'] == 'Last Purchase Rate':
            data = frappe.db.sql("""
                SELECT rate, qty, landed_cost_voucher_amount
                FROM `tabPurchase Receipt Item`
                WHERE item_code = %s
                ORDER BY creation DESC
                LIMIT 1
            """, (i['item_code'],), as_dict=True)
            last_rate = 0
            for i in data:
                last_landed = i['landed_cost_voucher_amount'] / i['qty']
                last_rate = last_landed + i['rate']
            frappe.db.set_value('Item Price', item_price_data[0]['name'], 'price_list_rate', last_rate)
        
        elif item_price_data[0]['custom_price_type'] == 'Manually':
            frappe.db.set_value('Item Price', item_price_data[0]['name'], 'price_list_rate', i['rate'])

