from django.conf.urls import patterns, include, url

# Django 1.9 url patterns
from ..sqwyre import views

urlpatterns = [
                ###########################################
                ### Testing                             ###
                ###########################################
                # url(r"^testing/", views.testing_novel,
                #     {"template_name": "sqwyre/testing_novel.html"},
                #     name="testing_novel"),
                # url(r"^(?P<novel_surl>[-\w]+)/test/", views.test_novel,
                #     {"template_name": "sqwyre/test_novel.html"},
                #     name="test_novel"),
                ###########################################
                ### Author Administration Views         ###
                ###########################################
                # Create / Edit Novel
                url(r"^create/", views.create_novel,
                    {"template_name": "sqwyre/create_novel.html"},
                    name="create_novel"),
                # Organise the novel
                url(r"^(?P<novel_surl>[-\w]+)/organise/", views.organise_novel,
                    {"template_name": "sqwyre/create_novel.html", "permission":"can_edit"},
                    name="organise_novel"),
                # Set novel chapter pricing
                url(r"^(?P<novel_surl>[-\w]+)/managing/", views.price_novel,
                    {"template_name": "sqwyre/price_novel.html", "permission":"can_edit"},
                    name="price_novel"),
                url(r"^(?P<novel_surl>[-\w]+)/(?P<from_db>[-\w]+)/(?P<region_slug>[-\w]+)/pricing/",
                    views.set_global_pricing,
                    {"template_name": "sqwyre/global_pricing.html", "permission":"can_edit"},
                    name="global_pricing"),
                ## Administer novel
                # url(r"^sortit/", "administer_novel",
                #    {"template_name": "sqwyre/administer_novel.html", "permission":"can_edit"},
                #    name="administer_novel"),
                ###########################################
                ### Javascript Automation               ###
                ###########################################
                # JSONResponse settings
                url(r"^(?P<novel_surl>[-\w]+)/settings/", views.novel_settings,
                    name="novel_settings"),
                url(r"^(?P<novel_surl>[-\w]+)/setcontents/", views.set_contents,
                    name="set_contents"),
                # Upload Docx
                url(r"^docxtract/", views.upload_docx,
                    {"template_name": "sqwyre/docxtract.html"},
                    name="upload_docx"),
                ###########################################
                ### Purchase and Manage Tokens          ###
                ###########################################
                # Issue and Redeem tokens
                url(r"^(?P<novel_surl>[-\w]+)/tokens/issue/", views.issue_tokens,
                    {"template_name": "sqwyre/issue_tokens.html"},
                    name="issue_tokens"),
                url(r"^tokens/redeem/(?P<token_surl>[-\w]+)/", views.redeem_token,
                    {"template_name": "sqwyre/redeem_token.html"},
                    name="redeem_token"),
                url(r"^tokens/refund/(?P<token_surl>[-\w]+)/", views.refund_token,
                    {"template_name": "sqwyre/refund_token.html"},
                    name="refund_token"),
                url(r"^(?P<novel_surl>[-\w]+)/tokens/market/", views.market_tokens,
                    name="market_tokens"),
                url(r"^(?P<novel_surl>[-\w]+)/sendreminder/", views.preorder_reminder,
                    name="preorder_reminder"),
                # Email token link to user
                url(r"^tokens/resend/(?P<token_surl>[-\w]+)/", views.resend_token,
                    {"template_name": "sqwyre/issue_tokens.html"},
                    name="resend_token"),
                # Buy and bulk-buy novel
                url(r"^(?P<novel_surl>[-\w]+)/buy/", views.buy_novel,
                    {"template_name": "sqwyre/buy_novel.html"},
                    name="buy_novel"),             
                ###########################################
                ### Reader Purchase Views               ###
                ###########################################
                # Download books based on one-time link
                url(r"^download/(?P<token_surl>[-\w]+)/", views.download_novel,
                    {"template_name": "sqwyre/download_novel.html"},
                    name="download_novel"),
                # Update reader details if logged in
                url(r"^update/", views.reader_update, name="reader_update"),
                ###########################################
                ### Reader Views                        ###
                ###########################################
                # View Novel
                url(r"^(?P<novel_surl>[-\w]+)/$", views.view_novel,
                   {"template_name": "sqwyre/view_novel.html"},
                   name="view_novel"),
                # Static pages
                # url(r"^(?P<novel_surl>[-\w]+)/about/", views.view_novel,
                #     {"template_name": "sqwyre/about.html"},
                #     name="about"),
                url(r"^site/legal/", views.view_legal,
                    {"template_name": "sqwyre/legal.html"},
                    name="plain_legal"),
                url(r"^(?P<novel_surl>[-\w]+)/legal/", views.view_legal,
                    {"template_name": "sqwyre/legal.html"},
                    name="legal"),
                # View the chapters
                url(r"^(?P<novel_surl>[-\w]+)/contents/", views.view_contents,
                    {"template_name": "sqwyre/view_contents.html"},
                    name="view_contents"),
                # Novel retailers for other version
                url(r"^(?P<novel_surl>[-\w]+)/retailers/", views.view_special,
                    {"template_name": "sqwyre/retailers.html"},
                    name="view_retailers"),
                # Music playlist
                url(r"^(?P<novel_surl>[-\w]+)/notes/", views.view_special,
                    {"template_name": "sqwyre/playlist.html"},
                    name="view_playlist"),
                # Still on preorder
                # url(r"^(?P<novel_surl>[-\w]+)/soon/", views.view_preorder,
                #     {"template_name": "sqwyre/view_preorder.html"},
                #     name="view_preorder"),
                # url(r"^(?P<novel_surl>[-\w]+)/(?P<wiqi_surl>[-\w]+)/$", views.view_chapter,
                #    {"template_name": "sqwyre/view_chapter.html"},
                #    name="view_novel_chapter"),
                url(r"^w/(?P<wiqi_surl>[-\w]+)/", views.view_chapter,
                    {"template_name": "sqwyre/view_text.html", "nav_type":"view"},
                    name="view_wiqi"),
                url(r'^$', views.view_index, {"template_name": "sqwyre/index.html"},
                    name='index'),
                ]