from django.shortcuts import get_object_or_404, get_list_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.forms.models import modelformset_factory
from django.core.urlresolvers import reverse
from django.conf import settings

import stripe
import simplejson as json #Decimal value support
from boto.s3.connection import S3Connection
from boto.exception import AWSConnectionError, S3DataError, S3ResponseError
from decimal import Decimal
from guardian.shortcuts import get_objects_for_user
from bs4 import BeautifulSoup

from ..sqwyre.models import Novel, Token, Reader
from ..sqwyre.forms import NovelForm, TokenForm, BulkBuyForm
from ..wiqi.models import Wiqi
from ..wiqi.forms import WiqiPriceForm
from ..wiqi import wiqi as wiqid
from ..qwyre import qwyre as sqwyd
from ..snippets.diff2merge import docxtract, xtractemail
from ..snippets.mailem import send_email
from ..snippets.forex import get_forex

EMAIL_SUBJECT = {'gift_lend': ' has lent you a copy of ',
                 'gift_purchase': ' has sent you a copy of ',
                 'issue_lend': 'You have lent out copies of ',
                 'issue_purchase': 'Your purchase of ',
                 'purchase': 'Your purchase of ',
                 'refund': 'Your refund for '
                 }

def view_novel(request, novel_surl=None, template_name="qwyre/index.html"):
    if novel_surl:
        novel_object = get_object_or_404(Novel, surl=novel_surl)
    else:
        novel_object = Novel.objects.all()
        if not novel_object:
            return redirect("create_novel")
        novel_object = novel_object[0]
    user_has_purchased = sqwyd.user_has_purchased(request, novel_object)
    page_title = novel_object.title
    page_subtitle = "Start Reading"
    page_class = "home"
    nav_set = None
    # forex and pricing settings
    fx = get_forex()
    fxd = novel_object.defaultcurrency
    page_price = novel_object.sentinal.price
    show_buy = False
    if novel_object.show_buy:
        show_buy = True
    if request.user.is_authenticated():
        can_read = request.user.reader.can_read(novel_object)
        if can_read == "purchased":
            show_buy = False
        elif can_read != "borrowed" and request.user.reader.current_price > page_price:
            page_price = request.user.reader.current_price
    return render(request, template_name, locals())

def view_chapter(request, wiqi_surl, wiqi_type=None, template_name="qwyre/view_chapter.html",
                 nav_type="view", permission=None):
    """
    Return chapter view, or the view of the stack (item or list) from the wiqi.
    """
    wiqi_object = wiqid.get_wiqi_object_or_404(wiqi_surl, request.user, wiqi_type, permission,
                                               nav_type)
    if wiqi_object:
        # If no wiqi object, user has no rights to view, and must login or buy...
        # nav_set = wiqid.get_wiqi_nav(request, nav_type, wiqi_object)
        template_name = "qwyre/view_%s.html" % wiqi_object.get_class
        try:
            chapter_title = wiqi_object.stack.title
            # Kludge for novel title
            novel_object = wiqi_object.stack.wiqi.novel_chapterlist.all()[0]
        except AttributeError:
            # It's from a wiqistack
            chapter_title = wiqi_object.title
            novel_object = wiqi_object.wiqi.novel_chapterlist.all()[0]
            nav_title = "stack"
        user_has_purchased = sqwyd.user_has_purchased(request, novel_object)
        page_title = novel_object.title
        page_subtitle = chapter_title
        # Prepare for viewing next_wiqi
        try:
            next_wiqi = wiqi_object.next_wiqi
        except:
            # It's a wiqi_object
            next_wiqi = wiqi_object.wiqi.next_wiqi
        if next_wiqi:
            can_read_next = False
            if request.user.is_authenticated():
                can_read_next = request.user.reader.can_read(next_wiqi)
            if not can_read_next:
                can_read_next = next_wiqi.read_if
        # forex and pricing settings
        fx = get_forex()
        fxd = novel_object.defaultcurrency
        try:
            page_price = wiqi_object.price
        except:
            # It's a wiqi_object
            page_price = wiqi_object.wiqi.price
        show_buy = False
        if novel_object.show_buy:
            show_buy = True
        if request.user.is_authenticated():
            can_read = request.user.reader.can_read(novel_object)
            if can_read == "purchased":
                show_buy = False
            elif can_read == "borrowed":
                page_price = novel_object.sentinal.price
            elif request.user.reader.current_price > page_price:
                page_price = request.user.reader.current_price
        if show_buy and next_wiqi and page_price < next_wiqi.price:
            # Only appears if the next page price > than user current price
            next_price = next_wiqi.price
    else:
        return redirect('index')
    if request.is_ajax():
        return HttpResponse(json.dumps(nav_set), content_type="application/json")
    else:
        return render(request, template_name, locals())

