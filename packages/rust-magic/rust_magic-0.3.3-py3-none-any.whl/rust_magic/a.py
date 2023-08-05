def primeira_pergunta(request):
    trans = Tranfer()
    my_list = trans.shared[0]
    respostaum = ['amarelo', 'vermelho', 'roxo', 'cinza']
    if request.method == 'POST':
        selecionada = request.POST['respostaum']
    #if selecionada != 'Escolha uma':
        f = Cheiro.objects.get(pk=my_list)
        u = f.pk
        f.resposta1 = selecionada
        f.save()
    else:
        selecionada = 'Escolha uma'

    context = {'respostaum': respostaum}

    return render(request, 'cheiro/primeira_pergunta.html', context)
