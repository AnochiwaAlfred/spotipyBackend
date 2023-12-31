
from ninja import NinjaAPI, Router
from ninja.security import django_auth
from django.http import HttpResponseForbidden
from users.models import CustomUser
from django.http import HttpResponseForbidden, response
from http import HTTPStatus
from decouple import config 

# from apis.v1.clientAuth import router as clientauth_router
# from apis.v1.lyrics import router as lyrics_router
from apis.v1.auth import router as auth_router
from apis.v1.albums import router as albums_router
from apis.v1.artists import router as artists_router
from apis.v1.client import router as clients_router
from apis.v1.genres import router as genres_router
from apis.v1.playlists import router as playlists_router
from apis.v1.tracks import router as tracks_router
from apis.v1.os import router as os_router

# from plugins.email_token import sendUserEmail
from django.utils import timezone
from ninja.security import HttpBearer


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        meta = request.META
        # HTTP_USER_AGENT = meta.get('HTTP_USER_AGENT')
        user =  CustomUser.objects.all().filter(token=token)
        if user.exists():
            foundUser = user.get()
        #     # on production check
        #     recipent_list =  f"{foundUser.email}" if config('ENVIRONMENT') == "production" else "anointedngeorge@gmail.com"
            
        #     sendUserEmail(
        #         recipient_list=recipent_list,
        #         subject=f'Login Notification <{foundUser.email}>',
        #         context={
        #                 'email': foundUser.email,
        #                 'message_date':timezone.now(),
        #                 "agent":str(HTTP_USER_AGENT),
        #             },
        #             template='login_template.html'
        #     )

            return foundUser.token
            # return True
    def on_auth_fail(self, response):
        return HttpResponseForbidden("Failed to authenticate! or maybe you requested for a password change.")
    

authenticator =  GlobalAuth() if config('ENVIRONMENT') == 'production' else None
api = NinjaAPI(
    auth=None,
    # auth=authenticator,
    title="Spotipy",
    description="This is an API with dynamic OpenAPI info section",
)

# let this be the first one.
api.add_router("/auth/", auth_router)
# -----------------------------------------
# api.add_router("/clientauth/", clientauth_router)
api.add_router("/albums/", albums_router)
api.add_router("/artists/", artists_router)
api.add_router("/clients/", clients_router)
api.add_router("/genres/", genres_router)
api.add_router("/playlists/", playlists_router)
api.add_router("/tracks/", tracks_router)
# api.add_router("/lyrics/", lyrics_router)




if config("ENVIRONMENT") == "development":
    api.add_router("/os/", os_router)
