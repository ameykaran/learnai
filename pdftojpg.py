from pdf2image import convert_from_path
import os

def pdf_to_images(pdf_path, output_folder="ocrtochunks/output_images_Test1", dpi=300):
    # Create output folder if it doesn’t exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Convert PDF pages to images
    print(f"Converting '{pdf_path}' to images...")
    images = convert_from_path(pdf_path, dpi=dpi)

    # Save each page as an image
    for i, image in enumerate(images, start=1):
        image_path = os.path.join(output_folder, f"page_{i}.png")
        image.save(image_path, "PNG")
        print(f"Saved: {image_path}")

    print(f"✅ Conversion complete! {len(images)} pages saved in '{output_folder}'.")

# Example usage
if __name__ == "__main__":
    pdf_path = "probabilityTes1.pdf"  # Replace with your PDF file
    pdf_to_images(pdf_path)
