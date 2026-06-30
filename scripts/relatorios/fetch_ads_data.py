"""
Script: fetch_ads_data.py
Extrai dados dos últimos 90 dias da conta Google Ads da Bellosom e gera relatório em JSON.
"""

import os
import json
from datetime import datetime, timedelta
from dotenv import dotenv_values

# Carrega credenciais do .env.local
env_path = os.path.join(os.path.dirname(__file__), "../../.env.local")
config = dotenv_values(env_path)

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Monta configuração do cliente
credentials = {
    "developer_token": config["GOOGLE_ADS_DEVELOPER_TOKEN"],
    "client_id": config["GOOGLE_ADS_CLIENT_ID"],
    "client_secret": config["GOOGLE_ADS_CLIENT_SECRET"],
    "refresh_token": config["GOOGLE_ADS_REFRESH_TOKEN"],
    "use_proto_plus": True,
}

client = GoogleAdsClient.load_from_dict(credentials)
customer_id = config["GOOGLE_ADS_CUSTOMER_ID"].replace("-", "")

# Período: últimos 90 dias
end_date = datetime.today()
start_date = end_date - timedelta(days=90)
date_range = f"'{start_date.strftime('%Y-%m-%d')}' AND '{end_date.strftime('%Y-%m-%d')}'"

ga_service = client.get_service("GoogleAdsService")

# -------------------------------------------------------
# 1. Campanhas
# -------------------------------------------------------
campaign_query = f"""
    SELECT
        campaign.id,
        campaign.name,
        campaign.status,
        campaign.advertising_channel_type,
        metrics.impressions,
        metrics.clicks,
        metrics.cost_micros,
        metrics.conversions,
        metrics.ctr,
        metrics.average_cpc
    FROM campaign
    WHERE segments.date BETWEEN {date_range}
      AND campaign.status != 'REMOVED'
    ORDER BY metrics.cost_micros DESC
"""

campaign_response = ga_service.search(customer_id=customer_id, query=campaign_query)

campaigns = []
for row in campaign_response:
    campaigns.append({
        "id": row.campaign.id,
        "name": row.campaign.name,
        "status": row.campaign.status.name,
        "tipo": row.campaign.advertising_channel_type.name,
        "impressoes": row.metrics.impressions,
        "cliques": row.metrics.clicks,
        "custo_brl": round(row.metrics.cost_micros / 1_000_000, 2),
        "conversoes": round(row.metrics.conversions, 2),
        "ctr_pct": round(row.metrics.ctr * 100, 2),
        "cpc_medio_brl": round(row.metrics.average_cpc / 1_000_000, 2),
    })

# -------------------------------------------------------
# 2. Grupos de anúncios
# -------------------------------------------------------
adgroup_query = f"""
    SELECT
        ad_group.id,
        ad_group.name,
        ad_group.status,
        campaign.name,
        metrics.impressions,
        metrics.clicks,
        metrics.cost_micros,
        metrics.conversions,
        metrics.ctr,
        metrics.average_cpc
    FROM ad_group
    WHERE segments.date BETWEEN {date_range}
      AND ad_group.status != 'REMOVED'
    ORDER BY metrics.cost_micros DESC
"""

adgroup_response = ga_service.search(customer_id=customer_id, query=adgroup_query)

adgroups = []
for row in adgroup_response:
    adgroups.append({
        "id": row.ad_group.id,
        "nome": row.ad_group.name,
        "status": row.ad_group.status.name,
        "campanha": row.campaign.name,
        "impressoes": row.metrics.impressions,
        "cliques": row.metrics.clicks,
        "custo_brl": round(row.metrics.cost_micros / 1_000_000, 2),
        "conversoes": round(row.metrics.conversions, 2),
        "ctr_pct": round(row.metrics.ctr * 100, 2),
        "cpc_medio_brl": round(row.metrics.average_cpc / 1_000_000, 2),
    })

# -------------------------------------------------------
# 3. Palavras-chave
# -------------------------------------------------------
keyword_query = f"""
    SELECT
        ad_group_criterion.keyword.text,
        ad_group_criterion.keyword.match_type,
        ad_group_criterion.status,
        ad_group.name,
        campaign.name,
        metrics.impressions,
        metrics.clicks,
        metrics.cost_micros,
        metrics.conversions,
        metrics.ctr,
        metrics.average_cpc,
        metrics.search_impression_share
    FROM keyword_view
    WHERE segments.date BETWEEN {date_range}
      AND ad_group_criterion.status != 'REMOVED'
    ORDER BY metrics.cost_micros DESC
"""