@login_required
def test_novel(request, novel_surl, template_name="qwyre/test_novel.html"):
    if not request.user.is_superuser:
        return Http404
    novel_object = get_object_or_404(Novel, surl=novel_surl)
    user_has_purchased = sqwyd.user_has_purchased(request, novel_object)
    page_title = novel_object.title
    data = request.META
    return render(request, template_name, locals())

def view_chapters(request, novel_surl, template_name="qwyre/view_chapters.html"):
    novel_object = get_object_or_404(Novel, surl=novel_surl)
    user_has_purchased = sqwyd.user_has_purchased(request, novel_object)
    page_title = novel_object.title
    page_subtitle = "Chapters"
    chapter_objects = json.loads(novel_object.chapterformat)
    # forex and pricing settings
    fx = get_forex()
    fxd = novel_object.defaultcurrency
    page_price = novel_object.sentinal.price
    show_buy = True
    can_read = False
    if request.user.is_authenticated():
        can_read = request.user.reader.can_read(novel_object)
        if can_read == "purchased":
            show_buy = False
        elif can_read != "borrowed" and request.user.reader.current_price > page_price:
            page_price = request.user.reader.current_price
    if not novel_object.show_buy:
        show_buy = False
        can_read = True
    return render(request, template_name, locals())

def buy_novel(request, novel_surl, template_name="qwyre/buy_novel.html"):
    novel_object = get_object_or_404(Novel, surl=novel_surl)
    page_title = novel_object.title
    buy_response = {'response': 'failed'}
    if request.method == "POST":
        # Set your secret key: remember to change this to your live secret key in production
        stripe_key = settings.STRIPE_PUBLISHABLE_KEY
        stripe.api_key = settings.STRIPE_SECRET_KEY
        # Get the credit card details submitted by the form or via ajax
        data = request.POST
        # Process and test emails
        stripe_emails = xtractemail(data["stripeEmails"])
        if sqwyd.check_fraud(request.user, novel_object, data, len(stripe_emails)):
            # Fraudulent or a problem
            return HttpResponse(json.dumps(buy_response), content_type="application/json")
        # Create the charge on Stripe's servers - this will charge the user's card
        try:
            # If Bitcoin, process a BitcoinReceiver first
            if data["stripeBitcoin"] == "true":
                #receiver = stripe.BitcoinReceiver.retrieve(data["stripeToken"])
                #receiver(refund_mispayments=True)
                charge = stripe.Charge.create(
                    amount=data["stripePrice"], # amount in pence
                    currency=data["stripeCurrency"],
                    source=data["stripeToken"],
                    description=data["stripeDescription"],
                    )
            else:
                charge = stripe.Charge.create(
                    amount=data["stripePrice"], # amount in pence
                    currency=data["stripeCurrency"],
                    card=data["stripeToken"],
                    description=data["stripeDescription"],
                    statement_description=novel_object.title,
                    )
        except stripe.CardError, e:
          # The card has been declined
            if request.is_ajax():
                return HttpResponse(json.dumps(buy_response), content_type="application/json")
            return render(request, template_name, locals())

        # Create a Token and associate this charge with it for each email recipient
        kwargs = {}
        kwargs["creator_ip"] = sqwyd.get_user_ip(request)
        kwargs["country_code"] = sqwyd.get_user_country(request)
        kwargs["novel"] = novel_object
        # Don't ask me why this works, but it does ... ask Stripe.
        kwargs["charge"] = json.loads(json.dumps(charge))
        kwargs["currency"] = data["stripeCurrency"].lower()
        kwargs["stripe_id"] = charge["id"]
        kwargs["is_purchased"] = True
        kwargs["is_preorder"] = novel_object.is_preorder
        if request.user.is_authenticated():
            kwargs["creator"] = request.user
        else:
            kwargs["creator"] = None
        send_list = []
        send_subject = EMAIL_SUBJECT[data['template']] + novel_object.title
        if data['template'] == 'gift_purchase':
            send_subject = request.user.username + send_subject #request.user.facebook_name + send_subject
        for e in stripe_emails:
            kwargs["recipient"] = e
            kwargs["price"] = Decimal(str(data["stripePrice"]))/len(stripe_emails)/100
            token_object = Token()
            token_object.issue(**kwargs)
            send_list.append(token_object)
            email_kwargs = {'to': token_object.recipient,
                            'subject': send_subject,
                            'template': data['template'],
                            'context': {'token_object': token_object,
                                        # https://docs.djangoproject.com/en/1.7/ref/request-response/#django.http.HttpRequest.get_host
                                        }
                            }
            if token_object.recipient:
                # Not everyone has an email address...
                send_email(**email_kwargs)
        # prepare ajax response
        buy_response = {'response': 'success',
                         'registered': False,
                         'link': token_object.get_token_redemption_url()}
        # if logged in and buying for self (and we, therefore, know there is only one token)
        if request.user.is_authenticated() and data.get("selfPurchase", False) == "true":
            kwargs["redeemer"] = request.user
            kwargs["redeemer_ip"] = sqwyd.get_user_ip(request)
            token_object.redeem(**kwargs)
            buy_response['registered'] = True
            buy_response['link'] = reverse('issue_tokens', kwargs={'novel_surl': novel_object.surl})
        # process send_list for logged-in users with emails...
        if request.user.is_authenticated() and data['template'] == 'gift_purchase' and request.user.email:
            email_kwargs['to'] = request.user.email
            email_kwargs['subject'] = EMAIL_SUBJECT['issue_purchase'] + novel_object.title
            email_kwargs['template'] = 'issue_purchase'
            email_kwargs['context']['token_list'] = send_list
            send_email(**email_kwargs)
    if request.is_ajax():
        return HttpResponse(json.dumps(buy_response), content_type="application/json")
    return render(request, template_name, locals())

