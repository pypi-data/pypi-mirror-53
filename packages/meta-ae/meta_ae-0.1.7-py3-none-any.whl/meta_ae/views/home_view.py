from edc_adverse_event.views import HomeView as BaseHomeView


class HomeView(BaseHomeView):

    navbar_name = "meta_dashboard"
    navbar_selected_item = "ae_home"
