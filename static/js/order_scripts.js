window.onload = function () {
    $('.basket_list').on('click', 'input[type="number"]', function () {
        let t_href = event.target;

        $.ajax({
            url: "/basket/edit/" + t_href.name + "/" + t_href.value + "/",
            success: function (data) {
                $('.basket_list').html(data.result);
            },
        });
        event.preventDefault();
    });

    let total_price = parseFloat($('.order_total_cost').text().replace(',', '.'));
    let total_forms = $('input[name=orderitem-TOTAL_FORMS]').val() || 0;
    let total_quantity = parseInt($('.order_total_quantity').text()) || 0;

    let _quantity, _price, orderitem_num, delta_quantity, orderitem_quantity,
        delta_cost;
    let quantity_arr = [];
    let price_arr = [];

    for (let i = 0; i < total_forms; i++) {
        _price = parseFloat($('.orderitems-' + i + '-price').text().replace(',', '.'));
        _quantity = parseInt($('input[name=orderitem-' + i + '-quantity]').val());
        quantity_arr[i] = _quantity;
        if (_price) {
            price_arr[i] = _price;
        } else { price_arr[i] = 0 };
    };


    $('.order_form').on('click', 'input[type=number]', function () {
        let target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitem-', '').replace('-quantity', ''));
        if (price_arr[orderitem_num]) {
            orderitem_quantity = parseInt(target.value);
            delta_quantity = orderitem_quantity - quantity_arr[orderitem_num];
            quantity_arr[orderitem_num] = orderitem_quantity;
            getSummary(price_arr[orderitem_num], delta_quantity);
        }
    })

    function getSummary(orderitem_price, delta_quantity) {
        delta_cost = orderitem_price * delta_quantity;
        total_price = Number((total_price + delta_cost).toFixed(2));
        total_quantity += delta_quantity
        $('.order_total_cost').html(Number(total_price.toString()));
        $('.order_total_quantity').html(total_quantity.toString());
    }

    $('.order_form').on('click', 'input[type=checkbox]', function () {
        let target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitem-', '').replace('-quantity', ''));

        if (target.checked) {
            delta_quantity = -quantity_arr[orderitem_num];
        } else {
            delta_quantity = quantity_arr[orderitem_num];
        }
        getSummary(price_arr[orderitem_num], delta_quantity);

    })

    $('.formset_row').formset({
        addText: 'добавить',
        deleteText: 'удалить',
        prefix: 'orderitem',
        removed: deleteOrderItem
    });

    function deleteOrderItem(row) {
        let target = row[0].querySelector('input[type="number"]').name;
        orderitem_num = parseInt(target.replace('orderitem-', '').replace('-quantity', ''));
        delta_quantity = -quantity_arr[orderitem_num];
        quantity_arr[orderitem_num] = 0;
        if (!isNaN(price_arr[orderitem_num]) && !isNaN(delta_quantity)) {
            getSummary(price_arr[orderitem_num], delta_quantity);
        };
    }

    $('.order_form select').change(function () {
        var target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitem-', '').replace('-product', ''));
        var orderitem_product_pk = target.options[target.selectedIndex].value;
        if (orderitem_product_pk) {
            $.ajax({
                url: '/product/' + orderitem_product_pk + '/',
                success: function (data) {
                    if (data.price) {
                        price_arr[orderitem_num] = parseFloat(data.price);
                        if (isNaN(quantity_arr[orderitem_num])) {
                            quantity_arr[orderitem_num] = 0;
                        }
                        var price_html = '<span class="orderitems-' + orderitem_num + '-price">' + data.price.toString().replace('.', ',') + '</span> руб';
                        var current_tr = $('.order_form table').find('tr:eq(' + (orderitem_num + 1) + ')');
                        current_tr.find('td:eq(2)').html(price_html);
                        if (isNaN(current_tr.find('input[type="number"]').val())) {
                            current_tr.find('input[type="number"]').val(0);
                        }
                        orderSummaryRecalc();
                    }
                },
            });
        }
    });
    if (!total_quantity) {
        orderSummaryRecalc();
    }
    function orderSummaryRecalc() {
        total_quantity = 0;
        total_price = 0;
        for (var i = 0; i < total_forms; i++) {
            total_quantity += quantity_arr[i];
            total_price += quantity_arr[i] * price_arr[i];
        }
        $('.order_total_quantity').html(total_quantity.toString());
        $('.order_total_cost').html(Number(total_price.toFixed(2)).toString());
    }
}