def novel_settings(request, novel_surl):
    if request.is_ajax():
        novel_object = get_object_or_404(Novel, surl=novel_surl)
        a = sqwyd.get_user_ip(request)
        response_dict = {'settings': {
            'stripe_key': settings.STRIPE_PUBLISHABLE_KEY,
            'bulk_discount': novel_object.discountpercent,
            'bulk_volume': novel_object.discountvolume,
            'bulk_price': novel_object.sentinal.price,
            'novel_price': novel_object.sentinal.price,
            'novel_title': novel_object.title,
            'user_email': ''
            }
        }
        if request.user.is_authenticated():
            response_dict['settings']['user_email'] = request.user.email
        return HttpResponse(json.dumps(response_dict), content_type="application/json")
    return Http404

def set_chapters(request, novel_surl):
    if request.is_ajax():
        novel_object = get_object_or_404(Novel, surl=novel_surl)
        chapter_response = {'response': 'failed'}
        if request.method == "POST":
            if request.user.is_authenticated():
                data = request.POST
                novel_object.chapterformat = data['chapterformat']
                novel_object.save()
                chapter_response = {'response': 'success'}
        else:
            chapter_response = {'response': 'success',
                                'chapterformat': novel_object.chapterformat}
        return HttpResponse(json.dumps(chapter_response), content_type="application/json")
    return Http404

