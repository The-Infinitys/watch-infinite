import colorsys
import math


def generate_complete_cyber_watch_svg_string(
    radius=140, cx=200, cy=100, use_rainbow=True
):
    """時針・分針・秒針、そして最新の反転剣型メモリをすべて含んだ

    1枚の完全なSVGコードを文字列として生成する関数
    """
    svg_lines = []

    # 1. 完全に完結するSVGヘッダーの記述
    svg_lines.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg" viewBox="0 0 {cx * 2} {cy * 2}">'
    )

    # 2. 🌈 円周に沿って（時計回りに）なだらかに変化するグラデーションの定義群
    if use_rainbow:
        svg_lines.append("  <defs>")
        for i in range(60):
            # 目盛りの中心角度（ラジアン）
            angle_rad = math.radians(i * 6 - 90)

            # 円周の接線方向（時計回りの進む向き）のベクトルを計算
            # 通常の放射方向から90度ずらすことで「円周に沿う向き」にします
            tangent_cos = -math.sin(angle_rad)
            tangent_sin = math.cos(angle_rad)

            # 目盛りの配置される中心座標
            mx = cx + radius * math.cos(angle_rad)
            my = cy + radius * math.sin(angle_rad)

            # 各パーツの幅に合わせたグラデーションの開始点と終了点（接線方向に約15px幅）
            x1 = mx - 7.5 * tangent_cos
            y1 = my - 7.5 * tangent_sin
            x2 = mx + 7.5 * tangent_cos
            y2 = my + 7.5 * tangent_sin

            # 現在の目盛りの色（左端）と、次の目盛りに繋がる色（右端）
            h1 = i / 60.0
            h2 = (i + 1) / 60.0

            r1, g1, b1 = colorsys.hsv_to_rgb(h1, 1.0, 1.0)
            r2, g2, b2 = colorsys.hsv_to_rgb(h2, 1.0, 1.0)

            c1 = f"#{int(r1 * 255):02x}{int(g1 * 255):02x}{int(b1 * 255):02x}"
            c2 = f"#{int(r2 * 255):02x}{int(g2 * 255):02x}{int(b2 * 255):02x}"

            svg_lines.append(
                f'    <linearGradient id="grad_{i}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" gradientUnits="userSpaceOnUse">'
            )
            svg_lines.append(f'      <stop offset="0%" stop-color="{c1}" />')
            svg_lines.append(f'      <stop offset="100%" stop-color="{c2}" />')
            svg_lines.append("    </linearGradient>")
        svg_lines.append("  </defs>")

    # 3. 🧱 メモリ（インデックス）の一括自動計算ループ
    svg_lines.append("  <g id='clock-cyber-indices'>")

    for i in range(60):
        angle = i * 6
        is_five_min = i % 5 == 0
        is_cardinal = i % 15 == 0  # 0(12)時, 3時, 6時, 9時

        fill_color = f"url(#grad_{i})" if use_rainbow else "#ffffff"
        opacity_str = "" if is_five_min else " opacity='0.6'"

        # 基準となるY座標（12時の位置の半径境界線＝すべての目盛りの『境目』）
        y_boundary = cy - radius

        if is_cardinal:
            # ⚔️ 剣型 (0, 3, 6, 9時) -> 境界線がパーツの最大幅の境目になるよう配置
            path_d = (
                f"M {cx} {y_boundary - 4} l 6 4 v 14 l -6 6 l -6 -6 v -14 z "
                f"M {cx} {y_boundary - 1} l 3 1 v 10 l -3 4 l -3 -4 v -10 z"
            )
            svg_lines.append(
                f"    <path d='{path_d}' transform='rotate({angle}, {cx}, {cy})' fill='{fill_color}' fill-rule='evenodd' />"
            )

        elif is_five_min:
            # 5分刻み：大きめの「中空ひし形」
            in_len = 12
            out_len = 6
            w = 5
            w_in = 2.5
            path_d = (
                f"M {cx} {y_boundary - out_len} l {w} {out_len} l -{w} {in_len} l -{w} -{in_len} z "
                f"M {cx} {y_boundary - (out_len - 2)} l {w_in} {out_len - 2} l -{w_in} {in_len - 3} l -{w_in} -{in_len - 3} z"
            )
            svg_lines.append(
                f"    <path d='{path_d}' transform='rotate({angle}, {cx}, {cy})' fill='{fill_color}' fill-rule='evenodd' />"
            )

        else:
            # 1分刻み：通常の「ひし形（内長・外短）」
            in_len = 8
            out_len = 4
            w = 2.5
            path_d = f"M {cx} {y_boundary - out_len} l {w} {out_len} l -{w} {in_len} l -{w} -{in_len} z"
            svg_lines.append(
                f"    <path d='{path_d}' transform='rotate({angle}, {cx}, {cy})' fill='{fill_color}'{opacity_str} />"
            )

    svg_lines.append("  </g>")
    svg_lines.append("</svg>")

    return "\n".join(svg_lines)


# 🚀 動作検証：半径140px、中心(200, 200)で完全版全体のXML文字列を出力
print(
    generate_complete_cyber_watch_svg_string(
        radius=210, cx=220, cy=220, use_rainbow=False
    )
)
