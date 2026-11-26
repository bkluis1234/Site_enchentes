//Endereço do servidor back-end LOCAL, Lembrar de trocar antes de fazer o deploy.
const API_URL = "http://127.0.0.1:8000"

//Busca as ocrreências na API e projeta na tela caso esteja vazia mostra na tela
async function carregarOcorrencias(){
    try{
        const resposta = await fetch(`${API_URL}/ocorrencias`);
        if (!resposta.ok) {
            const erroApi = await resposta.json().catch(() => ({}));
            throw new Error(`Servidor respondeu com status ${resposta.status}: ${erroApi.detail || ""}`);
        }
        const dados = await resposta.json();

        const container = document.getElementById("listaOcorrencias");
        container.innerHTML = "";

        if (dados.length === 0) {
            container.innerHTML = "<p>Nenhuma Ocorrências registrada ainda.</p>";
            return;
        }

         /*
        *Projeta cada OCORRÊNCIA na tela.
        *E Cria um div com classe "ocorrencia-card", preenchendo com os dados da API e colocando no container.           
        */
        dados.forEach(oc => {
           const card = document.createElement("div");
           card.className = "ocorrencia-card";

           // textContent evita que texto digitado pelo usuário seja executado como HTML (XSS)
           const titulo = document.createElement("strong");
           titulo.textContent = oc.tipo;

           const local = document.createTextNode(` - ${oc.bairro}`);

           const descricao = document.createElement("p");
           descricao.textContent = oc.descricao;

           const info = document.createElement("small");
           info.textContent = `Lat: ${oc.latitude} | Lon: ${oc.longitude} | Status: ${oc.status}`;

           card.append(titulo, local, document.createElement("br"), descricao, info);
           container.appendChild(card);
        });

    /*
    *Tratamento com o ERRO:
    *Caso a conexão com a API tenha alguma falha, iri ser exibido no console o ERRO com os detalhes tecnicos
    #e sera exibo ao USUARIO uma mensagem de alerta(erro) em vermelho.
    */
    } catch (erro) {
        console.error("Erro a o buscar as Ocorrências:", erro);
        document.getElementById("listaOcorrencias").innerHTML = "<p style='color:red;'>Erro ao tentar conectar com a API.</p>";
    }
}

// Captura o envio do formulário, envia a nova ocorrência (POST) para a API e atualiza a lista
document.getElementById("formOcorrencia").addEventListener("submit", async (e) => {
    e.preventDefault();
    const novaOcorrencia = {
        tipo: document.getElementById("tipo").value,
        descricao: document.getElementById("descricao").value,
        bairro: document.getElementById("bairro").value,
        latitude: parseFloat (document.getElementById("latitude").value),
        longitude: parseFloat (document.getElementById("longitude").value)
    };

    try{
        const resposta = await fetch(`${API_URL}/ocorrencias`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(novaOcorrencia)
        });

        if (resposta.ok) {
            alert("Ocorrência registrada com sucesso!");
            document.getElementById("formOcorrencia").reset()
            carregarOcorrencias(); //Atualiza as OCORRÊCIAS automaticamente na tela.
        } else{
            if (resposta.status === 422) {
                alert("Coordenadas inválidas. Confira a latitude e a longitude.");
            } else {
                alert ("ERRO ao regritrar sua OCORRÊNCIA.");
            }
        }

    } catch (erro){
        console.error("ERRO na requisição", erro);
        alert("Não foi possível conectar com o servidor.");
    }
});

//Assim que o site é aberto a lista é exibida
carregarOcorrencias();