@login_required
def resend_token(request, token_surl, template_name="qwyre/issue_tokens.html"):
    """
    Resend a valid token (and update recepient if that data is provided)
    """
    resend_response = {'response': 'failed'}
    if request.method == "POST":
        token_object = get_object_or_404(Token, surl=token_surl)
        page_title = token_object.novel.title
        data = request.POST
        if token_object.edit(data["recipient"]):
            try:    
                resend_response = {'response': 'success',
                                   'recipient': data["recipient"]}
                email_kwargs = {'to': token_object.recipient,
                                'subject': request.user.username + EMAIL_SUBJECT[data['template']] + token_object.novel.title,
                                'template': 'gift_purchase',
                                'context': {'token_object': token_object,
                                            'website': request.META['HTTP_HOST'],
                                            'days': token_object.novel.lenddays
                                            }
                                }
                send_email(**email_kwargs)
            except Exception:
                resend_response = {'response': 'failed'}
    if request.is_ajax():
        return HttpResponse(json.dumps(resend_response), content_type="application/json")
    return render(request, template_name, locals())

@login_required
def issue_tokens(request, novel_surl, template_name="qwyre/issue_tokens.html"):
    """
    Issue and manage a list of tokens to users identified by book owner:
        - Lend up to TOKEN_LIMIT copies of novel;
        - Bulk-buy an unlimited amount, unlocking BULK_DISCOUNT at specified BULK_VOLUME;
        - Resend, reallocate and rename valid tokens;
    """
    novel_object = get_object_or_404(Novel, surl=novel_surl)
    user_has_purchased = sqwyd.user_has_purchased(request, novel_object)
    if request.user.is_superuser:
        return redirect('price_novel', novel_surl=novel_object.surl)
    if not request.user.reader.can_read(novel_object) == "purchased":
        return render(request, '404.html', status=403)
    page_title = novel_object.title
    page_subtitle = "Share and Manage"
    # Where 'issue' is actually 'lent' ... 
    token_issued_list = Token.query.issued_list(request.user, novel_object)
    token_refund_list = Token.query.valid_purchased(request.user, True)
    token_purchased_list = Token.query.valid_purchased(request.user, False).all()
    # only need one if intend to download, doesn't matter which since they did buy
    token_download = request.user.reader.current_token(purchased=True)
    tokens_remaining = novel_object.lendnumber - len(token_issued_list)
    total_duration = novel_object.lenddays
    total_tokens = novel_object.lendnumber
    pro_disc = novel_object.discountpercent
    pro_bulk = novel_object.discountvolume
    TokenFormSet = modelformset_factory(Token, form=TokenForm, extra=tokens_remaining)
    RefundFormSet = modelformset_factory(Token, form=TokenForm, extra=0)
    # forex settings
    fx = get_forex()
    fxd = novel_object.defaultcurrency
    fxp = int(novel_object.sentinal.price*100)
    if request.method == "POST":
        send_list = []
        # http://stackoverflow.com/questions/1395807/proper-way-to-handle-multiple-forms-on-one-page-in-django
        # https://docs.djangoproject.com/en/1.7/topics/forms/formsets/#using-more-than-one-formset-in-a-view
        if "issue_tokens" in request.POST or "refund_tokens" in request.POST:
            if "issue_tokens" in request.POST:
                issue_token_formset = TokenFormSet(request.POST, queryset=token_issued_list.all(), prefix='issue')
                refund_token_formset = RefundFormSet(queryset=token_refund_list.all(), prefix='refund')
                formset = issue_token_formset
            else:
                issue_token_formset = TokenFormSet(request.POST, queryset=token_issued_list.all(), prefix='issue')
                refund_token_formset = RefundFormSet(request.POST, queryset=token_refund_list.all(), prefix='refund')
                formset = refund_token_formset
            if issue_token_formset.is_valid():
                kwargs = {}
                kwargs["creator"] = request.user
                kwargs["creator_ip"] = sqwyd.get_user_ip(request)
                kwargs["country_code"] = sqwyd.get_user_country(request)
                kwargs["novel"] = novel_object
                for form in issue_token_formset.cleaned_data:
                    do_send = False
                    if form:
                        if not form['id']:
                            kwargs['recipient'] = form['recipient']
                            token_object = Token()
                            token_object.issue(**kwargs)
                            tokens_remaining -= 1
                        elif form['id'].is_valid:
                            if form['id'].recipient != form['recipient']:
                                form['id'].recipient = form['recipient']
                                form['id'].save()
                            token_object = form['id']
                        if not form['id'] or form['id'].is_valid:
                            # Resend to existing recipients too
                            send_list.append(token_object)
                            do_send = True
                        if do_send:
                            try:
                                email_kwargs = {'to': token_object.recipient,
                                                'subject': request.user.username + EMAIL_SUBJECT['gift_lend'] +
                                                novel_object.title,
                                                'template': 'gift_lend',
                                                'context': {'token_object': token_object,
                                                            'website': request.META['HTTP_HOST'],
                                                            'days': total_duration
                                                            }
                                                }
                                send_email(**email_kwargs)
                            except Exception:
                                continue # without sending, obviously
        # process the send_list to the account manager
        if send_list and request.user.email:
            email_kwargs['to'] = request.user.email
            email_kwargs['subject'] = EMAIL_SUBJECT['issue_lend'] + novel_object.title
            email_kwargs['template'] = 'issue_lend'
            email_kwargs['context']['token_list'] = send_list
            send_email(**email_kwargs)        
        #if request.is_ajax():
        #    return HttpResponse(json.dumps({'token': token_object.surl}), content_type="application/json")
    else:
        issue_token_formset = TokenFormSet(queryset=token_issued_list.all(), prefix='issue')
        refund_token_formset = RefundFormSet(queryset=token_refund_list.all(), prefix='refund')
    return render(request, template_name, locals())

