from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
import requests, re, json, os
import time
from django.core.cache import cache
from django.http import JsonResponse
from .constants import ANIMAL_TRAITS # Importando o mapeamento acima
from .constants import ANIMAL_TRAITS, ERA_DETAILS, ERA_TAGS

# Configure sua chave da API aqui
# COLOQUE SUA API KEY DA TOGETHER AI AQUI
OPENROUTER_API_KEY = "chave"
DOTS_SLUG = "dots-studio/dots-3-note-preview:free"
# Chaves que a IA OBRIGATORIAMENTE deve retornar no JSON
XING_SLUG = "xingchen-agi/xing4.0-29b-a4b:free"
# OPENROUTER_API_KEY deve ser a string completa: "sk-or-v1-..."
MODELS = [DOTS_SLUG]
REQUIRED_KEYS = ["era_explanation", "final_look", "reasoning",
                 "animal_comment", "suggestions", "fit_score"]


def extract_json(text):
    """Pega do primeiro { ao último }, ignorando markdown e texto ao redor."""
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("sem JSON na resposta")
    return json.loads(text[start:end + 1])





def call_xing(system, user):
    models = MODELS
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "USP Fashion",
        "Content-Type": "application/json",
    }
    last_error = None
    for rodada in range(3):
        for model in models:
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                "reasoning": {"enabled": False},
                "max_tokens": 1500,
                "temperature": 0.8,
            }
        for attempt in range(5):
            try:
                r = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers, json=payload, timeout=60,
                )
                print(f"[xing] {model} tentativa {attempt + 1}: HTTP {r.status_code}")

                if r.status_code in (429, 502, 503, 504):
                    last_error = f"HTTP {r.status_code}: {r.text[:200]}"
                    time.sleep(8 * (attempt + 1))
                    continue
                if not r.ok:
                    last_error = f"HTTP {r.status_code}: {r.text[:300]}"
                    break  # erro que não adianta repetir (401, 404...)

                content = (r.json()["choices"][0]["message"].get("content") or "").strip()
                if not content:
                    raise ValueError("resposta vazia")
                data = extract_json(content)
                missing = [k for k in REQUIRED_KEYS if k not in data]
                if missing:
                    raise ValueError(f"faltam chaves: {missing}")
                if not isinstance(data["suggestions"], list):
                    data["suggestions"] = [str(data["suggestions"])]
                data["source"] = model
                return data

            except Exception as e:
                last_error = str(e)
                print(f"[xing] falhou: {last_error}")
                time.sleep(3)

    raise RuntimeError(last_error)


def backup_analysis(animal_id, year):
    animal, era = ANIMAL_TRAITS[animal_id], ERA_DETAILS[year]
    return {
        "era_explanation": era,
        "compatibility": f"{animal['perfil']} encara a era {year} do seu jeito.",
        "final_look": f"Look {animal['vibe']} reinterpretado para {year}.",
        "reasoning": "Combinação entre a vibe do personagem e a estética da época.",
        "animal_comment": "Hmm, até que eu gostei!",
        "suggestions": ["Acessório statement", "Paleta da era", "Calçado confortável"],
        "source": "local-backup",
    }


from pathlib import Path

LOOKS_FILE = Path(__file__).resolve().parent / "looks.json"

SYSTEM_PROMPT = ("Você é um stylist de moda irreverente e luxuoso. "
                 "Responda SOMENTE com um objeto JSON válido, sem markdown, em português do Brasil.")


