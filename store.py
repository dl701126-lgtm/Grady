import streamlit as st
import json

st.set_page_config(page_title="Stationery & Tomica Store", layout="wide")

# 讀取商品資料
with open("products.json", "r", encoding="utf-8") as f:
    products = json.load(f)

st.title("🛍️ my online store")

cols = st.columns(3)

# 顯示商品
for idx, item in enumerate(products):
    with cols[idx % 3]:
        st.image(item["image"], width=220)
        st.subheader(item["name"])
        st.write(item["description"])
        st.write(f"💰 價格：NT$ {item['price']}")
        st.button("加入購物車", key=f"add_{idx}")

st.markdown("---")
st.write("示範版本：目前尚未包含真正購物車功能。")
