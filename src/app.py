import streamlit as st
import cv2
from PIL import Image
from utils.change_color import change_color
from streamlit_drawable_canvas import st_canvas
import numpy as np

IMAGE_PATH_DEFAULT = "test_image/sugumi.png"


if __name__ == "__main__":
    st.title("クリックした部分の色を塗り替えます")
    new_color = st.color_picker(label="塗り替える色を選んでください", value="#00f900")

    if "img_rgb" not in st.session_state:
        img = cv2.imread(IMAGE_PATH_DEFAULT)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        st.session_state.img_rgb = img_rgb
        st.session_state.points = []

    uploaded_file = st.file_uploader(
        "画像をアップロードしてください（PNG, JPG）", type=["png", "jpg", "jpeg"]
    )
    if uploaded_file is not None:
        uploaded_file_id = uploaded_file.name + str(uploaded_file.size)
        if st.session_state.get("last_uploaded") != uploaded_file_id:
            pil_img = Image.open(uploaded_file).convert("RGB")
            img_rgb = np.array(pil_img)
            st.session_state.img_rgb = img_rgb
            st.session_state.last_uploaded = uploaded_file_id

    img_pil = Image.fromarray(st.session_state.img_rgb)

    canvas_result = st_canvas(
        fill_color="rgba(0, 0, 0, 0)",
        stroke_width=0,
        background_image=img_pil,
        update_streamlit=True,
        height=img_pil.height,
        width=img_pil.width,
        drawing_mode="point",
        key="canvas",
    )

    if canvas_result.json_data is not None:
        objects = canvas_result.json_data["objects"]
        old_count = len(st.session_state.points)
        if len(canvas_result.json_data["objects"]) > old_count:
            new_object = objects[-1]
            x, y = int(new_object["left"]), int(new_object["top"])
            st.session_state.points.append((x, y, new_color))
            st.session_state.img_rgb = change_color(
                x, y, st.session_state.img_rgb, new_color
            )
            st.rerun()