def redeem_token(request, token_surl, template_name="qwyre/redeem_token.html"):
    token_object = get_object_or_404(Token, surl=token_surl)
    user_has_purchased = sqwyd.user_has_purchased(request, token_object.novel)
    if not token_object.is_purchased:
        days = token_object.novel.lenddays
    show_refund = False
    if request.user.is_authenticated():
        # check if user already purchased this item and ignore redemption if they do
        if request.user.reader.can_read(token_object.novel) == "purchased":
            return redirect("issue_tokens", novel_surl=token_object.novel.surl)
        if token_object.is_valid:
            kwargs = request.POST.dict()
            kwargs["redeemer"] = request.user
            kwargs["redeemer_ip"] = sqwyd.get_user_ip(request)
            token_object.redeem(**kwargs)
            if token_object.is_purchased:
                return redirect("issue_tokens", novel_surl=token_object.novel.surl)
            return redirect("view_wiqi", wiqi_surl=token_object.novel.sentinal.surl)
    else:
        expiry = settings.S3_TIMER
        if token_object.is_valid and \
            token_object.is_purchased and \
            not token_object.creator:
            show_refund = True
            show_bitcoin_refund = False
        if show_refund and not token_object.charge["card"]:
            show_bitcoin_refund = True
    page_title = token_object.novel.title
    novel_object = token_object.novel
    page_subtitle = "Redemption"
    page_class = "home"
    pro_disc = novel_object.discountpercent
    pro_bulk = novel_object.discountvolume
    pro_lend = novel_object.lendnumber
    pro_days = novel_object.lenddays
    return render(request, template_name, locals())

