import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
"""Rend chacun des 14 tags dans un Django minimal, hors projet."""
import django
from django.conf import settings

settings.configure(
    DEBUG=True,
    INSTALLED_APPS=["django.contrib.contenttypes", "django.contrib.auth",
                    "django.contrib.staticfiles", "django.contrib.messages", "sdcd"],
    TEMPLATES=[{"BACKEND": "django.template.backends.django.DjangoTemplates",
                "APP_DIRS": True, "OPTIONS": {"context_processors": []}}],
    STATIC_URL="/static/",
    USE_I18N=True,
    DATABASES={},
)
django.setup()

from django.template import Context, Template
from django.core.paginator import Paginator

CAS = [
    ("sdcd_css", "{% sdcd_css %}", {}),
    ("sdcd_js", "{% sdcd_js nonce='abc' %}", {}),
    ("sdcd_favicon", "{% sdcd_favicon %}", {}),
    ("sdcd_theme_modale", "{% sdcd_theme_modale %}", {}),
    ("sdcd_accordion", "{% sdcd_accordion id='a1' title='Titre' content='<p>Corps</p>' %}", {}),
    ("sdcd_alert", "{% sdcd_alert title='Attention' type='warning' content='Texte' heading_tag='h3' %}", {}),
    ("sdcd_breadcrumb", "{% sdcd_breadcrumb fil %}",
     {"fil": {"links": [{"url": "/a", "title": "A"}], "current": "Page"}}),
    ("sdcd_notice", "{% sdcd_notice title='Info' description='Détail' link='/x' %}", {}),
    ("sdcd_quote", "{% sdcd_quote text='Citation' author='Auteur' source='Source' %}", {}),
    ("sdcd_skiplinks", "{% sdcd_skiplinks liens %}",
     {"liens": [{"link": "#contenu", "label": "Aller au contenu"}]}),
    ("sdcd_transcription", "{% sdcd_transcription title='T' content='<p>C</p>' %}", {}),
    ("sdcd_django_messages", "{% sdcd_django_messages %}", {"messages": []}),
    ("sdcd_pagination", "{% sdcd_pagination page %}",
     {"page": Paginator(list(range(100)), 10).page(5), "request": None}),
]

echecs = 0
for nom, source, ctx in CAS:
    try:
        html = Template("{% load sdcd_tags %}" + source).render(Context(ctx))
        classes = sorted({c for c in html.split('"') if c.strip().startswith("sdcd-")})
        marque = "fr-" in html
        etat = "ECHEC classes fr-* !" if marque else "ok"
        if marque:
            echecs += 1
        print(f"  {etat:5s}  {nom:22s}  {len(html):5d} car.  {classes[0][:44] if classes else '(aucune classe)'}")
    except Exception as e:
        echecs += 1
        print(f"  ECHEC  {nom:22s}  {type(e).__name__}: {e}")

# sdcd_form_field passe par la couche formulaires
from django import forms
from sdcd.forms import SdcdBaseForm

class Essai(SdcdBaseForm):
    courriel = forms.EmailField(label="Adresse électronique", help_text="Format : nom@exemple.cd")
    accepte = forms.BooleanField(label="J’accepte", required=False)
    choix = forms.ChoiceField(label="Choix", choices=[("a", "A"), ("b", "B")], widget=forms.RadioSelect)

try:
    f = Essai(data={})
    f.is_valid()
    html = Template("{% load sdcd_tags %}{% for c in form %}{% sdcd_form_field c %}{% endfor %}").render(Context({"form": f}))
    print(f"  {'ECHEC' if 'fr-' in html else 'ok':5s}  {'sdcd_form_field':22s}  {len(html):5d} car.")
    if "fr-" in html:
        echecs += 1
except Exception as e:
    echecs += 1
    print(f"  ECHEC  sdcd_form_field  {type(e).__name__}: {e}")

print(f"\n{'Tous les tags rendent sans classe fr-*.' if echecs == 0 else str(echecs) + ' echec(s).'}")
raise SystemExit(1 if echecs else 0)
