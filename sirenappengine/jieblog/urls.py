from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'jieblog.applications.views.index'),
    (r'^post/(?P<post_id>[^\.^/]+)/$', 'jieblog.applications.views.comment'),
    (r'^page/(?P<page>[^\.^/]+)/$', 'jieblog.applications.views.index'),
    (r'^post/$', 'jieblog.applications.views.index'),

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
    (r'^feeds/$', 'jieblog.applications.views.feeds'),
    (r'^tag/(?P<post_tag>[^\.^/]+)/$', 'jieblog.applications.views.view_tag'),
# XML-RPC
     (r'^rpc/', 'jieblog.applications.xmlrpc.rpc_handler'),
# Administration URL
    (r'^login/$', 'jieblog.applications.background.login'),    
    (r'^configdb/(?P<config_id>[^\.^/]+)/$', 'jieblog.applications.configdb.configdb'),
    (r'^setupdb/$', 'jieblog.applications.configdb.setupdb'),    
    (r'^list/$', 'jieblog.applications.background.list_post'),
    (r'^list/(?P<page>[^\.^/]+)/$', 'jieblog.applications.background.list_post'),
    (r'^remove/(?P<post_id>[^\.^/]+)/$', 'jieblog.applications.background.delete_post'),
    (r'^create/$', 'jieblog.applications.background.create'),
#test content
)

