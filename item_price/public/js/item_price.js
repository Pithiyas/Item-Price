frappe.ui.form.on('Item Price', {
    custom_price_type:function(frm){
        if(frm.doc.custom_price_type == 'Last Purchase Rate'){
            frappe.call({
                method:'item_price.public.py.item_price.get_last_purchase_rate',
                args:{'item_code':frm.doc.item_code}
            }).then(records =>{
                var data =  records['data']
                frm.set_value('price_list_rate', data)
            })
        }
        else if (frm.doc.custom_price_type == 'Item Average'){
            frappe.call({
                method:'item_price.public.py.item_price.get_avg_price',
                args:{'item_code':frm.doc.item_code, 'company':frm.doc.custom_company}
            }).then(records =>{
                var data =  records['data']

                length = data.length
                
                avr_rate = 0
                data.forEach(function(obj){
                     avr_rate += obj['valuation_rate']
                })

                finial_ave = avr_rate / length
                frm.set_value('price_list_rate', finial_ave)
            })
        }
    }
})