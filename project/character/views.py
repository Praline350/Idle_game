from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden

from character.models import *
from character.forms import *

class CharacterDetailView(LoginRequiredMixin, View):
    template_name = 'character/character_detail.html'

    def get(self, request, *args, **kwargs):
        character = request.user.character
        trailer = request.user.character

        context = {
            'character': character,
            'trailer': trailer
        }

        return render(request, self.template_name, context=context)
    

class CharacterCreateView(View):
    template_name =  'character/character_create.html'

    def get(self, request, *args, **kwargs):
        # Instancie les formulaires vides
        character_form = CharacterForm()
        trailer_form = TrailerForm()

        context = {
            'character_form': character_form,
            'trailer_form': trailer_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # Instancie les formulaires avec les données POST
        character_form = CharacterForm(request.POST, request.FILES)
        trailer_form = TrailerForm(request.POST, request.FILES)

        if character_form.is_valid() and trailer_form.is_valid():
            # Sauvegarde le personnage mais ne le commite pas encore à la DB
            character = character_form.save(commit=False)
            character.user = request.user
            character.save()

            # Sauvegarde le trailer et le lie à l'utilisateur
            trailer = trailer_form.save(commit=False)
            trailer.user = request.user
            trailer.save()

            # Redirige vers la page de détails du personnage
            return redirect('character_detail')

        # Si les formulaires ne sont pas valides, renvoie les erreurs
        context = {
            'character_form': character_form,
            'trailer_form': trailer_form,
        }
        return render(request, self.template_name , context)
