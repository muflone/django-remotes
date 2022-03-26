##
#     Project: Django Remotes
# Description: A Django application to execute remote commands
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2021-2022 Fabio Castelli
#     License: GPL-3+
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
##

from django.urls import path

from api.views.v1.commands.get import CommandGetView
from api.views.v1.commands.list import CommandsListView
from api.views.v1.commands.post import CommandPostView
from api.views.v1.discover import DiscoverView
from api.views.v1.host.register import HostRegisterView
from api.views.v1.host.verify import HostVerifyView
from api.views.v1.host.status import HostStatusView


urlpatterns = [
    path(route='discover/',
         view=DiscoverView.as_view(),
         name='api.v1.discover'),
    path(route='commands/get/',
         view=CommandGetView.as_view(),
         name='api.v1.command.get.generic'),
    path(route='commands/get/'
               '<int:pk>/',
         view=CommandGetView.as_view(),
         name='api.v1.command.get'),
    path(route='commands/post/',
         view=CommandPostView.as_view(),
         name='api.v1.command.post.generic'),
    path(route='commands/post/'
               '<int:pk>/',
         view=CommandPostView.as_view(),
         name='api.v1.command.post'),
    path(route='commands/list/',
         view=CommandsListView.as_view(),
         name='api.v1.commands.list'),
    path(route='host/register/',
         view=HostRegisterView.as_view(),
         name='api.v1.host.register'),
    path(route='host/verify/',
         view=HostVerifyView.as_view(),
         name='api.v1.host.verify'),
    path(route='host/status/',
         view=HostStatusView.as_view(),
         name='api.v1.host.status'),
]
