from django.contrib import admin
from .models import Question, Choice


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fields = ["pub_date", "question_text"]  # Campos del modelo admin
    inlines = [ChoiceInline]    # Autoriza modificar el Choice, conectado al Question
    # ordering = ["-pub_date",]   # ordena de esa manera
    list_display = ("id", "question_text", "pub_date", "was_published_recently")    # Muestra en el display
    # list_display_link = ["question_text"]  # Que funcione como hipervinculo
    # list_filter = ["pub_date"]  # Activa los filtros con ese tipo de dato
    # list_editable = ["question_text"]   # Deja editar ese caracter hay mismo
    # search_fields = ["question_text", "id"] # Crea un buscador para buscar esos caracteres
    # list_per_page = 3     # Muestra esa cantidad por hoja
    

admin.site.register(Question, QuestionAdmin)
