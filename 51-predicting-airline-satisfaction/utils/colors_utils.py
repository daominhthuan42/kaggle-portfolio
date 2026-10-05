# colors_utils.py
import numpy as np
import seaborn as sns

class ColorUtils:
    """Utility functions for generating color palettes."""

    @staticmethod
    def color(n_colors: int=2, tone: str ="diverging"):
        """
        Generate a list of colors based on predefined Seaborn palettes or custom palettes.

        Parameters
        ----------
        n_colors : int, default=2
            Number of colors to generate. If the palette is continuous (e.g., diverging, viridis),
            colors are sampled evenly across the colormap. If the palette is categorical,
            the first `n_colors` colors are returned.

        tone : str, default="diverging"
            The color style or palette to use. Supported values include:
            - "diverging": Seaborn diverging palette (continuous)
            - "pastel": Pastel palette
            - "muted": Muted palette
            - "husl": HUSL palette
            - "Dark2": Dark2 palette
            - "viridis": Viridis palette
            - "crest": Crest palette
            - "Paired": Paired categorical palette
            - "rocket", "rocket_r": Rocket palette and its reversed version
            - "mako": Mako palette
            - "RdYlGn": Red–Yellow–Green palette
            - "modern": Custom modern-style color set
            - "custom": Custom pastel/bright mixed color set

        Returns
        -------
        list of tuple
            A list of RGB color tuples in the range [0, 1].

        Notes
        -----
        - For continuous palettes (e.g., diverging, viridis, rocket), colors are sampled
        evenly across the palette using `numpy.linspace`.
        - For categorical palettes, the function simply slices the first `n_colors` items.

        Examples
        --------
        >>> color(3, tone="pastel")
        [(...RGB...), (...), (...)]

        >>> color(5, tone="diverging")
        [(0...., 0...., 0....), ...]

        >>> color(4, tone="modern")
        [(0.902, 0.223, 0.275), ...]
        """
        if tone == "diverging":
            cmap = sns.diverging_palette(0, 230, as_cmap=True)
        elif tone == "pastel":
            cmap = sns.color_palette("pastel")
        elif tone == "muted":
            cmap = sns.color_palette("muted")
        elif tone == "husl":
            cmap = sns.color_palette("husl")
        elif tone == "Dark2":
            cmap = sns.color_palette("Dark2")
        elif tone == "viridis":
            cmap = sns.color_palette("viridis")
        elif tone == "crest":
            cmap = sns.color_palette("crest")
        elif tone == "Paired":
            cmap = sns.color_palette("Paired")
        elif tone == "rocket":
            cmap = sns.color_palette("rocket")
        elif tone == "rocket_r":
            cmap = sns.color_palette("rocket_r")
        elif tone == "mako":
            cmap = sns.color_palette("mako")
        elif tone == "RdYlGn":
            cmap = sns.color_palette("RdYlGn")
        elif tone == "modern":
            cmap = sns.color_palette(["#E63946","#F1FAEE","#A8DADC","#457B9D","#1D3557"])
        elif tone == "custom":
            cmap = sns.color_palette(["#A077FF","#D6BBFF","#FFCAF8","#FE86C1","#40CBEA", "#9CE8EE"])

        positions = np.linspace(0, 1, n_colors)
        return [cmap(p) for p in positions] if callable(cmap) else cmap[:n_colors]
