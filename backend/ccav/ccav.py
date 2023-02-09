from .ccavutil import decrypt, encrypt
from string import Template


def pay(
        p_order_id,
        p_currency,
        p_amount,
        p_redirect_url,
        p_cancel_url,
        p_language,
        ####
        p_customer_identifier,
        p_delivery_name,
        p_delivery_address,
        p_delivery_city,
        p_delivery_state,
        p_delivery_zip,
        p_delivery_country,
        p_delivery_tel,
        ###
        p_billing_name,
        p_billing_address,
        p_billing_city,
        p_billing_state,
        p_billing_zip,
        p_billing_country,
        p_billing_tel,
        p_billing_email,
        ###
        p_merchant_param1=None,
        p_merchant_param2=None,
        p_merchant_param3=None,
        p_merchant_param4=None,
        p_merchant_param5=None,
        p_promo_code=None,
):
    p_merchant_id = '47953'
    p_integration_type = 'iframe_normal'

    merchant_data = 'merchant_id=' + p_merchant_id + '&' + 'order_id=' + p_order_id + '&' + "currency=" + p_currency + '&' + 'amount=' + p_amount + '&' + 'redirect_url=' + p_redirect_url + '&' + 'cancel_url=' + p_cancel_url + '&' + 'language=' + p_language + '&' + 'billing_name=' + p_billing_name + '&' + 'billing_address=' + p_billing_address + '&' + 'billing_city=' + p_billing_city + '&' + 'billing_state=' + p_billing_state + '&' + 'billing_zip=' + p_billing_zip + '&' + 'billing_country=' + p_billing_country + '&' + 'billing_tel=' + p_billing_tel + '&' + 'billing_email=' + p_billing_email + '&' + 'delivery_name=' + p_delivery_name + '&' + 'delivery_address=' + p_delivery_address + '&' + 'delivery_city=' + p_delivery_city + '&' + 'delivery_state=' + p_delivery_state + '&' + 'delivery_zip=' + p_delivery_zip + '&' + 'delivery_country=' + p_delivery_country + '&' + 'delivery_tel=' + p_delivery_tel + '&' + 'integration_type=' + p_integration_type

    if p_merchant_param1:
        merchant_data += '&' + 'merchant_param1=' + p_merchant_param1

    if p_merchant_param2:
        merchant_data += '&' + 'merchant_param2=' + p_merchant_param2

    if p_merchant_param3:
        merchant_data += '&' + 'merchant_param3=' + p_merchant_param3

    if p_merchant_param4:
        merchant_data += '&' + 'merchant_param4=' + p_merchant_param4

    if p_merchant_param5:
        merchant_data += '&' + 'merchant_param4=' + p_merchant_param5

    if p_promo_code:
        merchant_data += '&' + 'promo_code=' + p_promo_code

    merchant_data += '&' + 'customer_identifier=' + p_customer_identifier

    access_code = 'AVKE03IB70BD21EKDB'
    working_key = '4D6E3792B864FEE380685243E2C78324'

    encryption = encrypt(merchant_data, working_key)

    return f"https://secure.ccavenue.ae/transaction/transaction.do?command=initiateTransaction&merchant_id={p_merchant_id}&encRequest={encryption}&access_code={access_code}"
