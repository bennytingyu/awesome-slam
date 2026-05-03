"""Streamlit UI for side-by-side image generation comparisons."""

from __future__ import annotations

import streamlit as st

from client import ImageGenerationClient, MissingAPIKeyError

st.set_page_config(page_title="Image Gen Comparison", layout="wide")
st.title("Gemini vs GPT Image Comparison")
st.caption("Enter one prompt and compare model outputs side by side.")

prompt = st.chat_input("Type your image generation prompt")

if prompt:
    st.chat_message("user").write(prompt)

    try:
        client = ImageGenerationClient()
    except MissingAPIKeyError as exc:
        st.error(str(exc))
        st.stop()

    col_left, col_right = st.columns(2)

    with st.spinner("Generating images from both models..."):
        gemini_img = client.generate_with_gemini(prompt)
        gpt_img = client.generate_with_gpt_image2(prompt)

    with col_left:
        st.subheader("Gemini Image")
        st.image(gemini_img, use_container_width=True)

    with col_right:
        st.subheader("GPT Image 2")
        st.image(gpt_img, use_container_width=True)