def download_novel(request, token_surl, template_name="qwyre/download_novel.html"):
    """
    Return download links valid for S3_TIMER to all files in the appropriate S3 bucket.
    Only return links if:
        1. token is purchased and valid (for anonymous download, disable it);
        2. token is purchased and user is authenticated;
    Links will be valid for a specific amount of time.
    """
    token_object = get_object_or_404(Token, surl=token_surl)
    can_download = False
    cancel_token = False
    downloads = {'response': 'failure'}
    if token_object.is_purchased and token_object.is_valid:
        kwargs = {}
        kwargs["redeemer"] = None
        if request.user.is_authenticated():
            kwargs["redeemer"] = request.user
        kwargs["redeemer_ip"] = sqwyd.get_user_ip(request)
        can_download = True
    if token_object.is_purchased and request.user.is_authenticated():
        can_download = True
    if can_download:
        # Generate the time-limited AWS S3 link/s
        # http://boto.readthedocs.org/en/latest/ref/s3.html#boto.s3.key.Key.generate_url
        # http://ceph.com/docs/next/radosgw/s3/python/
        # http://boto.readthedocs.org/en/latest/boto_config_tut.html may need is_secure=False, validate_certs=False
        try:
            conn = S3Connection(settings.S3_ACCESS_KEY_ID, settings.S3_SECRET_ACCESS_KEY, is_secure=False)
            bucket = conn.get_bucket(settings.S3_EBOOK_BUCKET)
            # prepare response
            downloads = {'response': 'success',
                         'timer': str(settings.S3_TIMER),
                         'links': {}
            }
            # https://code.google.com/p/boto/wiki/GetAllKeys
            for k in bucket.list(settings.S3_EBOOK_DOWNLOAD_FOLDER):
                ky = k.key.replace(settings.S3_EBOOK_DOWNLOAD_FOLDER + "/", "")
                if ky:
                    downloads['links'][ky] = k.generate_url(settings.S3_TIMER)
            if token_object.is_purchased and token_object.is_valid:
                cancel_token = True
        except (AWSConnectionError, S3DataError, S3ResponseError) as e:
            cancel_token = False
            downloads = {'response': 'failure'}
        if cancel_token:
            # i.e. only do this after the download links have been generated in case this whole thing crashes
            token_object.redeem(**kwargs)
    if request.is_ajax():
        return HttpResponse(json.dumps(downloads), content_type="application/json")
    return render(request, template_name, locals())

def refund_token(request, token_surl, template_name="qwyre/refund_token.html"):
    """
    Refund a valid token (even where part of a bulk-buy).
    If the user is not logged in, then only refund if the creator is anonymous.
    Users can't request refunds for tokens they didn't buy for themselves.
    """
    token_object = get_object_or_404(Token, surl=token_surl)
    page_title = token_object.novel.title
    refund_response = {'response': 'failure'}
    token_refund = False
    data = request.POST
    if token_object.is_valid and token_object.is_purchased:
        if request.user.is_authenticated() or not token_object.creator:
            token_refund = True
        if not token_object.charge["card"] and (data["bitcoin_refund"] == "false" or data["bitcoin_refund"] == ""):
            token_refund = False # No bitcoin address for refund.
    if token_refund:
        stripe_key = settings.STRIPE_PUBLISHABLE_KEY
        # Set your secret key: remember to change this to your live secret key in production
        stripe.api_key = settings.STRIPE_SECRET_KEY
        # Create the refund on Stripe's servers
        try:
            # Get the token key
            stripe_charge = stripe.Charge.retrieve(token_object.charge["id"])
            if token_object.charge["card"]:
                stripe_refund = stripe_charge.refunds.create(
                    amount = int(token_object.price * 100), # amount in pence / cents
                    reason = "requested_by_customer",
                  )
            else:
                try:
                    stripe_refund = stripe_charge.refunds.create(
                        refund_address = data["bitcoin_refund"],
                        amount = int(token_object.price * 100), # amount in pence / cents
                      )
                except stripe.InvalidRequestError, e:
                    # Stripe insists on a single repayment wallet address
                    stripe_refund = stripe_charge.refunds.create(
                        amount = int(token_object.price * 100), # amount in pence / cents
                      )
            token_object.charge = stripe_refund
            token_object.is_valid = False
            token_object.is_purchased = False
            token_object.save()
            refund_response = {'response': 'success'}
            email_kwargs = {'to': token_object.recipient,
                            'subject': EMAIL_SUBJECT['refund'] + token_object.novel.title,
                            'template': 'refund',
                            'context': {'token_object': token_object,
                                        'website': request.META['HTTP_HOST']
                                        }
                            }
            send_email(**email_kwargs)
        except stripe.CardError, e: 
            # The refund has been declined
            refund_response = {'response': 'failure'}
    if request.is_ajax():
        return HttpResponse(json.dumps(refund_response), content_type="application/json")
    return render(request, template_name, locals())

