let fullResponse = ''
let typingInterval
let isTyping = false
let synth = window.speechSynthesis

// Função para enviar a pergunta e exibir a resposta
async function sendQuestion() {
  const question = document.getElementById('question').value
  document.getElementById('response').innerHTML = '<span>Carregando...</span>'
  document.getElementById('stopBtn').disabled = true

  try {
    const response = await fetch(
      `/chat/perguntar/?pergunta=${encodeURIComponent(question)}`
    )
    if (!response.ok) {
      throw new Error('Erro na resposta do servidor')
    }
    const data = await response.json()
    fullResponse = data.resposta || 'Desculpe, não consegui responder.'
    typeResponseWithEffect(fullResponse, data.imagens)
  } catch (error) {
    document.getElementById('response').innerText =
      'Erro ao enviar a pergunta: ' + error.message
  }
}

// Efeito de digitação gradual
function typeResponseWithEffect(response, images) {
  const responseDiv = document.getElementById('response')
  responseDiv.innerHTML = ''
  let index = 0
  isTyping = true

  typingInterval = setInterval(() => {
    if (index < response.length) {
      const char = response.charAt(index)
      responseDiv.innerHTML += char === '\n' ? '<br>' : char
      index++
    } else {
      finalizeTyping(response, images)
    }
  }, 3)

  document.getElementById('stopBtn').disabled = false
}

// Finaliza o efeito de digitação
function finalizeTyping(response, images) {
  clearInterval(typingInterval)
  isTyping = false
  document.getElementById('stopBtn').disabled = true
  applyFullFormatting(response, images)
}

// Exibe a resposta formatada e a galeria de imagens
function applyFullFormatting(response, images) {
  const responseDiv = document.getElementById('response')
  responseDiv.innerHTML = response

  if (images && images.length > 0) {
    const gallery = document.createElement('div')
    gallery.className = 'image-gallery'

    images.forEach((image, index) => {
      const linkElement = document.createElement('a')
      linkElement.href = '#'

      const imgElement = document.createElement('img')
      imgElement.src = image
      imgElement.alt = 'Imagem ' + (index + 1)

      linkElement.appendChild(imgElement)
      gallery.appendChild(linkElement)
    })

    responseDiv.appendChild(gallery)
  }
}

// Interrompe a digitação
function stopTyping() {
  if (isTyping) {
    clearInterval(typingInterval)
    document.getElementById('response').innerHTML = fullResponse
    isTyping = false
  }
}

// Lê a resposta com controle de velocidade
function readResponse() {
  if (synth.speaking) {
    synth.cancel() // Cancela a fala se já estiver em andamento
  } else {
    const utterance = new SpeechSynthesisUtterance(fullResponse) // Cria o objeto de fala
    const rateControl = document.getElementById('rateControl') // Pega o valor da velocidade

    utterance.rate = parseFloat(rateControl.value) // Define a velocidade da leitura
    synth.speak(utterance) // Inicia a leitura em voz alta
  }
}
