from PIL import Image
import numpy as np

def process_logo():
    input_path = "/home/akshay/Documents/Projects/synth-fm/frontend/public/logo-original.png"
    output_transparent_path = "/home/akshay/Documents/Projects/synth-fm/frontend/public/logo-transparent.png"
    output_favicon_path = "/home/akshay/Documents/Projects/synth-fm/frontend/public/favicon.ico"
    
    img = Image.open(input_path).convert("RGBA")
    datas = img.getdata()
    
    newData = []
    # Target background color #07001F is (7, 0, 31)
    # Adding a small tolerance
    for item in datas:
        if item[0] < 20 and item[1] < 20 and item[2] < 50:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
            
    img.putdata(newData)
    img.save(output_transparent_path, "PNG")
    print(f"Saved transparent logo to {output_transparent_path}")
    
    # Save original as favicon (keep background for visibility in browser tabs typically)
    # Or should we use transparent? User said "faviicon can have some background"
    # So we use the original input for favicon, just resized.
    img_fav = Image.open(input_path)
    img_fav.save(output_favicon_path, sizes=[(32, 32)])
    print(f"Saved favicon to {output_favicon_path}")

if __name__ == "__main__":
    process_logo()
