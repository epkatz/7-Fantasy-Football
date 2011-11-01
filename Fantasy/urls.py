from Fantasy import settings
from Fantasy.football.authentication_views import *
from Fantasy.football.league_views import *
from Fantasy.football.myteam_views import *
from Fantasy.football.views import *
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'Fantasy.football.views.home', name='home'),
    # url(r'^Fantasy/', include('Fantasy.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    #Authentication
    url(r'^home', home),
    url(r'^login_page', login_page),
    url(r'^login', do_login),
    url(r'^logout', do_logout),
    url(r'^register', do_register),
    url(r'^change_password', change_password),
    url(r'^do_change_password', do_change_password),
    url(r'^myteam', myteam),
    url(r'^bench_player', bench_player),
    url(r'^start_player', start_player),
    url(r'^players', show_free_agents),
    url(r'^add_from_free_agent', add_from_free_agent),
    url(r'^drop_player', do_drop_player),
    url(r'^scoreboard', scoreboard),
    url(r'^add_week', add_week),
    url(r'^add_stats', add_stats),
    url(r'^trade_with', trade_with),    
    url(r'^trade', pick_counterpart),
    url(r'^make_trade', make_trade),
    url(r'^pending_trades', pending_trades),
    url(r'^accept_trade', accept_trade),
    
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
)
    
