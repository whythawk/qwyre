from django.conf.urls import patterns, include, url

# Django 1.9 url patterns
from ..qwyre import views

urlpatterns = [
                url(r"^testing/", views.testing_novel,
                    {"template_name": "qwyre/testing_novel.html"},
                    name="testing_novel"),
                # Create / Edit Novel
                url(r"^create/", views.create_novel,
                    {"template_name": "qwyre/create_novel.html"},
                    name="create_novel"),
                # Organise the novel
                url(r"^(?P<novel_surl>[-\w]+)/organise/", views.organise_novel,
                    {"template_name": "qwyre/create_novel.html", "permission":"can_edit"},
                    name="organise_novel"),
                # View the chapters
                url(r"^(?P<novel_surl>[-\w]+)/contents/", views.view_chapters,
                    {"template_name": "qwyre/view_chapters.html"},
                    name="view_chapters"),
                # Set novel chapter pricing
                url(r"^(?P<novel_surl>[-\w]+)/pricing/", views.price_novel,
                    {"template_name": "qwyre/price_novel.html", "permission":"can_edit"},
                    name="price_novel"),
                # Issue and Redeem tokens
                url(r"^(?P<novel_surl>[-\w]+)/tokens/issue/", views.issue_tokens,
                    {"template_name": "qwyre/issue_tokens.html"},
                    name="issue_tokens"),
                url(r"^tokens/redeem/(?P<token_surl>[-\w]+)/", views.redeem_token,
                    {"template_name": "qwyre/redeem_token.html"},
                    name="redeem_token"),
                url(r"^tokens/refund/(?P<token_surl>[-\w]+)/", views.refund_token,
                    {"template_name": "qwyre/refund_token.html"},
                    name="refund_token"),
                url(r"^(?P<novel_surl>[-\w]+)/tokens/market/", views.market_tokens,
                    name="market_tokens"),
                # Email token link to user
                url(r"^tokens/resend/(?P<token_surl>[-\w]+)/", views.resend_token,
                    {"template_name": "qwyre/issue_tokens.html"},
                    name="resend_token"),
                # Buy and bulk-buy novel
                url(r"^(?P<novel_surl>[-\w]+)/buy/", views.buy_novel,
                    {"template_name": "qwyre/buy_novel.html"},
                    name="buy_novel"),
                # Download books based on one-time link
                url(r"^download/(?P<token_surl>[-\w]+)/", views.download_novel,
                    {"template_name": "qwyre/download_novel.html"},
                    name="download_novel"),
                # JSONResponse settings
                url(r"^(?P<novel_surl>[-\w]+)/settings/", views.novel_settings,
                    name="novel_settings"),
                url(r"^(?P<novel_surl>[-\w]+)/setcontents/", views.set_chapters,
                    name="set_chapters"),
                # Upload Docx
                url(r"^docxtract/", views.upload_docx,
                    {"template_name": "qwyre/docxtract.html"},
                    name="upload_docx"),
                ## Administer novel
                # url(r"^sortit/", "administer_novel",
                #    {"template_name": "qwyre/administer_novel.html", "permission":"can_edit"},
                #    name="administer_novel"),
                # View Novel
                url(r"^(?P<novel_surl>[-\w]+)/$", views.view_novel,
                   {"template_name": "qwyre/index.html"},
                   name="view_novel"),
                url(r"^(?P<novel_surl>[-\w]+)/test/", views.test_novel,
                    {"template_name": "qwyre/test_novel.html"},
                    name="test_novel"),
                url(r"^(?P<novel_surl>[-\w]+)/about/", views.view_novel,
                    {"template_name": "qwyre/about.html"},
                    name="about"),
                url(r"^(?P<novel_surl>[-\w]+)/legal/", views.view_legal,
                    {"template_name": "qwyre/legal.html"},
                    name="legal"),
                url(r"^update/", views.reader_update, name="reader_update"),
                # url(r"^(?P<novel_surl>[-\w]+)/(?P<wiqi_surl>[-\w]+)/$", views.view_chapter,
                #    {"template_name": "qwyre/view_chapter.html"},
                #    name="view_novel_chapter"),
                url(r"^w/(?P<wiqi_surl>[-\w]+)/", views.view_chapter,
                    {"template_name": "qwyre/view_text.html", "nav_type":"view"},
                    name="view_wiqi"),
                url(r'^$', views.view_novel, {"template_name": "qwyre/index.html"},
                    name='index'),
                ]