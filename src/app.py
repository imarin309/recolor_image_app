import streamlit as st
import cv2
from PIL import Image
from utils.change_color import change_color
from streamlit_drawable_canvas import st_canvas

IMAGE_PATH_SUGUMI = "test_image/sugumi.png"


if __name__ == "__main__":
    st.title("クリックした部分の色を塗り替えます")
    new_color = st.color_picker(label="塗り替える色を選んでください", value="#00f900")

    if "img_rgb" not in st.session_state:
        img = cv2.imread(IMAGE_PATH_SUGUMI)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        st.session_state.img_rgb = img_rgb
        st.session_state.points = []
    img_pil = Image.fromarray(st.session_state.img_rgb)

    canvas_result = st_canvas(
        fill_color="rgba(0, 0, 0, 0)",
        stroke_width=1,
        background_image=img_pil,
        update_streamlit=True,
        height=img_pil.height,
        width=img_pil.width,
        drawing_mode="point",
        key="canvas",
    )

    if canvas_result.json_data is not None:
        new_objects = canvas_result.json_data["objects"]
        old_count = len(st.session_state.points)
        if len(canvas_result.json_data["objects"]) > old_count:
            obj = new_objects[-1]
            x, y = int(obj["left"]), int(obj["top"])
            st.session_state.points.append((x, y, new_color))
            st.session_state.img_rgb = change_color(
                x, y, st.session_state.img_rgb, new_color
            )
            st.rerun()
