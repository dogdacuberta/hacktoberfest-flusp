ANIMAL_TRAITS = {
    "quati": {
        "perfil": "O Sobrevivente Urbano",
        "caracteristicas": "Curioso, oportunista, ágil, lida bem com a terra e sucata.",
        "vibe": "Streetwear, utilitarismo, explorador.",
        "tags": ["urbano", "explorador", "utilitario", "rebelde", "ironia", "sustentavel"],
    },
    "galinha": {
        "perfil": "A Operária do Café",
        "caracteristicas": "Matinal, ansiosa, social, segue rotinas rígidas.",
        "vibe": "Preppy, casual, workcore, confortável.",
        "tags": ["conforto", "rotina", "social", "nostalgia", "minimalista", "retro"],
    },
    "flusp": {
        "perfil": "O Hacker do Software Livre",
        "caracteristicas": "Colaborativo, curioso, noturno, defensor do código aberto, vive de café e commits.",
        "vibe": "Geek-chic, moletom com adesivos, techwear, orgulho nerd.",
        "tags": ["tech", "noturno", "ironia", "nostalgia", "neon", "sustentavel", "rebelde", "conforto"],
    },
}

ERA_DETAILS = {
    "1970": "Disco / Boho: calças boca de sino, paetês, franjas, tons terrosos e brilho de pista de dança.",
    "1980": "Neon Pop: ombreiras, cores fluorescentes, legging, jaquetas coloridas, volume e ousadia.",
    "1990": "Grunge / Minimalismo: flanela, jeans rasgado, coturno, camisetas de banda, slip dress.",
    "2000": "Y2K: metalizado, cintura baixa, óculos minúsculos, tecnologia retrô, brilho e glitter.",
    "2016": "Era Hipster / Pokémon GO: ironia, nostalgia digital, camisas xadrez, óculos redondos.",
    "2020": "Era E-Girl / Gamer: neon, TikTok, correntes, headsets, cultura de internet.",
    "2024": "Quiet Luxury / Coquette: minimalismo, cores neutras, laços, pérolas, elegância discreta.",
    "2026": "Cyber-Organic: futurismo sustentável, tecidos vivos, sensores de luz, bioplásticos.",
    "vampiro": "Vampiro Gótico: capa com gola alta, vermelho sangue, preto, presas e elegância sombria.",
    "bruxa": "Bruxa: chapéu pontudo, túnica roxa, poções verdes, estrelas e magia noturna.",
    "mumia": "Múmia: bandagens envelhecidas, tons de areia, mistério do Egito antigo.",
    "zumbi": "Zumbi: roupas rasgadas, pele esverdeada, manchas de sangue, apocalipse urbano.",
    "fantasma": "Fantasma: lençol esvoaçante, véu translúcido, correntes e assombração clássica.",
    "frankenstein": "Frankenstein: parafusos no pescoço, testa quadrada, cicatriz costurada, jaqueta preta.",
    "palhaco": "Palhaço Macabro: peruca colorida, sorriso exagerado, gola de babados e circo sinistro.",
    "lobisomem": "Lobisomem: orelhas peludas, garras, presas, pelos e camisa rasgada sob a lua cheia.",
}

# Tags usadas no cálculo local de afinidade (personagem x era)
ERA_TAGS = {
    "1970": ["retro", "social", "nostalgia", "maximalista", "artistico", "luxo"],
    "1980": ["neon", "rebelde", "social", "retro", "maximalista", "artistico"],
    "1990": ["rebelde", "utilitario", "urbano", "conforto", "minimalista", "ironia"],
    "2000": ["tech", "neon", "nostalgia", "ironia", "social", "maximalista"],
    "2016": ["ironia", "nostalgia", "urbano", "retro", "conforto"],
    "2020": ["tech", "neon", "noturno", "rebelde", "ironia"],
    "2024": ["minimalista", "luxo", "conforto", "rotina"],
    "2026": ["tech", "sustentavel", "minimalista", "explorador"],
    "vampiro": ["noturno", "luxo", "retro", "rebelde"],
    "bruxa": ["noturno", "explorador", "sustentavel", "ironia", "rotina"],
    "mumia": ["retro", "minimalista", "explorador", "nostalgia"],
    "zumbi": ["urbano", "rotina", "utilitario", "ironia", "noturno"],
    "fantasma": ["noturno", "minimalista", "nostalgia", "conforto"],
    "frankenstein": ["tech", "rebelde", "utilitario", "ironia", "noturno"],
    "palhaco": ["ironia", "social", "neon", "rebelde", "urbano"],
    "lobisomem": ["noturno", "explorador", "urbano", "rebelde", "utilitario"],
}