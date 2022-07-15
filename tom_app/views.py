from django.shortcuts import render
from tom_app.fourier import busca_tom
from .forms import PostForm

# Create your views here.
def index(request):
    if request.method == "POST":
        form  = PostForm(request.POST)
        if form.is_valid():
            music = form.save(commit = False)
            url = str(form.cleaned_data["url"])
            tom_maior, tom_menor, vetor, nome, imagem, link = busca_tom(url)
            music.vetor = str(vetor)
            music.tom = tom_maior
            music.save()
            context = {'tom_maior': tom_maior, 'tom_menor': tom_menor, 'nome': nome, 'imagem':imagem, 'link':link, 'form': form}
            return render(request, "resposta.html", context)
    else:
        form  = PostForm()
    return render(request, "index.html", {"form":form})

def sobre(request):
    return render(request, "sobre.html")



# https://www.youtube.com/watch?v=OZI1hC5A_2M&ab_channel=IveteSangalo-Topic