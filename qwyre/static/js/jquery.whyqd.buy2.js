$(document).ready(function() {
    //if ($('#stripeButton').length > 0) {
    document.body.addEventListener('click', function(e) {
        // https://www.sitepoint.com/javascript-event-delegation-is-easier-than-you-think/
        // http://stackoverflow.com/a/13142797
        e = e || window.event;
        var target = e.target || e.srcElement;
        if (target.id.lastIndexOf("stripeButton",0) !== 0) {
            return e;
        }
        var novel_id = target.id.replace("stripeButton", "");
        $.ajax({
            url: $('#stripeSettings' + novel_id).val()
            }).done(function(data) {
                ns = data.settings;
                ns.template = $('#mailTemplate' + novel_id).val();
                var handler = StripeCheckout.configure({
                    key: ns.stripe_key,
                    image: '/static/images/qwyre_logo_128pxBW.png',
                    name: ns.novel_title,
                    email: ns.user_email,
                    bitcoin: true,
                    token: function(token) {
                        // http://stackoverflow.com/a/22461608
                        // You can access the token ID with `token.id`
                        if (!ns.user_email) {
                            ns.user_email = token.email;
                        }
                        var is_bitcoin = false;
                        if (token.type === "source_bitcoin") {
                            is_bitcoin = true;
                        }
                        $.ajax({
                            url: $('#stripeBuy' + novel_id).val(),
                            type: 'post',
                            data: {
                                stripeToken: token.id,
                                stripeDescription: ns.description,
                                stripePrice: ns.price,
                                stripeCurrency: ns.currency,
                                stripeEmails: ns.user_email,
                                selfPurchase: true, // Buying for own use
                                stripeBitcoin: is_bitcoin,
                                template: ns.template
                            },
                            success: function(data) {
                                if (data.response == 'success') {
                                    // http://stackoverflow.com/a/8965804
                                    $("#buytrigger" + novel_id).val(true).change();
                                    $('#buynow' + novel_id).empty();
                                    if (data.registered) {
                                        $('#buynow' + novel_id).before(
                                            '<div class="alert alert-success alert-dismissable">'+
                                            '<button type="button" class="close" ' + 
                                            'data-dismiss="alert" aria-hidden="true">' + '&times;' + 
                                            '</button>' + 
                                            '<p><strong>Thank you</strong>, your purchase has been successful.</p>' +
                                            '<p>You can continue reading ' + ns.novel_title + ' online, or ' +
                                            '<a href="' + data.link + '" class="alert-link"> download an ebook ' +
                                            'version</a>. You could even share a copy with your friends.</p>' +
                                            '</div>');
                                    }
                                    else {
                                        // http://stackoverflow.com/a/506004
                                        window.location.href = data.link;
                                    }
                                }
                                else {
                                    $('#buynowresponse').before(
                                        '<div class="alert alert-danger alert-dismissable">'+
                                            '<button type="button" class="close" ' + 
                                                'data-dismiss="alert" aria-hidden="true">' + '&times;' + 
                                            '</button>' + 
                                            '<strong>Sorry</strong>, something went wrong. ' +
                                            'You have not been charged. Please try again.' +
                                         '</div>');
                                }
                            },
                            error: function(data) {
                                $('#buynowresponse').after(
                                    '<div class="alert alert-danger alert-dismissable">'+
                                        '<button type="button" class="close" ' + 
                                            'data-dismiss="alert" aria-hidden="true">' + '&times;' + 
                                        '</button>' + 
                                        '<strong>Sorry</strong>, something went wrong. ' +
                                        'You have not been charged. Please try again.' +
                                     '</div>');
                            }
                        }); // end ajax call
                    }
                });
        ns.price = $('#stripePrice' + novel_id).val().trim();
        ns.description = "Single purchase of " + ns.novel_title;
        ns.currency = $('#stripeCurrency' + novel_id).val();
        // Open Checkout with further options
        handler.open({
            name: "Whythawk Limited (Qwyre)",
            description: ns.description,
            amount: parseInt(ns.price,10),
            currency: ns.currency
        });
        e.preventDefault();
        });
    }, false);
    $('[id^=forex_]').on('click', function (e) {
        var forex = this;
        var forex_id = forex.id.slice(6,9);
        var novel_id = forex.id.replace("forex_" + forex_id, "");
        var preorder_text = $('#novelPreorder' + novel_id).attr('value').trim();
        var base_price = parseFloat($('#basePrice' + novel_id).attr('value').trim());
        var next_price = $('#nextPrice' + novel_id).attr('value').trim();
        var select_price = parseFloat($(this).attr('data-value').trim());
        var new_price = (select_price * base_price);
        if (next_price) {
            next_price = (parseFloat(next_price) * select_price/100);
        }
        switch (this.id) {
            case 'forex_usd' + novel_id:
                $('#stripeButton' + novel_id).html(preorder_text + " for $ " + (new_price/100).toFixed(2));
                $("#stripeCurrency" + novel_id).val('USD');
                if (next_price) {
                    $('#nextPriceText' + novel_id).html("Price increases to $ " + next_price.toFixed(2));
                }
                break;
            case 'forex_gbp' + novel_id:
                $('#stripeButton' + novel_id).html(preorder_text + " for &pound; " + (new_price/100).toFixed(2));
                $("#stripeCurrency" + novel_id).val('GBP');
                if (next_price) {
                    $('#nextPriceText' + novel_id).html("Price increases to &pound; " + next_price.toFixed(2));
                }
                break;
            case 'forex_eur' + novel_id:
                $('#stripeButton' + novel_id).html(preorder_text + " for &euro; " + (new_price/100).toFixed(2));
                $("#stripeCurrency" + novel_id).val('EUR');
                if (next_price) {
                    $('#nextPriceText' + novel_id).html("Price increases to &euro; " + next_price.toFixed(2));
                }
                break;
            case 'forex_btc' + novel_id:
                $('#stripeButton' + novel_id).html(preorder_text + " for &#3647; " + (new_price/100).toFixed(4));
                if (next_price) {
                    $('#nextPriceText' + novel_id).html("Price increases to &#3647; " + next_price.toFixed(4));
                }
                // Stripe needs this to be in USD for 10min period conversion rate
                var USD_price = parseFloat($('#forex_usd' + novel_id).attr('data-value').trim());
                new_price = (USD_price * base_price);
                $("#stripeCurrency" + novel_id).val('USD');
                break;
        }
        $("#stripePrice" + novel_id).val(new_price.toFixed());
        e.preventDefault();
    });
    $("#buytrigger").change(function () {
        var next_page = '<a href="' + $('#nextpagelink').val()
            + '" class="btn btn-md btn-read nextchapter pull-right" >Next chapter</a>';
        $('#nextpage').html(next_page);
    });
    if ($('#nextPriceText').length) {
        $('#nextbutton').addClass("two-line");
    }
    if ($('#two-line').length) {
        if ($('#nextbutton').length) {
            $('#nextbutton').addClass("two-line");
        } else {
            $('#two-line').addClass("two-line");
        }
    }
});