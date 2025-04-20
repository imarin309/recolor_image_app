import streamlit as st
import cv2
from PIL import Image
from utils.change_color import change_color
from streamlit_drawable_canvas import st_canvas

IMAGE_PATH_SUGUMI = "test_image/sugumi.jpeg"

# REFACTER: canvasの処理をクラス化したい

if __name__ == "__main__":
    st.title("クリックした部分の色を塗り替えます")

    # 初期化処理
    if "img_rgb" not in st.session_state:
        img = cv2.imread(IMAGE_PATH_SUGUMI)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        st.session_state.img_rgb = img_rgb

    # OpenCV → PIL
    img_pil = Image.fromarray(st.session_state.img_rgb)

    # キャンバスに画像を描画 & クリックイベント待機
    canvas_result = st_canvas(
        fill_color="rgba(0, 0, 0, 0)",
        stroke_width=1,
        background_image=img_pil,
        update_streamlit=True,
        height=img_pil.height,
        width=img_pil.width,
        drawing_mode="point",  # 点でクリックを受け取る
        key="canvas",
    )



aaa



    # 座標が取得できたら塗り替え処理
    if canvas_result.json_data is not None:
        for obj in canvas_result.json_data["objects"]:
            x, y = int(obj["left"]), int(obj["top"])
            st.session_state.img_rgb = change_color(x, y, st.session_state.img_rgb)
        st.experimental_rerun()
