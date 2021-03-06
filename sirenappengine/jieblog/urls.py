﻿from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'jieblog.applications.views.index'),
    (r'^post/(?P<post_slug>[^\.^/]+)/$', 'jieblog.applications.views.comment'),
    (r'^page/(?P<page>[^\.^/]+)/$', 'jieblog.applications.views.index'),
    (r'^post/$', 'jieblog.applications.views.index'),
    (r'^wiki/$', 'jieblog.wiki.views.wiki'),
    (r'^catagory/(?P<cat_slug>[^\.^/]+)/(?P<page>[^\.^/]+)/$', 'jieblog.applications.views.catagory'),
#archive view  
    (r'^archive/(?P<post_year>[^\.^/]+)/(?P<post_month>[^\.^/]+)/$', 'jieblog.applications.views.archive'),

#File Manager
    (r'^uploader/$', 'jieblog.applications.views.uploader'),
    (r'^filelist/$', 'jieblog.applications.views.filelist'),
    (r'^file/(?P<the_key>[^\.^/]+)/$', 'jieblog.applications.views.filedown'),
    (r'^uploader/(?P<pic_key>[^\.^/]+)/$', 'jieblog.applications.views.uploader'),
    (r'^delete/(?P<the_key>[^\.^/]+)/$', 'jieblog.applications.views.filedelete'),

    (r'^adminlink/$', 'jieblog.applications.views.add_site_link'),
    (r'^addfeaturelink/$', 'jieblog.applications.views.add_feature_link'),
    (r'^link/$', 'jieblog.applications.views.site_link'),
    (r'^quotation/$', 'jieblog.applications.views.quotation'),
    (r'^featurelink/$', 'jieblog.applications.views.feature_link'),
    (r'^edit/(?P<post_id>[^\.^/]+)/$', 'jieblog.applications.background.edit'),
    (r'^editfeature/(?P<feature_list_id>[^\.^/]+)/$', 'jieblog.applications.views.edit_feature'),
    (r'^editquotation/(?P<quotation_id>[^\.^/]+)/$', 'jieblog.applications.views.edit_quotation'),
    (r'^tag/(?P<post_tag>[^\.^/]+)/$', 'jieblog.applications.views.tags'),

#sitemap and feed
    (r'^feeds/$', 'jieblog.applications.views.sitemap'),
    (r'^sitemap/$', 'jieblog.applications.views.sitemap'),

# XML-RPC
#   (r'^rpc/', 'jieblog.applications.xmlrpc.rpc_handler'),
# Administration URL
    (r'^login/$', 'jieblog.applications.background.login'),    
    (r'^configdb/(?P<config_id>[^\.^/]+)/$', 'jieblog.applications.configdb.configdb'),
    (r'^setupdb/$', 'jieblog.applications.configdb.setupdb'),    
    (r'^list/$', 'jieblog.applications.background.list_post'),
    (r'^list/(?P<page>[^\.^/]+)/$', 'jieblog.applications.background.list_post'),
    (r'^remove/(?P<post_id>[^\.^/]+)/$', 'jieblog.applications.background.delete_post'),
    (r'^create/$', 'jieblog.applications.background.create'),
    (r'^cat/$', 'jieblog.applications.background.PostCat'),
    
#new admin interface
    (r'^admin/$', 'jieblog.applications.background.create'),
    (r'^admin/create/$', 'jieblog.applications.background.create'),
    (r'^admin/config/$', 'jieblog.applications.background.Config'),
    (r'^admin/manage/$', 'jieblog.applications.background.list_post'),
    (r'^admin/wiki/$', 'jieblog.wiki.views.write_wiki'),
    (r'^admin/edit/(?P<post_id>[^\.^/]+)/$', 'jieblog.applications.background.edit'),
    (r'^admin/catagory/$', 'jieblog.applications.background.PostCat'),
    (r'^admin/catagory/edit/(?P<cat_id>[^\.^/]+)/$', 'jieblog.applications.background.edit_cat'),
    (r'^admin/catagory/delete/(?P<cat_id>[^\.^/]+)/$', 'jieblog.applications.background.delete_cat'),
#test content
)

