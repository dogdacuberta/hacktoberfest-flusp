async function requestOutfit() {
    const animal = document.getElementById('selected-animal').value;
    const year = document.getElementById('selected-year').value;

    const response = await fetch(`/get-fashion-advice/?animal=${animal}&year=${year}`);
    const data = await response.json();

    // O Modelo fala
    document.getElementById('model-speech').innerText = `Para ${year}, a tendência é ${data.trend_name}. Você deve usar: ${data.suggestion}!`;
    
    // O Animal reage após 2 segundos
    setTimeout(() => {
        document.getElementById('animal-speech').innerText = data.reaction;
        document.getElementById('animal-sprite').classList.add('bounce-animation');
    }, 2000);
}