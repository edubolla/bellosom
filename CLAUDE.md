# CLAUDE.md — Bellosom Aparelhos Auditivos

## Sobre o Projeto

**Nome do cliente:** Bellosom Aparelhos Auditivos  
**Segmento:** Clínica especializada em saúde auditiva — fonoaudiólogos e venda de aparelhos auditivos  
**Localização:** Av. Assis Brasil, 3768 - Jardim Lindóia, Porto Alegre - RS — CEP 91010-003

**Contexto de negócio:**  
A Bellosom é uma clínica consolidada. Os serviços de audiometria e exames já são bem reconhecidos no mercado. O foco atual do projeto é aumentar a venda de aparelhos auditivos, que caiu nos últimos tempos. A principal estratégia de aquisição é o Google Ads.

**Principal conversão:** Clique para o WhatsApp  
**Orçamento mensal Google Ads:** ~R$ 1.000,00

---

## Canais e Presença Digital

| Canal | URL |
|---|---|
| Site institucional | https://www.bellosom.com.br/ |
| Landing Page Google Ads | https://www.bellosom.com.br/aparelho-auditivo-bellosom |
| Instagram | https://www.instagram.com/bellosomaparelhosauditivos/ |
| Facebook | https://www.facebook.com/bellosomaparelhosauditivos |
| Google Meu Negócio | https://share.google/oOVLejd5HvpSYlREd |

---

## Sobre o Gestor (eu)

Sou Gestor de Tráfego e Performance responsável pelo Google Ads da Bellosom. Minhas responsabilidades incluem:

- Gerenciar as campanhas ativas no Google Ads
- Sugerir novas campanhas e segmentações
- Executar rotina de otimização de conta (lances, qualidade, palavras-chave, negativações etc.)
- Propor copies e criativos para anúncios com objetivo de aumentar conversões
- Analisar performance e gerar insights acionáveis

Se tiver dúvida sobre alguma decisão, proposta ou contexto do projeto — **pergunte antes de agir.**

---

## Tecnologias Utilizadas

- **Google Ads API** — para automações, relatórios e integrações programáticas
- **Variáveis de ambiente:** todas as credenciais sensíveis estão no arquivo `.env.local`

> ⚠️ **NUNCA exponha, compartilhe ou exiba as credenciais do `.env.local`.** Isso inclui tokens, client IDs, client secrets e quaisquer chaves de API.

---

## Estrutura de Pastas Sugerida

```
bellosom-ads/
├── .env.local               # Credenciais (nunca expor)
├── CLAUDE.md                # Este arquivo
├── ads/
│   ├── copies/              # Textos de anúncios (títulos, descrições)
│   ├── criativos/           # Briefings e referências para criativos visuais
│   └── campanhas/           # Configurações e estruturas de campanhas
├── scripts/
│   ├── relatorios/          # Scripts para extração de dados via API
│   └── otimizacao/          # Scripts de automação e ajustes de conta
├── relatorios/              # Outputs gerados (CSVs, JSONs, resumos)
└── docs/                    # Documentações e anotações do projeto
```

---

## Principais Entregáveis

O Claude Code atua principalmente em:

1. **Sugestão de copies e criativos** — títulos e descrições para anúncios de pesquisa, display e Performance Max, com foco em conversão (clique para WhatsApp)
2. **Análise e otimização** — leitura de dados da conta e sugestão de melhorias embasadas
3. **Automações via Google Ads API** — scripts para tarefas repetitivas ou relatórios

---

## Regras do Projeto

- **Sempre responda em PT-BR** — todos os textos, comentários de código e entregas devem estar em português do Brasil
- **Entregue código que funciona** — sem esqueletos, sem TODOs soltos; se não tiver informação suficiente, pergunte antes
- **Nunca quebre o que já está funcionando** — ao adicionar algo novo, preserve o que já opera em produção
- **Pergunte antes de assumir** — se houver dúvida sobre contexto, estratégia ou intenção, questione antes de criar
- **Credenciais são intocáveis** — jamais exponha o conteúdo do `.env.local` em qualquer output

---

## Contexto Estratégico para Copies

Ao sugerir textos de anúncios, considere sempre:

- **Público-alvo:** pessoas com perda auditiva (ou familiares/cuidadores), em Porto Alegre e região
- **Diferenciais da Bellosom:** fonoaudiólogos especialistas, clínica estabelecida, localização central (Av. Assis Brasil)
- **Gatilhos relevantes:** qualidade de vida, discrição dos aparelhos modernos, facilidade de acesso, confiança clínica
- **CTA principal:** "Fale no WhatsApp", "Chame no WhatsApp", "Agende pelo WhatsApp"
- **Tom de voz:** acolhedor, profissional, direto — sem exageros ou promessas não comprovadas
- **Página de destino dos anúncios:** https://www.bellosom.com.br/aparelho-auditivo-bellosom
