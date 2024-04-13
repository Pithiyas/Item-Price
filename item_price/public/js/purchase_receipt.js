frappe.ui.form.on('Purchase Receipt', {
    on_submit:function(frm){
        frappe.call({
            method:'item_price.public.py.purchase_receipt.update_item_prince',
            args:{
                'items':frm.doc.items,
                'company':frm.doc.company
            }
        })
    }

})