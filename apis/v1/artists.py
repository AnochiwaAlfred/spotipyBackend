from ninja import Router, UploadedFile, Form, File
from typing import List, Union
from schemas.tracks import *
from schemas.album import *
from users.models import *
from schemas.artist import *
from decouple import config

router = Router(tags=["Artists Router"])
BASE_URL = config('BACKEND_BASE_URL') if config('ENVIRONMENT')=='production' else config('DEVELOPMENT_BACKEND_BASE__URL')


@router.get('/getAllArtists', response=Union[List[ArtistRetrievalSchema], str])
def getAllArtists(request):
    artists = Artist.objects.all()
    artistsMod = [
        ArtistRetrievalSchema(
            id=artist.id,
            email=artist.email,
            username=artist.username,
            firstName=artist.firstName,
            lastName=artist.lastName,
            stageName=artist.stageName,
            phone=artist.phone,
            bio=artist.bio,
            dateOfBirth=artist.dateOfBirth,
            coverImage=f"{BASE_URL}{artist.coverImage.url}" if artist.coverImage else None,
            image=f"{BASE_URL}{artist.image.url}" if artist.image else None,
        )
        for artist in artists
    ]
    return artistsMod

@router.get('/getArtistById/{id}', response=Union[ArtistRetrievalSchema, str])
def getArtistById(request, id):
    instance = Artist.objects.filter(id=id)
    if instance.exists():
        artist=instance[0]
        return ArtistRetrievalSchema(
            id=artist.id,
            email=artist.email,
            username=artist.username,
            firstName=artist.firstName,
            lastName=artist.lastName,
            stageName=artist.stageName,
            phone=artist.phone,
            bio=artist.bio,
            dateOfBirth=artist.dateOfBirth,
            coverImage=f"{BASE_URL}{artist.coverImage.url}" if artist.coverImage else None,
            image=f"{BASE_URL}{artist.image.url}" if artist.image else None,
        )
    else:
        return f"Artist with ID {id} does not exists"


@router.get('/searchArtists/{query}', response=List[ArtistRetrievalSchema])
def searchArtists(request, query):
    artists = Artist.objects.filter(stageName__icontains=query)
    return artists

@router.post('/updateArtist/{id}', response=Union[ArtistRetrievalSchema, str])
def updateArtist(request, id, data:ArtistUpdateSchema=Form(...)):
    instance = Artist.objects.filter(id=id)
    if instance.exists():
        # artist = instance[0]
        data_p = data.dict()
        filterdata = {attr:value for attr,value in data_p.items() if (value != None) and (value != '')}
        if len(filterdata) > 0:
            artist = instance.filter(id=id).update(**filterdata)
            return instance[0]
        else:
            return "Data Empty"
    else:
        return f"Error: Artist with ID {id} does not exist"
    
     
@router.post('/updateArtistImages/{id}', response=Union[ArtistRetrievalSchema, str])
def updateArtistImages(request, id, image:UploadedFile=File(...), coverImage:UploadedFile=File(...)):
    instance = Artist.objects.filter(id=id)
    if instance.exists():
        artist = instance[0]
        artist.image = image
        artist.coverImage = coverImage
        artist.save()
        return artist

            
 
# gAAAAABlHz1qPA4i1y7sb-IP2D1H6CpZHmarg5CAqOYUhmtAlanYwY_PKdzfV3o1qgM5r_GBwU7TYRWTWQCCUoW-v_5vpSHE7w==