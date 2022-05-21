window.onload = function () {
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
        total_price += delta_cost;
        total_quantity += delta_quantity
        $('.order_total_cost').html(Number(total_price.toString()).toFixed(2));
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
}