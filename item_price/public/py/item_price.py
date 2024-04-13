import frappe

@frappe.whitelist()
def get_last_purchase_rate(item_code):
    
    data = frappe.db.sql("""
    SELECT rate, qty, landed_cost_voucher_amount
    FROM `tabPurchase Receipt Item`
    WHERE item_code = %s
    ORDER BY creation DESC
    LIMIT 1
""", (item_code,), as_dict=True)

    last_rate = 0
    for i in data:
        last_landed = i['landed_cost_voucher_amount'] / i['qty']
        last_rate = last_landed + i['rate']

    frappe.response['data']=last_rate


@frappe.whitelist()
def get_avg_price(item_code, company):

    data = frappe.db.sql("""
    SELECT b.valuation_rate
    FROM `tabBin` b
    INNER JOIN `tabWarehouse` w ON b.warehouse = w.name
    WHERE b.item_code = %s AND w.company = %s
""", (item_code, company), as_dict=True)   


    frappe.response['data']=data
    