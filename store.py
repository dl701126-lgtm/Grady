import streamlit as st

st.set_page_config(page_title="My Online Store", layout="wide")

st.title("🛒 Online Store ")

# 商品資料
products = [
    {"name": "原子筆", "price": 20, "img": "images/pen.jpg"},
    {"name": "橡皮擦", "price": 15, "img": "images/eraser.jpg"},
    {"name": "Tomica 小汽車 No.1", "price": 120, "img": "images/tomica1.jpg"},
]

# 用三欄顯示
cols = st.columns(3)

for col, product in zip(cols, products):
    with col:
        st.image(product["img"], width=200)
        st.subheader(product["name"])
        st.write(f"💲 Price: {product['price']} 元")
        if st.button(f"加入購物車：{product['name']}"):
            st.success(f"{product['name']} 已加入購物車！")
