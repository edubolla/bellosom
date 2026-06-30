"""
Script: fetch_adrank_assets.py
Extrai Quality Score, AdRank, performance de assets e extensões das campanhas ativas.
"""

import os
import json
from dotenv import dotenv_values
from google.ads.googleads.client import GoogleAdsClient

env_path = os.path.join(os.path.dirname(__file__), "../../.env.local")
config = dotenv_values(env_path)

credentials = {
    "developer_token": config["GOOGLE_ADS_DEVELOPER_TOKEN"],
    "client_id": config["GOOGLE_ADS_CLIENT_ID"],
    "client_secret": config["GOOGLE_ADS_CLIENT_SECRET"],
    "refresh_token": config["GOOGLE_ADS_REFRESH_TOKEN"],
    "use_proto_plus": True,
}

client = GoogleAdsClient.load_from_dict(credentials)
customer_id = config["GOOGLE_ADS_CUSTOMER_ID"].replace("-", "")
ga = client.get_service("GoogleAdsService")

# IDs das campanhas ativas (extraídos do relatório anterior)
ACTIVE_CAMPAIGN_FILTER = "campaign.status = 'ENABLED'"

# -------------------------------------------------------
# 1. Quality Score por keyword (campanhas ativas)
# -------------------------------------------------------
qs_query = f"""
    SELECT
        campaign.name,
        ad_group.name,
        ad_group_criterion.keyword.text,
        ad_group_criterion.keyword.match_type,
        ad_group_criterion.quality_info.quality_score,
        ad_group_criterion.quality_info.creative_quality_score,
        ad_group_criterion.quality_info.post_click_quality_score,
        ad_group_criterion.quality_info.search_predicted_ctr,
        metrics.impressions,
        metrics.clicks,
        metrics.cost_micros,
        metrics.conversions,
        metrics.average_cpc
    FROM keyword_view
    WHERE {ACTIVE_CAMPAIGN_FILTER}
      AND ad_group_criterion.status != 'REMOVED'
      AND metrics.impressions > 0
    ORDER BY metrics.cost_micros DESC
"""

qs_resp = ga.search(customer_id=customer_id, query=qs_query)
keywords_qs = []
for row in qs_resp:
    qi = row.ad_group_criterion.quality_info
    keywords_qs.append({
        "campanha": row.campaign.name,
        "grupo": row.ad_group.name,
        "keyword": row.ad_group_criterion.keyword.text,
        "match_type": row.ad_group_criterion.keyword.match_type.name,
        "quality_score": qi.quality_score,
        "creative_quality": qi.creative_quality_score.name if qi.creative_quality_score else "UNKNOWN",
        "landing_page_quality": qi.post_click_quality_score.name if qi.post_click_quality_score else "UNKNOWN",
        "expected_ctr": qi.search_predicted_ctr.name if qi.search_predicted_ctr else "UNKNOWN",
        "impressoes": row.metrics.impressions,
        "cliques": row.metrics.clicks,
        "custo_brl": round(row.metrics.cost_micros / 1_000_000, 2),
        "conversoes": round(row.metrics.conversions, 2),
        "cpc_medio_brl": round(row.metrics.average_cpc / 1_000_000, 2),
    })

# -------------------------------------------------------
# 2. Ad Strength dos anúncios ativos
# -------------------------------------------------------
ad_strength_query = f"""
    SELECT
        ad_group_ad.ad.id,
        ad_group_ad.ad_strength,
        ad_group_ad.status,
        ad_group_ad.policy_summary.approval_status,
        ad_group_ad.ad.responsive_search_ad.headlines,
        ad_group_ad.ad.responsive_search_ad.descriptions,
        ad_group_ad.ad.final_urls,
        ad_group.name,
        campaign.name,
        metrics.impressions,
        metrics.clicks,
        metrics.cost_micros,
        metrics.conversions,
        metrics.ctr,
        metrics.average_cpc
    FROM ad_group_ad
    WHERE {ACTIVE_CAMPAIGN_FILTER}
      AND ad_group_ad.status = 'ENABLED'
      AND metrics.impressions > 0
    ORDER BY metrics.conversions DESC
"""

