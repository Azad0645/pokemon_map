from django.utils import timezone
import folium
from django.shortcuts import render, get_object_or_404
from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    now  = timezone.now()

    for entity in PokemonEntity.objects.select_related('pokemon').filter(
            appeared_at__lte=now,
            disappeared_at__gte=now
    ):
        image_url = (
            request.build_absolute_uri(entity.pokemon.image.url)
            if entity.pokemon.image else DEFAULT_IMAGE_URL
        )
        add_pokemon(folium_map, entity.lat, entity.lon, image_url)

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': (
                request.build_absolute_uri(pokemon.image.url)
                if pokemon.image else DEFAULT_IMAGE_URL
            ),
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for entity in pokemon.entities.all():
        image_url = (
            request.build_absolute_uri(pokemon.image.url)
            if pokemon.image else DEFAULT_IMAGE_URL
        )
        add_pokemon(folium_map, entity.lat, entity.lon, image_url)

    next_evolution = pokemon.next_evolutions.first()
    next_evolution_dict = None
    if next_evolution:
        next_evolution_dict = {
            'pokemon_id': next_evolution.id,
            'title_ru': next_evolution.title,
            'img_url': (
                request.build_absolute_uri(next_evolution.image.url)
                if next_evolution.image else DEFAULT_IMAGE_URL
            )
        }

    previous_evolution = pokemon.evolved_from
    previous_evolution_dict = None
    if previous_evolution:
        previous_evolution_dict = {
            'pokemon_id': previous_evolution.id,
            'title_ru': previous_evolution.title,
            'img_url': (
                request.build_absolute_uri(previous_evolution.image.url)
                if previous_evolution.image else DEFAULT_IMAGE_URL
            )
        }

    pokemon_dict = {
        'pokemon_id': pokemon.id,
        'title_ru': pokemon.title,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'img_url': (
            request.build_absolute_uri(pokemon.image.url)
            if pokemon.image else DEFAULT_IMAGE_URL
        ),
        'description': pokemon.description,
        'next_evolution': next_evolution_dict,
        'previous_evolution': previous_evolution_dict,
    }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemon_dict,
    })
