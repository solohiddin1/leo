from django.contrib.admin.apps import AdminConfig
from django.contrib import admin

class CustomAdminSite(admin.AdminSite):
    def get_app_list(self, request, app_label=None):
        app_dict = self._build_app_dict(request, app_label)

        app_ordering = {
            "user": 1,
            "order": 2,
            "product": 3,
            "transaction": 4,
            "notification": 5,
        }

        app_list = sorted(
            app_dict.values(),
            key=lambda x: app_ordering.get(x['app_label'], float('inf'))
        )

        # reordering models inside apps
        # for app in app_list:
        #     if app['app_label'] == 'my_main_app':
        #         model_ordering = {
        #             "UserProfile": 1,
        #             "Order": 2,
        #             "Product": 3,
        #         }
        #         app['models'].sort(
        #             key=lambda x: model_ordering.get(x['object_name'], float('inf'))
        #         )

        return app_list

class MyAdminConfig(AdminConfig):
    default_site = 'root.admin_site.CustomAdminSite'