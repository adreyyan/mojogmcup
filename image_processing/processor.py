from PIL import Image
import os

def add_gm_cup(nft_image_path, gm_cup_path, output_folder):
    # Open the NFT image
    nft_image = Image.open(nft_image_path).convert("RGBA")
    
    # Open the GM cup image
    gm_cup = Image.open(gm_cup_path).convert("RGBA")
    
    # Calculate the new size for the GM cup image, maintaining the aspect ratio
    aspect_ratio = gm_cup.width / gm_cup.height
    new_height = int(nft_image.width / aspect_ratio)
    
    # Resize the GM cup image to match the width of the NFT image
    if hasattr(Image, "ANTIALIAS"):
        gm_cup_resized = gm_cup.resize((nft_image.width, new_height), Image.ANTIALIAS)
    else:
        gm_cup_resized = gm_cup.resize((nft_image.width, new_height))
    
    # Calculate position to paste, centered vertically
    position = (0, (nft_image.height - new_height) // 2)
    
    # Paste the resized GM cup image onto the NFT image
    nft_image.paste(gm_cup_resized, position, gm_cup_resized)
    
    # Save the modified image to the output folder
    output_path = os.path.join(output_folder, os.path.basename(nft_image_path))
    nft_image.save(output_path, format="PNG")
    
    return output_path
