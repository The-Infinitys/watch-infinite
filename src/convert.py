import glob
import os

import cairosvg

# 1024x1024の枠に収める設定
TARGET_SIZE = 1024

# カレントディレクトリにあるすべてのSVGファイルを検索
svg_files = glob.glob("*.svg")

if not svg_files:
    print("SVGファイルが見つかりませんでした。")
else:
    print(f"{len(svg_files)}個のSVGファイルを処理します...")

    for svg_path in svg_files:
        png_path = os.path.splitext(svg_path)[0] + ".png"

        try:
            # アスペクト比を維持し、長辺が1024pxになるように強制リサイズして透過PNG出力
            cairosvg.svg2png(
                url=svg_path,
                write_to=png_path,
                output_width=TARGET_SIZE,
                output_height=TARGET_SIZE,
            )
            print(f"変換成功: {svg_path} -> {png_path}")

        except Exception as e:
            print(f"エラー発生 ({svg_path}): {e}")

print("すべての処理が完了しました！")
