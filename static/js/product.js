django.jQuery(function () {
    
    function change_product_type() {
        django.jQuery('.field-box.field-ladies_type').hide();
        django.jQuery('.field-box.field-mens_type').hide();
        django.jQuery('.field-box.field-accessories_type').hide();
        django.jQuery('.field-box.field-dance_shoes_type').hide();
        
        if (django.jQuery('#id_product_type').val() == 'ladies') {
            django.jQuery('.field-box.field-ladies_type').show();
        }
        if (django.jQuery('#id_product_type').val() == 'mens') {
            django.jQuery('.field-box.field-mens_type').show();
        }
        if (django.jQuery('#id_product_type').val() == 'accessories') {
            django.jQuery('.field-box.field-accessories_type').show();
        }
        if (django.jQuery('#id_product_type').val() == 'dance_shoes') {
            django.jQuery('.field-box.field-dance_shoes_type').show();
        }
    }
    
    change_product_type();
    
    django.jQuery('#id_product_type').change(function () {
        change_product_type();
    });
});