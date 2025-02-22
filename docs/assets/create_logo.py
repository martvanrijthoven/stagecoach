from PIL import Image

# Load images
empty_img_original = Image.open("./stagecoach_empty.png").convert("RGBA")
wheel_img = Image.open("./stagecoach_wheel.png").convert("RGBA")
# Resize wheel
scale_factor = 0.7  # Adjust this value as needed
new_size = (int(wheel_img.width * scale_factor), int(wheel_img.height * scale_factor))
wheel_img = wheel_img.resize(new_size, Image.LANCZOS)

# Define parameters
num_frames = 20  # Number of frames in the GIF
angle_step = 360 / num_frames

frames = []

# Position where the wheel should be placed
wheel_x = empty_img_original.width // 2 - wheel_img.width // 2  # Adjust as needed
wheel_y = empty_img_original.height // 2 - wheel_img.height // 2  # Adjust as needed
wheel_x += 335

for i in range(num_frames):
    empty_img = empty_img_original.copy()  # Ensure fresh background
    rotated_wheel = wheel_img.rotate(i * angle_step, resample=Image.BICUBIC, center=(wheel_img.width // 2, wheel_img.height // 2)).convert("RGBA")
    
    # Create a new frame with transparency
    frame = Image.new("RGBA", empty_img.size, (255, 255, 255, 0))  # Fully transparent background
    frame.paste(empty_img, (0, 0), empty_img)
    frame.paste(rotated_wheel, (wheel_x, wheel_y), rotated_wheel)
    frames.append(frame)

# Save as GIF
output_path = "./stagecoach_wheel_animation.gif"
frames[0].save(output_path, save_all=True, append_images=frames[1:], duration=100, loop=0, disposal=2, transparency=0)

print(f"GIF saved to {output_path}")
