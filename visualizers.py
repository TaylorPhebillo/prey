from PIL import Image, ImageDraw
from creature import Creature


def print_locations(cats, mice, killed):
    print(f"cats:{cats}\nmice:{mice}\nkilled{killed}")


class CatMouseVisualizer:
    def __init__(
            self,
            size=256,
            target="simulated_result",
            suffix="",
            filetype=".gif",
            limit=None):
        self.limit = limit
        self.target = target + suffix + filetype
        self.img_size = size
        self.imgs = []

    def visualize_locations(self, cats, mice, killed):
        self.imgs.append(
            Image.new('RGB', (self.img_size, self.img_size), "black"))
        draw = ImageDraw.Draw(self.imgs[-1])
        dot_size = self.img_size * Creature().nearness_threshold / 2

        def draw_at(pos, color):
            draw.ellipse(
                (pos[0] *
                 self.img_size -
                 dot_size,
                 pos[1] *
                    self.img_size -
                    dot_size,
                    pos[0] *
                    self.img_size +
                    dot_size,
                    pos[1] *
                    self.img_size +
                    dot_size),
                fill=color)

        for dead in killed:
            draw_at(dead, "blue")
        for mouse in mice:
            draw_at(mouse, "white")
        for cat in cats:
            draw_at(cat, "red")
        if self.limit and self.limit == len(self.imgs):
            self.complete()

    def complete(self):
        print(f"Saving {len(self.imgs)} images into a gif")
        Image.new(
            'RGB', (self.img_size, self.img_size),
            "black").save(
            fp=self.target, format='GIF', append_images=self.imgs,
            save_all=True, duration=20, loop=0)
