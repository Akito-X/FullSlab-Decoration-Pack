import os
import shutil

# 現在のPythonスクリプトのディレクトリを基準にパスを設定
script_dir = os.path.dirname(os.path.abspath(__file__))
blockstates_path = os.path.join(script_dir, "blockstates")
models_block_path = os.path.join(script_dir, "models", "block")
textures_block_path = os.path.join(script_dir, "textures", "block")

# 入力値
original = input("元となるブロック名を入力してください: ")
additional = input("追加するブロック名を入力してください: ")
block_type = int(input("ブロックのタイプを入力してください (1: cube_all, 2: cube_column, 3: cube_bottom_top): "))

print(blockstates_path)

# 1. blockstates内にOriginal_slab.jsonを生成
original_slab_json = {
    "variants": {
        "type=bottom": {
            "model": f"minecraft:block/{original}_slab"
        },
        "type=double": {
            "model": f"minecraft:block/{additional}"
        },
        "type=top": {
            "model": f"minecraft:block/{original}_slab_top"
        }
    }
}

# JSONファイルを保存する関数
def save_json(data, path):
    with open(path, 'w') as file:
        import json
        json.dump(data, file, indent=4)

blockstates_file = os.path.join(blockstates_path, f"{original}_slab.json")
save_json(original_slab_json, blockstates_file)

# 2. blockタイプに応じてmodels\block内にAdditional.jsonを生成
if block_type == 1:
    additional_model_json = {
        "parent": "minecraft:block/cube_all",
        "textures": {
            "all": f"minecraft:block/{additional}"
        }
    }
elif block_type == 2:
    additional_model_json = {
        "parent": "minecraft:block/cube_column",
        "textures": {
            "side": f"minecraft:block/{additional}_side",
            "end": f"minecraft:block/{additional}_end"
        }
    }
elif block_type == 3:
    additional_model_json = {
        "parent": "block/cube_bottom_top",
        "textures": {
            "bottom": f"block/{additional}_bottom",
            "top": f"block/{additional}_top",
            "side": f"block/{additional}_side"
        }
    }

additional_model_file = os.path.join(models_block_path, f"{additional}.json")
save_json(additional_model_json, additional_model_file)

# 3. テクスチャファイルのコピーとリネーム
source_texture_dir = r"C:\Users\akito\MyFolder\Minecraft\Data\assets&data(1.21)\assets\minecraft\textures\block"

# originalが"_brick"で終わる場合は"_bricks"に変更
if original.endswith("_brick"):
    texture_name = original + "s"
else:
    texture_name = original
    
source_texture_file = os.path.join(source_texture_dir, f"{texture_name}.png")

def copy_texture(src, dest):
    shutil.copyfile(src, dest)

if block_type == 1:
    # cube_allの場合は1つのファイルをコピー
    dest_texture_file = os.path.join(textures_block_path, f"{additional}.png")
    copy_texture(source_texture_file, dest_texture_file)

elif block_type == 2:
    # cube_columnの場合は2つのファイルをコピー
    dest_texture_file_side = os.path.join(textures_block_path, f"{additional}_side.png")
    dest_texture_file_end = os.path.join(textures_block_path, f"{additional}_end.png")
    copy_texture(source_texture_file, dest_texture_file_side)
    copy_texture(source_texture_file, dest_texture_file_end)

elif block_type == 3:
    # cube_bottom_topの場合は3つのファイルをコピー
    dest_texture_file_bottom = os.path.join(textures_block_path, f"{additional}_bottom.png")
    dest_texture_file_top = os.path.join(textures_block_path, f"{additional}_top.png")
    dest_texture_file_side = os.path.join(textures_block_path, f"{additional}_side.png")
    copy_texture(source_texture_file, dest_texture_file_bottom)
    copy_texture(source_texture_file, dest_texture_file_top)
    copy_texture(source_texture_file, dest_texture_file_side)

print("ファイル生成とコピーが完了しました。")