@login_required
def create_novel(request, template_name="qwyre/create_novel.html"):
    """
    Create the novel but does not yet populate the chapters.
    """
    if not request.user.is_superuser:
        return render(request, '404.html', status=403)
    if request.method == "POST":
        novel_form = NovelForm(request.POST)
        if novel_form.is_valid():
            kwargs = request.POST.dict()
            kwargs["creator"] = request.user
            kwargs["creator_ip"] = sqwyd.get_user_ip(request)
            novel_object = Novel()
            novel_object.set(**kwargs)
            novel_object.assign_all_perm(request.user)
            if request.is_ajax():
                return HttpResponse(json.dumps({'novel': novel_object.surl}), content_type="application/json")
    else:
        novel_form = NovelForm()
    page_title = "Qwyre - Create Novel"
    return render(request, template_name, locals())

@login_required
def upload_docx(request, template_name="qwyre/create_novel.html"):
    """
    Receive a file and return the components necessary for the user to organise and save it.
    """
    if not request.user.is_superuser:
        return render(request, '404.html', status=403)
    usr_ip = sqwyd.get_user_ip(request)
    if request.is_ajax():
        # http://stackoverflow.com/questions/1208067/wheres-my-json-data-in-my-incoming-django-request
        kwargs = request.POST.dict()
        kwargs["file"] = request.FILES.get("file", "")
        tree = docxtract(kwargs["file"])
        return HttpResponse(json.dumps(tree), content_type="application/json")
    return render(request, template_name, locals())

# Next too https://docs.djangoproject.com/en/dev/topics/auth/default/#the-permission-required-decorator
@login_required
def organise_novel(request, novel_surl, template_name="qwyre/create_novel.html", permission="can_edit"):
    """
    By default, permits the review of the Book wiqi, reorganising of chapter order,
    rights management and that sort of thing. With time, perhaps, this can be
    extended to the other wiqis...
    """
    if not request.user.is_superuser:
        return render(request, '404.html', status=403)
    novel_object = get_object_or_404(Novel, surl=novel_surl)
    page_title = novel_object.title
    page_subtitle = "Organise"
    #if not request.user.has_perm(permission, novel_object):
    #    raise Http404
    if request.method == "POST":
        if request.is_ajax():
            kwargs = json.loads(request.body)
            kwargs["common"] = {"creator": request.user,
                                "creator_ip": sqwyd.get_user_ip(request),
                                "WiqiStack": wiqid.get_wiqi_or_404('text'),
                                "price": novel_object.defaultprice,
                                "is_live_from": novel_object.is_live_from,
                                }
            novel_object = novel_object.add_chapters(**kwargs)
            return HttpResponse(json.dumps({'response': 'success'}), content_type="application/json")
    return render(request, template_name, locals())

