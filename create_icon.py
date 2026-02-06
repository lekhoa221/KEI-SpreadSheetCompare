from PIL import Image, ImageDraw

def create_icon():
    # optimized for 256x256
    size = (256, 256)
    color = "#107c41" # Excel Green
    
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw rounded rect
    rect_coords = [10, 10, 246, 246]
    draw.rounded_rectangle(rect_coords, radius=40, fill=color)
    
    # Draw "grid" white lines
    draw.line([(10, 80), (246, 80)], fill="white", width=8)
    draw.line([(10, 160), (246, 160)], fill="white", width=8)
    draw.line([(90, 80), (90, 246)], fill="white", width=8) # vertical
    
    # Draw "Diff" badge
    draw.ellipse([160, 160, 250, 250], fill="#f97316", outline="white", width=4)
    # Plus sign
    draw.line([205, 180, 205, 230], fill="white", width=8)
    draw.line([180, 205, 230, 205], fill="white", width=8)

    img.save("app_icon.ico", format='ICO', sizes=[(256, 256)])
    print("Created app_icon.ico")

if __name__ == "__main__":
    try:
        create_icon()
    except ImportError:
        print("Pillow not installed. Skipping icon generation.")
    except Exception as e:
        print(f"Error creating icon: {e}")
