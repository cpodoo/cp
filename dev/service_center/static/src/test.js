export class ServiceProductQuantity extends FloatField {
    setup() {
        super.setup(...arguments);
        const refName = 'numpadDecimal';
        useAutofocus({ refName });
        this.state = useState({
            readonly: this.props.readonly,
            addSmallClass: this.props.value.toString().length > 5,
        });

        const ref = useRef(refName);
        useEffect((el) => {
            if (el && ["INPUT", "TEXTAREA"].includes(el.tagName) && el.type === 'number') {
                el.value = el.value === '0' ? '' : el.value;
            }
        }, () => [ref.el]);
    }

    onInput(ev) {
        let service_product_qty = Number(ev.target.value.replace(",", ""));
        if (service_product_qty < 0) {
            alert("Quantity cannot be negative.");
            return;
        }
        let product_id = this.props.record.data.id;
        let context = this.getSession().context;
        let _service_id = context.service_id;
        $.ajax({
            url: "/qtyupdateservice",
            method: "GET",
            dataType: 'json',
            data: { quantity: service_product_qty, product_id: product_id, service_id: _service_id },
            success: function(response) {
                console.log("Quantity updated successfully.");
            },
            error: function(error) {
                console.error("Error updating quantity:", error);
            }
        });
        this.state.addSmallClass = ev.target.value.length > 5;
    }
}