ad_resp = ga.search(customer_id=customer_id, query=ad_strength_query)
ads_detail = []
for row in ad_resp:
    ad = row.ad_group_ad.ad
    headlines = [{"text": h.text, "pinned": h.pinned_field.name if h.pinned_field else "NONE"} for h in ad.responsive_search_ad.headlines]
    descriptions = [{"text": d.text, "pinned": d.pinned_field.name if d.pinned_field else "NONE"} for d in ad.responsive_search_ad.descriptions]
    ads_detail.append({
        "id": ad.id,
        "campanha": row.campaign.name,
        "grupo": row.ad_group.name,
        "ad_strength": row.ad_group_ad.ad_strength.name if row.ad_group_ad.ad_strength else "UNKNOWN",
        "status": row.ad_group_ad.status.name,
        "approval": row.ad_group_ad.policy_summary.approval_status.name if row.ad_group_ad.policy_summary else "UNKNOWN",
        "titulos": headlines,
        "descricoes": descriptions,
        "url_final": list(ad.final_urls)[:1],
        "impressoes": row.metrics.impressions,
        "cliques": row.metrics.clicks,
        "custo_brl": round(row.metrics.cost_micros / 1_000_000, 2),
        "conversoes": round(row.metrics.conversions, 2),
        "ctr_pct": round(row.metrics.ctr * 100, 2),
        "cpc_medio_brl": round(row.metrics.average_cpc / 1_000_000, 2),
    })

# -------------------------------------------------------
# 3. Performance de assets individuais (RSA asset view)
# -------------------------------------------------------
asset_query = f"""
    SELECT
        ad_group_ad.ad.id,
        ad_group_ad_asset_view.field_type,
        ad_group_ad_asset_view.performance_label,
        ad_group_ad_asset_view.enabled,
        asset.text_asset.text,
        campaign.name,
        ad_group.name
    FROM ad_group_ad_asset_view
    WHERE {ACTIVE_CAMPAIGN_FILTER}
      AND ad_group_ad_asset_view.enabled = TRUE
    ORDER BY ad_group_ad.ad.id
"""

asset_resp = ga.search(customer_id=customer_id, query=asset_query)
assets = []
for row in asset_resp:
    assets.append({
        "ad_id": row.ad_group_ad.ad.id,
        "campanha": row.campaign.name,
        "grupo": row.ad_group.name,
        "tipo": row.ad_group_ad_asset_view.field_type.name,
        "texto": row.asset.text_asset.text,
        "performance": row.ad_group_ad_asset_view.performance_label.name,
    })

# -------------------------------------------------------
# 4. Extensões ativas
# -------------------------------------------------------
ext_query = f"""
    SELECT
        campaign.name,
        campaign.status,
        campaign_asset.field_type,
        campaign_asset.status
    FROM campaign_asset
    WHERE {ACTIVE_CAMPAIGN_FILTER}
"""

ext_resp = ga.search(customer_id=customer_id, query=ext_query)
extensions = []
for row in ext_resp:
    extensions.append({
        "campanha": row.campaign.name,
        "tipo": row.campaign_asset.field_type.name,
        "status": row.campaign_asset.status.name,
    })

# -------------------------------------------------------
# Salva
# -------------------------------------------------------
output = {
    "keywords_quality_score": keywords_qs,
    "ads_detail": ads_detail,
    "assets_performance": assets,
    "extensions": extensions,
}

out_path = os.path.join(os.path.dirname(__file__), "../../relatorios/adrank_assets.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Salvo em: {os.path.abspath(out_path)}")
print(f"Keywords c/ QS: {len(keywords_qs)} | Anúncios: {len(ads_detail)} | Assets: {len(assets)} | Extensões: {len(extensions)}")