def load_looks():
    try:
        return json.loads(LOOKS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_looks(looks):
    LOOKS_FILE.write_text(json.dumps(looks, ensure_ascii=False, indent=2), encoding="utf-8")


def build_prompt(animal_id, year):
    animal, era = ANIMAL_TRAITS[animal_id], ERA_DETAILS[year]
    return f"""PERSONAGEM: {animal_id} - {animal['perfil']}
Características: {animal['caracteristicas']}
Vibe: {animal['vibe']}
ERA: {year} - {era}

Crie uma fantasia de Halloween para esse personagem nesse estilo.
Se for um monstro ou tema de terror, deixe assustadora e divertida ao mesmo tempo.
Seja CURTO: cada campo de texto com no máximo 25 palavras.
Seja honesto: se a era combina pouco com a personalidade, dê nota baixa e o
personagem pode reclamar com humor. Se combina muito, ele pode amar.

JSON exigido:
{{
  "era_explanation": "a era em 1 frase curta",
  "final_look": "o look completo em 1-2 frases",
  "reasoning": "por que combina (ou não) com a personalidade, 1 frase",
  "animal_comment": "fala do personagem em 1ª pessoa, 1 frase",
  "suggestions": ["acessório 1 (máx 6 palavras)", "acessório 2", "acessório 3"],
  "fit_score": 0 a 100 (inteiro: quão bem esse look combina com a personalidade),
  "emojis": ["3 emojis que representam as peças do look"]
}}"""


def shorten(text, n=220):
    text = str(text or "").strip()
    if len(text) <= n:
        return text
    return text[:n].rsplit(" ", 1)[0] + "…"


def local_score(animal_id, year):
    ov = len(set(ANIMAL_TRAITS[animal_id]["tags"]) & set(ERA_TAGS[year]))
    return min(98, 35 + round(65 * ov / 3))


def enrich(analysis, animal_id, year):
    """Acrescenta notas e limpa o texto. Roda na hora de servir (cache ou novo)."""
    a = dict(analysis)
    local = local_score(animal_id, year)
    try:
        ai = max(0, min(100, int(float(a.get("fit_score")))))
    except (TypeError, ValueError):
        ai = None

    if ai is None:
        match, agreement = local, None
    else:
        match = round(0.6 * ai + 0.4 * local)
        agreement = 100 - abs(ai - local)

    a["match"] = match
    a["agreement"] = agreement
    a["verdict"] = "combina" if match >= 75 else "parcial" if match >= 50 else "contraste"

    for k in ("era_explanation", "final_look", "reasoning", "animal_comment"):
        a[k] = shorten(a.get(k), 220)
    sug = a.get("suggestions") or []
    a["suggestions"] = [shorten(s, 60) for s in sug][:3]
    emo = a.get("emojis") or []
    a["emojis"] = [e for e in emo if isinstance(e, str) and 0 < len(e) <= 8][:3]
    return a


def get_fashion_analysis(request):
    try:
        animal_id = request.GET.get("animal")
        year = request.GET.get("year")
        if not animal_id or not year:
            return JsonResponse({"error": "Animal ou ano não fornecido"}, status=400)
        if animal_id not in ANIMAL_TRAITS or year not in ERA_DETAILS:
            return JsonResponse({"error": "Animal ou era inválidos"}, status=404)

        key = f"{animal_id}:{year}"
        looks = load_looks()

        if key in looks and not request.GET.get("nocache"):
            return JsonResponse({"analysis": enrich(looks[key], animal_id, year)})

        try:
            analysis = call_xing(SYSTEM_PROMPT, build_prompt(animal_id, year))
            looks[key] = analysis
            save_looks(looks)
        except Exception as e:
            print(f"[DEBUG] IA falhou ({e}). Usando backup local.")
            analysis = backup_analysis(animal_id, year)

        return JsonResponse({"analysis": enrich(analysis, animal_id, year)})

    except Exception as e:
        print(f"[DEBUG] ERRO CRÍTICO: {e}")
        return JsonResponse({"error": str(e)}, status=500)


def warmup(request):
    """Gera todos os looks (personagens x eras) e salva em looks.json."""
    looks = load_looks()
    resultado = {}
    for animal_id in ANIMAL_TRAITS:
        for year in ERA_DETAILS:
            key = f"{animal_id}:{year}"
            if key in looks:
                resultado[key] = "já existia"
                continue
            try:
                print(f"[warmup] gerando {key}...")
                looks[key] = call_xing(SYSTEM_PROMPT, build_prompt(animal_id, year))
                save_looks(looks)
                resultado[key] = "OK"
            except Exception as e:
                resultado[key] = f"FALHOU: {str(e)[:150]}"
            time.sleep(3)  # respiro para não estourar o limite
    return JsonResponse(resultado, json_dumps_params={"ensure_ascii": False, "indent": 2})
def home(request):  
    return render(request, "index.html")

def studio(request):
    return render(request, "studio.html")