@login_required
def price_novel(request, novel_surl, template_name="qwyre/price_novel.html", permission="can_edit"):
    """
    Set the price and view permissions required for each chapter.
    """
    if not request.user.is_superuser:
        return render(request, '404.html', status=403)
    novel_object = get_object_or_404(Novel, surl=novel_surl)
    page_title = novel_object.title
    page_subtitle = "Pricing and Management"
    if not request.user.has_perm(permission, novel_object):
        return render(request, '404.html', status=403)
    # https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#model-formsets
    WiqiPriceFormSet = modelformset_factory(Wiqi, form=WiqiPriceForm, extra=0)
    if request.method == "POST":
        formset = WiqiPriceFormSet(request.POST, queryset=novel_object.chapterlist.all())
        if formset.is_valid():
            formset.save()
    else:
        formset = WiqiPriceFormSet(queryset=novel_object.chapterlist.all())
    return render(request, template_name, locals())

@login_required
def market_tokens(request, novel_surl):
    """
    Email the admin a list of tokens for marketing purposes.
    These will be both valid and purchased.
    """
    if not request.user.is_superuser:
        return render(request, '404.html', status=403)
    novel_object = get_object_or_404(Novel, surl=novel_surl)
    if request.method == "POST":
        if request.is_ajax():
            market_response = {'response': 'failure'}
            data = request.POST
            # Process and test emails
            recipients = xtractemail(data["recipients"])
            from_address = "%s <%s>" % (request.user.username, request.user.email)
            kwargs = {}
            kwargs["creator"] = request.user
            kwargs["creator_ip"] = sqwyd.get_user_ip(request)
            kwargs["novel"] = novel_object
            kwargs["is_purchased"] = True
            send_list = []
            for r in recipients:
                kwargs["recipient"] = r
                token_object = Token()
                token_object.issue(**kwargs)
                send_list.append(token_object)
                if data["custom"] and data["subject"]:
                    email_kwargs = {'to': token_object.recipient,
                                    'from': from_address,
                                    'subject': data['subject'],
                                    'template': data['custom'],
                                    'context': {'token_object': token_object}
                                    }
                    send_email(**email_kwargs)
            if send_list:
                email_kwargs = {'to': request.user.email,
                                'subject': EMAIL_SUBJECT['issue_purchase'] + novel_object.title,
                                'template': 'issue_purchase',
                                'context': {'token_object': token_object,
                                            # https://docs.djangoproject.com/en/1.7/ref/request-response/#django.http.HttpRequest.get_host
                                            'token_list': send_list
                                            }
                                }
                send_email(**email_kwargs)
                market_response = {'response': 'success'}
            return HttpResponse(json.dumps(market_response), content_type="application/json")
    raise Http404 

@login_required
def administer_novel(request, template_name="qwyre/administer_novel.html", permission="can_edit"):
    """
    Present a list of novels and permit actions.
    """
    if not request.user.is_superuser:
        return Http404
    novel_objects = get_objects_for_user(request.user, permission, klass=Novel)
    page_title = "Qwyre List"
    return render(request, template_name, locals())

def view_legal(request, novel_surl, template_name="qwyre/legal.html"):
    novel_object = get_object_or_404(Novel, surl=novel_surl)
    user_has_purchased = sqwyd.user_has_purchased(request, novel_object)
    page_title = novel_object.title
    return render(request, template_name, locals())

@login_required
def reader_update(request):
    """
    Update the details for this user.
    """
    if request.method == "POST":
        if request.is_ajax():
            usr_response = {'response': 'failure'}
            data = request.POST
            # Process and test emails
            usr_email = xtractemail(data["email"])[0]
            usr_name = data["name"]
            if usr_email and usr_name:
                request.user.email = usr_email
                request.user.username = usr_name
                request.user.optout = False
                if data["optout"] == "true":
                    request.user.optout = True
                request.user.save()
            usr_response = {'response': 'success'}
            return HttpResponse(json.dumps(usr_response), content_type="application/json")
    raise Http404

def testing_novel(request, template_name="qwyre/testing_novel.html"):
    return render(request, template_name, locals())