keyword_response = ga_service.search(customer_id=customer_id, query=keyword_query)

keywords = []
for row in keyword_response:
    keywords.append({
        "keyword": row.ad_group_criterion.keyword.text,
        "match_type": row.ad_group_criterion.keyword.match_type.name,
        "status": row.ad_group_criterion.status.name,
        "grupo": row.ad_group.name,
        "campanha": row.campaign.name,
        "impressoes": row.metrics.impressions,
        "cliques": row.metrics.clicks,
        "custo_brl": round(row.metrics.cost_micros / 1_000_000, 2),
        "conversoes": round(row.metrics.conversions, 2),
        "ctr_pct": round(row.metrics.ctr * 100, 2),
        "cpc_medio_brl": round(row.metrics.average_cpc / 1_000_000, 2),
        "impression_share_pct": round((row.metrics.search_impression_share or 0) * 100, 1),
    })

# -------------------------------------------------------
# 4. Termos de pesquisa (search terms reais)
# -------------------------------------------------------
search_terms_query = f"""
    SELECT
        search_term_view.search_term,
        search_term_view.status,
        campaign.name,
        ad_group.name,
        metrics.impressions,
        metrics.clicks,
        metrics.cost_micros,
        metrics.conversions,
        metrics.ctr
    FROM search_term_view
    WHERE segments.date BETWEEN {date_range}
    ORDER BY metrics.conversions DESC, metrics.clicks DESC
"""

st_response = ga_service.search(customer_id=customer_id, query=search_terms_query)

search_terms = []
for row in st_response:
    search_terms.append({
        "termo": row.search_term_view.search_term,
        "status": row.search_term_view.status.name,
        "campanha": row.campaign.name,
        "grupo": row.ad_group.name,
        "impressoes": row.metrics.impressions,
        "cliques": row.metrics.clicks,
        "custo_brl": round(row.metrics.cost_micros / 1_000_000, 2),
        "conversoes": round(row.metrics.conversions, 2),
        "ctr_pct": round(row.metrics.ctr * 100, 2),
    })

# -------------------------------------------------------
# 5. Anúncios
# -------------------------------------------------------
ads_query = f"""
    SELECT
        ad_group_ad.ad.id,
        ad_group_ad.ad.final_urls,
        ad_group_ad.status,
        ad_group_ad.ad.responsive_search_ad.headlines,
        ad_group_ad.ad.responsive_search_ad.descriptions,
        ad_group.name,
        campaign.name,
        metrics.impressions,
        metrics.clicks,
        metrics.cost_micros,
        metrics.conversions,
        metrics.ctr
    FROM ad_group_ad
    WHERE segments.date BETWEEN {date_range}
      AND ad_group_ad.status != 'REMOVED'
    ORDER BY metrics.conversions DESC, metrics.clicks DESC
"""

ads_response = ga_service.search(customer_id=customer_id, query=ads_query)

ads = []
for row in ads_response:
    ad = row.ad_group_ad.ad
    headlines = []
    descriptions = []
    if hasattr(ad, "responsive_search_ad") and ad.responsive_search_ad:
        headlines = [h.text for h in ad.responsive_search_ad.headlines]
        descriptions = [d.text for d in ad.responsive_search_ad.descriptions]
    ads.append({
        "id": ad.id,
        "status": row.ad_group_ad.status.name,
        "grupo": row.ad_group.name,
        "campanha": row.campaign.name,
        "titulos": headlines,
        "descricoes": descriptions,
        "url_final": list(ad.final_urls)[:1],
        "impressoes": row.metrics.impressions,
        "cliques": row.metrics.clicks,
        "custo_brl": round(row.metrics.cost_micros / 1_000_000, 2),
        "conversoes": round(row.metrics.conversions, 2),
        "ctr_pct": round(row.metrics.ctr * 100, 2),
    })

# -------------------------------------------------------
# Salva resultado JSON
# -------------------------------------------------------
output = {
    "periodo": {
        "inicio": start_date.strftime("%Y-%m-%d"),
        "fim": end_date.strftime("%Y-%m-%d"),
    },
    "campanhas": campaigns,
    "grupos_de_anuncio": adgroups,
    "palavras_chave": keywords,
    "termos_de_pesquisa": search_terms,
    "anuncios": ads,
}

output_path = os.path.join(os.path.dirname(__file__), "../../relatorios/dados_brutos.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Dados salvos em: {os.path.abspath(output_path)}")
print(f"Campanhas: {len(campaigns)} | Grupos: {len(adgroups)} | Keywords: {len(keywords)} | Search Terms: {len(search_terms)} | Anúncios: {len(ads)}")
