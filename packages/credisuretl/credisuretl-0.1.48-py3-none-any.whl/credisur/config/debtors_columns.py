def get_debtors_columns():
    # Ciudad	Cliente	Dirección	Teléfono	Fecha de Compra	Fecha de Vencimiento	
    # Orden de Compra	Última Cobranza	Cuotas	**Cuotas a pagar***	Valor de cuota	
    # Monto total a cobrar	Descripción	CBU

    # reemplazado Cuotas a pagar por Pagos faltantes

    config_list = list()
    config_list.append(("A", "Ciudad", 'city'))
    config_list.append(("B", "Cliente", 'customer'))
    config_list.append(("C", "Dirección", 'address'))
    config_list.append(("D", "Teléfono", 'phone'))
    config_list.append(("E", "Fecha de Compra", 'date_of_purchase'))
    config_list.append(("F", "Fecha de Vencimiento", 'due_date'))
    config_list.append(("G", "Orden de Compra", 'order'))
    config_list.append(("H", "Última Cobranza", 'last_collection'))
    config_list.append(("I", "Cuotas", 'plan'))
    config_list.append(("J", "Pagos faltantes", 'missing_payments'))
    config_list.append(("K", "Valor de cuota", 'payment'))
    config_list.append(("L", "Monto total a cobrar", 'amount_to_collect'))
    config_list.append(("M", "Descripción", 'full_description'))
    config_list.append(("N", "CBU", 'cbu'))
    config_list.append(("O", "Tipo de Venta", 'collection_account'))
    return config_list