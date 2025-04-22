import numpy as np
import cv2
from PIL import ImageColor

NEW_COLOR = [127, 255, 212]  # 青色（BGR形式）
NEW_COLOR_DEFAULT = "#b0c4de"


def change_color(x: int, y: int, image, new_color: str = NEW_COLOR_DEFAULT):
    # フラッドフィル（領域を特定）
    mask = np.zeros(
        (image.shape[0] + 2, image.shape[1] + 2), np.uint8
    )  # マスク画像 (周囲+2)
    flood_flags = 4 | cv2.FLOODFILL_MASK_ONLY | (255 << 8)
    tolerance = (7, 7, 7)  # 色の許容範囲 (B, G, R)
    cv2.floodFill(image, mask, (x, y), None, tolerance, tolerance, flood_flags)  # type: ignore

    # エッジを検出
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray_image, 100, 200)

    # エッジ部分のマスクを作成
    edge_mask = edges > 0  # エッジ部分はTrue
    fill_mask = mask[1:-1, 1:-1] > 0  # フラッドフィルの範囲

    # 塗りつぶし領域からエッジ部分を除外
    combined_mask = np.logical_and(fill_mask, ~edge_mask)

    # 色を置換（エッジ部分以外）
    result_image = image.copy()
    new_color_rgb = ImageColor.getcolor(new_color, "RGB")
    result_image[combined_mask] = new_color_rgb

    # 画像を更新して再描画
    return result_image
